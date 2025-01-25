import random
import math
import copy
import time

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from scipy.spatial.distance import euclidean
from algorytmy.terrain import terrain_generator

#############################
#  1) Wizualizacja          #
#############################

def plot_graph(best_path, terrain, start, end):
    """
    Rysuje 2D mapę `terrain` i nanosi ścieżkę `best_path` (czerwone kropki).
    """
    print("\nBEST PATH:", best_path)
    plt.close("all")
    plt.figure(figsize=(6, 6))
    plt.imshow(terrain, origin='upper', cmap="magma")

    # Rysowanie ścieżki
    X = [p[0] for p in best_path]
    Y = [p[1] for p in best_path]
    plt.plot(X, Y, "ro-")

    # Zaznaczenie start i end
    plt.scatter(end[0], end[1], 100, marker='*', c='k')
    plt.scatter(start[0], start[1], 100, marker='o', c='k')

    plt.title("GA TSP 3D - A* style cost")
    plt.show()


#############################
#  2) Klasa GA TSP 3D Path  #
#############################

class GeneticTSP3DPath:
    """
    GA w stylu 'komiwojażer 3D' + styl A*:
      - siatka NxN,
      - ruch 4-kierunkowy,
      - cost = height_diff * 100 + 1
    """

    def __init__(self, terrain, debug=False):
        self.terrain = terrain
        self.size_x, self.size_y = terrain.shape

        # Bufor dystansów: (p1,p2)->cost
        self.distance_cache = {}
        # Bufor kosztu całej ścieżki: tuple(path)->cost
        self.path_cost_cache = {}

        # Statystyki
        self.invalid_paths = 0
        self.children_mutated = 0

        # Flaga debug (czy drukować info w stylu A*)
        self.debug = debug

    #############################
    #   Obliczanie odległości  #
    #############################

    def distance_3d(self, p1, p2):
        """
        Styl a'la A*:
          cost = (height_diff * 100) + 1
        """
        if p1 > p2:
            key = (p2, p1)
        else:
            key = (p1, p2)

        if key in self.distance_cache:
            return self.distance_cache[key]

        r1, c1 = p1
        r2, c2 = p2
        z1 = self.terrain[r1, c1]
        z2 = self.terrain[r2, c2]
        height_diff = abs(z2 - z1)
        cost = height_diff * 100 + 1

        if self.debug:
            print(f"[distance_3d] PUNKT: {p1} -> {p2} | height_diff={height_diff}, cost={cost}")

        self.distance_cache[key] = cost
        return cost

    def distance_path(self, path):
        """
        Suma costów kolejnych kroków.
        """
        path_key = tuple(path)
        if path_key in self.path_cost_cache:
            return self.path_cost_cache[path_key]

        total_cost = 0.0
        for i in range(len(path)-1):
            total_cost += self.distance_3d(path[i], path[i+1])
        self.path_cost_cache[path_key] = total_cost
        return total_cost

    #############################
    #   Walidacja ścieżki      #
    #############################

    def valid_path(self, path):
        """
        1) Bez duplikatów w środku,
        2) Kazdy krok 4-kier,
        3) W granicach NxN
        """
        if len(path) < 2:
            return False

        inner = path[1:-1]
        if len(inner) != len(set(inner)):
            self.invalid_paths += 1
            return False

        for i in range(len(path)-1):
            r1,c1 = path[i]
            r2,c2 = path[i+1]
            # Krok 4-kier
            if abs(r2-r1)+abs(c2-c1) != 1:
                self.invalid_paths += 1
                return False
            # Granice
            if not (0 <= r2 < self.size_x and 0 <= c2 < self.size_y):
                self.invalid_paths += 1
                return False

        return True

    #############################
    #  Generowanie ścieżek     #
    #############################

    def generate_random_path(self, start, end):
        """
        Budujemy ścieżkę w stylu A*, z pewną losowością:
          - max 2*(Nx+Ny) kroków,
          - z visited,
          - sortujemy sąsiadów wg cost a'la A*, wybieramy w top3.
        """
        max_steps = 2*(self.size_x + self.size_y)
        visited = set([start])
        path = [start]

        current = start
        for step_i in range(max_steps):
            if current == end:
                break
            r,c = current

            # Zbieramy 4-kier.
            neighbors = []
            for (dx,dy) in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr, nc = r+dx, c+dy
                if 0<=nr<self.size_x and 0<=nc<self.size_y:
                    if (nr,nc) not in visited:
                        neighbors.append((nr,nc))

            if self.debug:
                print(f"\n-- step={step_i}, current={current}, neighbors={neighbors}")

            if not neighbors:
                break

            # sortujemy wg cost = height_diff*100 + 1
            # ale nie liczymy precyzyjnie w distance_3d, bo to jest local step
            # => we can replicate the cost
            def local_cost(nr,nc):
                height_diff = abs(self.terrain[nr,nc] - self.terrain[r,c])
                return height_diff*100 + 1

            neighbors.sort(key=lambda n: local_cost(n[0], n[1]))
            top_k = neighbors[:3]
            nxt = random.choice(top_k)

            if self.debug:
                print(f"Wybrane next={nxt} spośród top_k={top_k}, cost={local_cost(nxt[0],nxt[1])}")

            path.append(nxt)
            visited.add(nxt)
            current = nxt

        if path[-1] != end:
            path.append(end)

        return path

    def generate_population(self, pop_size, start, end):
        """
        Tworzymy populację.
        """
        population = []
        seen = set()
        while len(population) < pop_size:
            new_path = self.generate_random_path(start, end)
            keyp = tuple(new_path)
            if keyp not in seen and self.valid_path(new_path):
                population.append(new_path)
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
        Selekcja turniejowa
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
        prefix p1, wklejamy srodki p2 (4-kier, brak duplikatow),
        doklejamy end
        """
        if len(parent1) < 2 or len(parent2) < 2:
            return parent1

        cut = random.randint(1, max(len(parent1)-2,1))
        child = parent1[:cut]
        used = set(child)
        cur = child[-1]
        mid2 = parent2[1:-1]

        for pt in mid2:
            if pt not in used:
                if abs(pt[0]-cur[0]) + abs(pt[1]-cur[1])==1:
                    child.append(pt)
                    used.add(pt)
                    cur=pt

        endp = parent1[-1]
        if child[-1]!=endp:
            child.append(endp)

        return child

    def mutate(self, path):
        """
        Mutacja 1 kroku
        """
        if len(path)<3:
            return path
        newp = path[:]
        idx = random.randint(1, len(path)-2)
        r,c = newp[idx]
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        random.shuffle(dirs)
        used = set(newp)
        for (dx,dy) in dirs:
            nr,nc = r+dx, c+dy
            if 0<=nr<self.size_x and 0<=nc<self.size_y:
                if (nr,nc) not in used:
                    newp[idx] = (nr,nc)
                    break
        return newp

    def generate_children(self, mating_pool, offspring_count):
        kids=[]
        while len(kids)<offspring_count:
            p1 = random.choice(mating_pool)
            p2 = random.choice(mating_pool)
            if p1!=p2:
                c=self.crossover(p1,p2)
                if self.valid_path(c):
                    kids.append(c)
        return kids

#############################
#  3) Funkcja Główna (GA)   #
#############################

def run_tsp3d_path(
    terrain,
    start_2d,
    end_2d,
    pop_size=30,
    num_of_generations=20,
    elite_size=5,
    tournament_size=3,
    offspring_rate=0.5,
    mutation_rate=0.05,
    debug=False
):
    """
    - terrain: mapa 2D (numpy)
    - start_2d, end_2d: (r,c)
    - parametry GA
    - debug: czy wypisywać szczegółowe info
    """
    ga = GeneticTSP3DPath(terrain, debug=debug)
    t0 = time.time()

    # 1) Inicjalizacja populacji
    population = ga.generate_population(pop_size, tuple(start_2d), tuple(end_2d))
    best = min(population, key=lambda p: ga.distance_path(p))
    best_cost = ga.distance_path(best)
    init_time = time.time()-t0
    print(f"Initial best dist={best_cost:.4f} | init_time={init_time:.2f}s")

    # 2) Główna pętla GA
    total_start = time.time()
    for gen in range(num_of_generations):
        gen_start = time.time()

        # a) Elity
        elites = ga.select_elites(population, elite_size)
        non_elites = [p for p in population if p not in elites]

        # b) Mating pool (selekcja turniejowa)
        pool_size = pop_size - elite_size
        parents = ga.create_pool(non_elites, tournament_size, pool_size)
        parents += elites

        # c) Dzieci
        num_children = int(len(parents)*offspring_rate)
        children = ga.generate_children(parents, num_children)

        # d) Mutacja
        for i in range(len(children)):
            if random.random()<mutation_rate:
                mp = ga.mutate(children[i])
                if ga.valid_path(mp):
                    children[i]=mp
                ga.children_mutated+=1

        # e) Nowa populacja
        newpop = elites+children
        if len(newpop)<pop_size and len(non_elites)>0:
            need = pop_size - len(newpop)
            newpop += random.sample(non_elites, min(need,len(non_elites)))
        newpop = newpop[:pop_size]
        population = newpop

        # f) Sprawdzamy nowe best
        curr = min(population, key=lambda p: ga.distance_path(p))
        curr_cost = ga.distance_path(curr)
        if curr_cost<best_cost:
            best=curr
            best_cost=curr_cost

        gen_time = time.time()-gen_start
        print(f"GEN {gen+1}/{num_of_generations} - best so far={best_cost:.4f}, time={gen_time:.2f} sec")

    total_end = time.time()
    print(f"\nCalkowity czas GA: {(total_end - total_start):.2f} sec.")
    return best, best_cost


#############################
#  4) MAIN DEMO             #
#############################

if __name__=="__main__":
    # Parametry
    map_size=(30,30)
    start=[0,0]
    end=[25,27]

    terrain=terrain_generator(
        noise_num=1,
        terrain_size=map_size,
        terrain_type="hills"
    )

    best_path,best_val=run_tsp3d_path(
        terrain,
        start,
        end,
        pop_size=200,             # do testów
        num_of_generations=100,   # do testów
        elite_size=5,
        tournament_size=3,
        offspring_rate=0.5,
        mutation_rate=0.1,
        debug=False               # włącz printy w stylu A*
    )

    print(f"\nDONE. Best cost={best_val:.4f}")
    print("BEST PATH:",best_path)

    plot_graph(best_path, terrain, start, end)
