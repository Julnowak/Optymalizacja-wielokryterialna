import random
import math
import copy
import time

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from scipy.spatial.distance import euclidean
from algorytmy.terrain import terrain_generator

#############################
#  1) Wizualizacja          #
#############################

def plot_graphs_static(all_paths, terrain, starts, ends):
    """
    Rysuje 2D mapę 'terrain' i nanosi wszystkie ścieżki z listy all_paths.
    (wersja statyczna)
    """
    plt.close("all")
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(terrain, origin='upper', cmap="magma")

    colors = ["red", "blue", "green", "purple", "orange", "yellow", "white", "cyan"]

    for i, path in enumerate(all_paths):
        # path = [(r,c), (r2,c2), ...]
        X = [p[1] for p in path]
        Y = [p[0] for p in path]
        c = colors[i % len(colors)]
        ax.plot(X, Y, marker='o', markersize=4, color=c, linewidth=2, label=f"Robot {i+1}")

        # zaznacz start i koniec
        sx, sy = starts[i]
        gx, gy = ends[i]
        ax.scatter(sy, sx, 100, marker='o', color='black')
        ax.scatter(gy, gx, 100, marker='*', color='black')

    ax.set_title("Multi-Robot TSP 3D (statyczny widok)")
    ax.legend()
    plt.show()


def plot_graphs_animation(all_paths, terrain, starts, ends):
    """
    Animacja krok-po-kroku: w każdej klatce rysujemy po jednym kroku
    ruchu każdego robota (o ile jeszcze nie zakończył ścieżki).
    """
    plt.close("all")
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(terrain, origin='upper', cmap="magma")

    colors = ["red", "blue", "green", "purple", "orange", "yellow", "white", "cyan"]

    # narysuj punkty startu i celu (duże markery)
    for i, (st, en) in enumerate(zip(starts, ends)):
        ax.scatter(st[1], st[0], 100, marker='o', facecolors="k", edgecolors="k")
        ax.scatter(en[1], en[0], 100, marker='*', facecolors="k", edgecolors="k")

    # obliczamy maksymalną liczbę kroków = najdłuższa ścieżka
    max_len = max(len(path) for path in all_paths)

    # funkcja aktualizacji klatek w animacji
    def update(frame):
        ax.clear()
        ax.imshow(terrain, origin='upper', cmap="magma")

        # ponownie rysuj starty i końce
        for i, (st, en) in enumerate(zip(starts, ends)):
            ax.scatter(st[1], st[0], 100, marker='o', facecolors="k", edgecolors="k")
            ax.scatter(en[1], en[0], 100, marker='*', facecolors="k", edgecolors="k")

        # rysujemy historię do klatki 'frame'
        for i, path in enumerate(all_paths):
            c = colors[i % len(colors)]

            # narysuj wszystkie poprzednie kroki do 'frame', aby widać było trajektorię
            sub_path = path[:frame + 1]
            X = [p[1] for p in sub_path]
            Y = [p[0] for p in sub_path]
            ax.plot(X, Y, marker='o', markersize=4, color=c, linewidth=2)

        ax.set_title(f"Multi-Robot TSP 3D - animacja, krok={frame}")

    ani = animation.FuncAnimation(fig, update, frames=max_len, interval=300, repeat=False)
    plt.show()

#############################
#  2) Klasa GA TSP 3D Path  #
#############################

