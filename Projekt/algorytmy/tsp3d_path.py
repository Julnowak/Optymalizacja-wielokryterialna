import random
import math
import copy

import numpy as np
import matplotlib

from algorytmy.terrain import terrain_generator

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from scipy.spatial.distance import euclidean

#############################
#  2) KLASA GA TSP 3D PATH  #
#############################

class GeneticTSP3DPath:
    """
    GA w stylu "komiwojażer 3D" do znajdowania ścieżki:
      - Mamy siatkę NxN (każdy piksel to miasto).
      - Start i end: [x_start, y_start], [x_end, y_end].
      - Ścieżka to sekwencja pikseli (miast), gdzie każdy kolejny
        jest sąsiadem 4-kierunkowym (góra/dół/lewo/prawo).
      - Funkcja celu to suma odległości euklidesowych 3D.
    """

    def __init__(self, terrain):
        self.terrain = terrain
        self.size_x, self.size_y = terrain.shape

        # Cache (opcjonalnie) na odległości
        self.coordinates_cache = {}
        self.path_cache = {}

        # Statystyki
        self.coordinates_cache_hits = 0
        self.path_cache_hits = 0
        self.invalid_paths = 0
        self.children_mutated = 0

    #############################
    #  Funkcje obliczające     #
    #############################

    def distance_3d(self, p1, p2):
        """
        p1, p2 = (x1, y1), (x2, y2)
        Z do obliczenia: z1 = terrain[x1, y1], z2 = terrain[x2, y2]
        Odległość euklidesowa 3D.
        """
        key = tuple(sorted((p1, p2)))
        if key in self.coordinates_cache:
            self.coordinates_cache_hits += 1
            return self.coordinates_cache[key]

        x1, y1 = p1
        x2, y2 = p2
        z1 = self.terrain[x1, y1]
        z2 = self.terrain[x2, y2]

        dist = euclidean((x1, y1, z1), (x2, y2, z2))
        self.coordinates_cache[key] = dist
        return dist

    def distance_path(self, path):
        """
        Suma odległości 3D kolejnych miast w path (start->...->end).
        path = [ (x0,y0), (x1,y1), ... ]
        """
        key = tuple(path)
        if key in self.path_cache:
            self.path_cache_hits += 1
            return self.path_cache[key]

        dist_sum = 0.0
        for i in range(len(path) - 1):
            dist_sum += self.distance_3d(path[i], path[i+1])

        self.path_cache[key] = dist_sum
        return dist_sum

    #############################
    #  Walidacja ścieżki       #
    #############################

    def valid_path(self, path):
        """
        1) Brak duplikatów w środku (pomijając start i end - chociaż w tym problemie
           najpewniej nie chcemy odwiedzać dwa razy tego samego miasta).
        2) Kolejne punkty w path to sąsiedzi w 2D (|dx|+|dy|=1).
        3) Mieszczą się w [0..size_x-1] i [0..size_y-1].
        """
        # Sprawdzenie duplikatów:
        inner = path[1:-1]
        if len(inner) != len(set(inner)):
            self.invalid_paths += 1
            return False

        # Sprawdzenie sąsiedztwa:
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]
            if abs(x2 - x1) + abs(y2 - y1) != 1:
                # Nie jest sąsiadem w 4-kierunkach
                self.invalid_paths += 1
                return False
            # Sprawdź, czy w granicach:
            if not (0 <= x2 < self.size_x and 0 <= y2 < self.size_y):
                self.invalid_paths += 1
                return False

        return True

    #############################
    #  Generowanie ścieżek     #
    #############################

    def generate_random_path(self, start, end):
        """
        Tworzy losową ścieżkę od start do end, wykonując 'losowe kroki'
        w 4-kierunkowym sąsiedztwie, dopóki nie osiągniemy end lub
        nie osiągniemy pewnego limitu długości (by nie wpaść w pętlę).
        """
        path = [start]
        current = start
        max_steps = 2 * (self.size_x + self.size_y)  # np. limit kroków
        for _ in range(max_steps):
            if current == end:
                break
            x, y = current
            moves = []
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.size_x and 0 <= ny < self.size_y:
                    moves.append((nx, ny))
            if not moves:
                break
            next_move = random.choice(moves)
            path.append(next_move)
            current = next_move

        # Jeśli w max_steps nie dotarliśmy do end, dopisujemy end i liczymy na validację
        if path[-1] != end:
            path.append(end)
        return path

    def generate_population(self, pop_size, start, end):
        """
        Generuje populację (pop_size ścieżek),
        każda ścieżka to "losowy spacer" od start do end (lub do limitu).
        """
        population = []
        seen = set()

        while len(population) < pop_size:
            new_path = self.generate_random_path(start, end)
            path_tuple = tuple(new_path)
            if path_tuple not in seen and self.valid_path(new_path):
                population.append(new_path)
                seen.add(path_tuple)

        return population

    #############################
    #  Selekcja, krzyżowanie   #
    #############################

    def select_elites(self, population, elite_size):
        """
        Najlepsze (elite_size) ścieżek o najmniejszej sumie dystansu.
        """
        scored = [(p, self.distance_path(p)) for p in population]
        scored.sort(key=lambda x: x[1])
        return [s[0] for s in scored[:elite_size]]

    def create_pool(self, population, tournament_size, pool_size):
        """
        Selekcja turniejowa: z populacji wybieramy 'tournament_size',
        zwycięzcę (o najmniejszym dystansie) dodajemy do puli,
        usuwamy go z rozważania i powtarzamy.
        """
        mating_pool = []
        pop_copy = population[:]
        while len(mating_pool) < pool_size and len(pop_copy) >= tournament_size:
            candidates = random.sample(pop_copy, tournament_size)
            best_cand = min(candidates, key=lambda x: self.distance_path(x))
            mating_pool.append(best_cand)
            pop_copy.remove(best_cand)

        return mating_pool

    def crossover(self, parent1, parent2):
        """
        Próba łączenia dwóch ścieżek w jedną (losowo łączymy fragmenty).
        Idea:
         1) Bierzemy prefix z parent1 do pewnego miejsca,
         2) Następnie staramy się kontynuować z parent2,
            wybierając takie kroki, by iść w stronę end, ale jednocześnie
            nie łamać reguły sąsiedztwa.
        """
        # Bardzo uproszczone - można wymyślić inny crossover.
        size1 = len(parent1)
        size2 = len(parent2)

        cut1 = random.randint(1, size1-2)  # pomijając start/end
        child = parent1[:cut1]

        # Próba dokończenia childa fragmentem parent2
        tail = parent2[1:-1]  # środek
        current = child[-1]
        for pt in tail:
            # sprawdź, czy jest sąsiadem i czy w 2D nie łamie granic
            if abs(pt[0]-current[0]) + abs(pt[1]-current[1]) == 1:
                child.append(pt)
                current = pt

        # dodaj end
        if child[-1] != parent1[-1]:
            if child[-1] != parent2[-1]:
                child.append(parent1[-1])  # wymuszenie end (lub parent2[-1], bo end
        return child

    def mutate(self, path):
        """
        Mutacja: losowa zmiana jednego kroku na inny (o 1 piksel).
        """
        if len(path) <= 2:
            return path
        new_path = path[:]
        idx = random.randint(1, len(path)-2)  # omijamy start=0 i end=-1
        x, y = new_path[idx]
        moves = []
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size_x and 0 <= ny < self.size_y:
                moves.append((nx, ny))
        if moves:
            new_path[idx] = random.choice(moves)
        return new_path

    def generate_children(self, mating_pool, offspring_count):
        """
        Tworzy dzieci przez 'crossover'. Losowo dobieramy pary.
        """
        children = []
        while len(children) < offspring_count:
            p1 = random.choice(mating_pool)
            p2 = random.choice(mating_pool)
            if p1 != p2:
                child = self.crossover(p1, p2)
                if self.valid_path(child):
                    children.append(child)
        return children