class GeneticTSP3DPath:

    def __init__(self, terrain, occupied_paths=None):
        self.terrain = terrain
        self.size_x, self.size_y = terrain.shape

        # Buforowanie kosztów ruchu (p1, p2) -> cost
        self.cost_cache = {}
        # Buforowanie kosztu całej ścieżki
        self.path_cost_cache = {}

        # statystyki
        self.invalid_paths = 0
        self.children_mutated = 0

        # Ścieżki już wyznaczone (dla poprzednich robotów)
        if occupied_paths is None:
            self.occupied_paths = []
        else:
            self.occupied_paths = occupied_paths

        # Duża kara kolizji
        self.collision_penalty = 1e10

        # 8 kierunków
        self.directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

    #############################
    #   Funkcja Kosztu      #
    #############################

    def cost_move(self, p1, p2):
        """
        Identycznie jak w A*:
          cost = 1 + 10000 * abs( z2 - z1 )
        """
        if p1 > p2:
            key = (p2, p1)
        else:
            key = (p1, p2)

        if key in self.cost_cache:
            return self.cost_cache[key]

        r1, c1 = p1
        r2, c2 = p2
        z1 = self.terrain[r1, c1]
        z2 = self.terrain[r2, c2]

        # Tak samo jak w A*: 1 + 10000*(różnica w wysokości)
        base_cost = 1 + 10000 * abs(z2 - z1)
        self.cost_cache[key] = base_cost
        return base_cost

    def distance_path(self, path):
        """
        Suma 'A*-like' kosztów ruchu + kara za kolizje w oknie +/-2.
        """
        key = tuple(path)
        if key in self.path_cost_cache:
            return self.path_cost_cache[key]

        # 1) Suma kosztów ruchów (tak jak w A*)
        cost = 0.0
        for i in range(len(path) - 1):
            cost += self.cost_move(path[i], path[i+1])

        # 2) Kolizje (uwzględniamy okno +/-2 wokół i-tego kroku)
        for i, pos in enumerate(path):
            for other_path in self.occupied_paths:
                # Sprawdzamy kroki i-2, i-1, i, i+1, i+2
                for dt in range(-2, 3):
                    step_idx = i + dt
                    if step_idx < 0:
                        continue
                    if step_idx < len(other_path):
                        if other_path[step_idx] == pos:
                            cost += self.collision_penalty
                            # (opcjonalnie możesz wstawić print("ffff") jak w A*)
                            break  # wystarczy raz dodać karę

        self.path_cost_cache[key] = cost
        return cost

    #############################
    #   Walidacja ścieżki      #
    #############################

    def valid_path(self, path):
        """
        - Sprawdza brak duplikatów (poza start i end)
        - Sprawdza czy każdy krok jest 8-kierunkowy
        - Sprawdza czy w granicach NxN
        """
        if len(path) < 2:
            return False

        # Sprawdzenie duplikatów w środku
        mid = path[1:-1]
        if len(mid) != len(set(mid)):
            self.invalid_paths += 1
            return False

        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i+1]
            # sprawdzamy, czy (r2-r1, c2-c1) jest w zbiorze dozwolonych ruchów (8)
            dr = r2 - r1
            dc = c2 - c1
            if (dr, dc) not in self.directions:
                self.invalid_paths += 1
                return False

            # sprawdzanie w granicach
            if not (0 <= r2 < self.size_x and 0 <= c2 < self.size_y):
                self.invalid_paths += 1
                return False

        return True

    #############################
    #  Generowanie ścieżek     #
    #############################

    def generate_random_path(self, start, end):
        """
        Generuje ścieżkę max do 2*(Nx+Ny) kroków w 8-kier.
        Częściowo losowa, częściowo preferencja w stronę end.
        """
        max_steps = 2 * (self.size_x + self.size_y)
        visited = set([start])
        path = [start]

        current = start
        for _ in range(max_steps):
            if current == end:
                break
            r, c = current

            # generujemy 8 sąsiadów
            neighbors = []
            for (dx, dy) in self.directions:
                nr, nc = r+dx, c+dy
                if 0 <= nr < self.size_x and 0 <= nc < self.size_y:
                    if (nr, nc) not in visited:
                        neighbors.append((nr,nc))

            if not neighbors:
                break

            # sortowanie wg "odległości manhattan do end" (lub euklides 2D)
            neighbors.sort(key=lambda x: abs(x[0]-end[0]) + abs(x[1]-end[1]))
            top_k = neighbors[:3]
            nextp = random.choice(top_k)
            path.append(nextp)
            visited.add(nextp)
            current = nextp

        if path[-1] != end:
            path.append(end)

        return path

    def generate_population(self, pop_size, start, end):
        """
        Tworzymy populację, sprawdzamy valid_path, jak ok - dodajemy.
        """
        population = []
        seen = set()
        while len(population) < pop_size:
            newp = self.generate_random_path(start, end)
            keyp = tuple(newp)
            if keyp not in seen and self.valid_path(newp):
                population.append(newp)
                seen.add(keyp)
        return population

    #############################
    #   Selekcja i krzyżowanie #
    #############################

    def select_elites(self, population, elite_size):
        scored = [(p, self.distance_path(p)) for p in population]
        scored.sort(key=lambda x: x[1])
        return [s[0] for s in scored[:elite_size]]

    def create_pool(self, population, tournament_size, pool_size):
        """
        Selekcja turniejowa (losujemy tournament_size osobników
        i wybieramy z nich najlepszego).
        """
        mating_pool = []
        pop_copy = population[:]
        while len(mating_pool) < pool_size and len(pop_copy) >= tournament_size:
            cands = random.sample(pop_copy, tournament_size)
            best_cand = min(cands, key=lambda x: self.distance_path(x))
            mating_pool.append(best_cand)
            pop_copy.remove(best_cand)
        return mating_pool

    def crossover(self, parent1, parent2):
        """
        Krzyżowanie - bierzemy prefix z parent1,
        wklejamy środek parent2 (jeśli pasuje 8-kier i brak duplikatów),
        doklejamy end.
        """
        if len(parent1) < 2 or len(parent2) < 2:
            return parent1

        cut = random.randint(1, max(len(parent1)-2, 1))
        child = parent1[:cut]
        used = set(child)
        cur = child[-1]
        # środek parent2 (bez startu i końca)
        middle = parent2[1:-1]
        for pt in middle:
            if pt not in used:
                # sprawdzamy, czy (pt - cur) jest w directions
                dr = pt[0] - cur[0]
                dc = pt[1] - cur[1]
                if (dr, dc) in self.directions:
                    child.append(pt)
                    used.add(pt)
                    cur = pt

        endp = parent1[-1]
        if child[-1] != endp:
            child.append(endp)

        return child

    def mutate(self, path):
        """
        Mutacja - w jednym losowym miejscu staramy się
        zastąpić punkt innym 8-kierunkowym (bez duplikatów).
        """
        if len(path) < 3:
            return path
        newp = path[:]
        idx = random.randint(1, len(newp) - 2)
        r, c = newp[idx]

        # losowo tasujemy 8 kierunków
        dirs_8 = self.directions[:]
        random.shuffle(dirs_8)
        used = set(newp)
        for (dx, dy) in dirs_8:
            nr, nc = r + dx, c + dy
            if 0 <= nr < self.size_x and 0 <= nc < self.size_y:
                if (nr, nc) not in used:
                    newp[idx] = (nr, nc)
                    break
        return newp

    def generate_children(self, mating_pool, offspring_count):
        kids = []
        while len(kids) < offspring_count:
            p1 = random.choice(mating_pool)
            p2 = random.choice(mating_pool)
            if p1 != p2:
                c = self.crossover(p1, p2)
                if self.valid_path(c):
                    kids.append(c)
        return kids

#############################
#  3) Funkcje GA            #
#############################

def run_tsp3d_path_single_robot(
        ga: GeneticTSP3DPath,
        start_2d,
        end_2d,
        pop_size=30,
        num_of_generations=20,
        elite_size=5,
        tournament_size=3,
        offspring_rate=0.5,
        mutation_rate=0.05
):
    """
    Uruchamia algorytm GA (TSP 3D) dla JEDNEGO robota (start->end).
    Zwraca najlepszą znalezioną ścieżkę (listę (r,c)) i jej koszt.
    """
    # t0 = time.time()

    # 1) Inicjalizacja populacji
    population = ga.generate_population(pop_size, tuple(start_2d), tuple(end_2d))

    best = min(population, key=lambda p: ga.distance_path(p))
    best_cost = ga.distance_path(best)
    # init_time = time.time() - t0
    # print(f"Initial best dist={best_cost:.4f} | init_time={init_time:.2f}s")

    # 2) Pętla pokoleń
    total_start = time.time()
    for gen in range(num_of_generations):
        gen_start = time.time()

        # a) Elity
        elites = ga.select_elites(population, elite_size)
        non_elites = [p for p in population if p not in elites]

        # b) rodzice (turniej)
        pool_size = len(population) - elite_size
        parents = ga.create_pool(non_elites, tournament_size, pool_size)
        parents += elites

        # c) dzieci (krzyżowanie)
        num_children = int(len(parents) * offspring_rate)
        children = ga.generate_children(parents, num_children)

        # d) mutacja
        for i in range(len(children)):
            if random.random() < mutation_rate:
                mp = ga.mutate(children[i])
                if ga.valid_path(mp):
                    children[i] = mp
                ga.children_mutated += 1

        # e) nowa populacja
        newpop = elites + children
        if len(newpop) < len(population) and len(non_elites) > 0:
            needed = len(population) - len(newpop)
            newpop += random.sample(non_elites, min(needed, len(non_elites)))
        newpop = newpop[:len(population)]
        population = newpop

        # f) aktualizacja best
        curr = min(population, key=lambda p: ga.distance_path(p))
        curr_cost = ga.distance_path(curr)
        if curr_cost < best_cost:
            best = curr
            best_cost = curr_cost

        gen_time = time.time() - gen_start
        print(f"GEN {gen+1}/{num_of_generations} - best so far={best_cost:.4f}, time={gen_time:.2f} sec")

    total_end = time.time()
    print(f"\nCalkowity czas GA (dla 1 robota): {(total_end - total_start):.2f} sec.")
    return best, best_cost