#############################
#  3) FUNKCJA GŁÓWNA (GA)   #
#############################

def run_tsp3d_path(
    terrain,
    start_2d,
    end_2d,
    pop_size=100,
    num_of_generations=50,
    elite_size=10,
    tournament_size=5,
    offspring_rate=0.5,
    mutation_rate=0.1
):
    """
    Uruchamia GA 3D:
     - terrain to map 2D o rozmiarze NxN
     - start_2d, end_2d => (x_s, y_s), (x_e, y_e)
     - pop_size => rozmiar populacji
     - num_of_generations => ile iteracji GA
     - parametry selekcji i mutacji.
    Zwraca: (best_path, best_cost)
    """
    ga = GeneticTSP3DPath(terrain)

    # 1) Inicjalizacja populacji
    population = ga.generate_population(pop_size, tuple(start_2d), tuple(end_2d))
    best_individual = min(population, key=lambda p: ga.distance_path(p))
    best_cost = ga.distance_path(best_individual)
    print(f"Initial best dist = {best_cost:.4f}")

    # 2) Pętla GA
    for gen in range(num_of_generations):
        print(f"\nGENERATION {gen+1}/{num_of_generations}")

        # a) Elity
        elites = ga.select_elites(population, elite_size)
        non_elites = [p for p in population if p not in elites]

        # b) Mating pool
        pool_size = pop_size - elite_size
        mating_pool = ga.create_pool(non_elites, tournament_size, pool_size)
        mating_pool += elites

        # c) Tworzenie dzieci
        offspring_count = int(len(mating_pool) * offspring_rate)
        children = ga.generate_children(mating_pool, offspring_count)

        # d) Mutacja
        for i in range(len(children)):
            if random.random() < mutation_rate:
                new_child = ga.mutate(children[i])
                if ga.valid_path(new_child):
                    children[i] = new_child
                ga.children_mutated += 1

        # e) Nowa populacja
        new_population = elites + children
        if len(new_population) < pop_size and len(non_elites) > 0:
            needed = pop_size - len(new_population)
            new_population += random.sample(non_elites, min(needed, len(non_elites)))
        # w razie nadmiaru
        new_population = new_population[:pop_size]
        population = new_population

        # f) Sprawdzamy, czy mamy lepsze
        current_best = min(population, key=lambda p: ga.distance_path(p))
        current_dist = ga.distance_path(current_best)
        if current_dist < best_cost:
            best_cost = current_dist
            best_individual = current_best
            print(f"  New best = {best_cost:.4f}")
        else:
            print(f"  Curr best in pop = {current_dist:.4f}, global best={best_cost:.4f}")

    return best_individual, best_cost