def run_multi_robot_tsp3d_path(
        terrain,
        starts_2d,
        ends_2d,
        pop_size=30,
        num_of_generations=20,
        elite_size=5,
        tournament_size=3,
        offspring_rate=0.5,
        mutation_rate=0.05
):
    """
    Sekwencyjnie uruchamia GA dla wielu robotów,
    każdy musi unikać kolizji ze ścieżkami zaplanowanymi wcześniej.

    Zwraca listę najlepszych ścieżek [path_robot1, path_robot2, ...].
    """
    # Obiekt GA współdzielony, by reużywać caches i wiedzę o ścieżkach (occupied_paths).
    ga = GeneticTSP3DPath(terrain, occupied_paths=[])

    all_paths = []
    for i, (st, en) in enumerate(zip(starts_2d, ends_2d)):
        print(f"\n=== Planowanie dla robota {i+1}: start={st}, end={en} ===")
        best_path, best_val = run_tsp3d_path_single_robot(
            ga,
            st, en,
            pop_size=pop_size,
            num_of_generations=num_of_generations,
            elite_size=elite_size,
            tournament_size=tournament_size,
            offspring_rate=offspring_rate,
            mutation_rate=mutation_rate
        )
        print(f"Robot {i+1} - best cost={best_val:.4f}")
        print(f"Best path={best_path}\n")

        # Dodaj tę ścieżkę do occupied_paths,
        # aby kolejne roboty unikały kolizji.
        ga.occupied_paths.append(best_path)
        all_paths.append(best_path)

    return all_paths

#############################
#  4) MAIN DEMO             #
#############################

# if __name__ == "__main__":
#
#     # 4 roboty, każdy ma wspólny cel
#     starts = [(5, 10), (20, 0), (0, 30), (1, 1)]
#     ends   = [(48, 49), (48, 49), (48, 49), (48, 49)]
#     starts = [(5, 10),]
#     ends   = [(48, 49),]
#
#     # Teren 51x51 (jak w A*)
#     map_size = (51, 51)
#     terrain = terrain_generator(
#         noise_num=0,
#         terrain_size=map_size,
#         terrain_type="hills"
#     )
#
#     # Parametry GA
#     pop_size = 1000
#     num_of_generations = 10
#     elite_size = 5
#     tournament_size = 3
#     offspring_rate = 0.5
#     mutation_rate = 0.2
#
#     # Uruchamiamy wielorobotowe planowanie
#     final_paths = run_multi_robot_tsp3d_path(
#         terrain,
#         starts,
#         ends,
#         pop_size=pop_size,
#         num_of_generations=num_of_generations,
#         elite_size=elite_size,
#         tournament_size=tournament_size,
#         offspring_rate=offspring_rate,
#         mutation_rate=mutation_rate
#     )
#
#     # Wizualizacja statyczna (wszystkie ścieżki)
#     plot_graphs_static(final_paths, terrain, starts, ends)
#
#     # Wizualizacja animowana (krok-po-kroku)
#     plot_graphs_animation(final_paths, terrain, starts, ends)