#############################
#  4) WIZUALIZACJA          #
#############################

def plot_graph(best_path, terrain, start, end):
    """
    Rysuje 2D mapę i nanosi ścieżkę.
    best_path to lista [(x,y), (x2,y2), ...].
    """
    plt.close("all")
    plt.figure(figsize=(6,6))
    plt.imshow(terrain, origin='upper', cmap="magma")

    # Osobno x i y
    X = [p[0] for p in best_path]
    Y = [p[1] for p in best_path]
    plt.plot(X, Y, 'ro-')

    plt.scatter(end[0], end[1], 80, marker='*', c='k')
    plt.scatter(start[0], start[1], 80, marker='o', c='k')
    plt.title("GA TSP 3D - only neighbor moves")
    plt.show()


#############################
#  5) MAIN DEMO             #
#############################

if __name__ == "__main__":
    # Parametry
    map_size = (10, 10)
    start = [0, 0]
    end = [9, 9]

    terrain = terrain_generator(
        noise_num=1,
        terrain_size=map_size,
        terrain_type="hills"
    )

    best_path, best_cost = run_tsp3d_path(
        terrain,
        start,
        end,
        pop_size=50,
        num_of_generations=50,
        elite_size=5,
        tournament_size=3,
        offspring_rate=0.6,
        mutation_rate=0.1
    )

    print(f"\nDONE. Best cost = {best_cost:.4f}")
    print("BEST PATH:", best_path)

    plot_graph(best_path, terrain, start, end)