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
    Rysuje 2D mapę 'terrain' i nanosi ścieżkę 'best_path' czerwonymi kropkami.
    best_path: lista [(x,y), (x2,y2), ...].
    start, end: [x,y].
    """
    print("\nBEST PATH:", best_path)
    plt.close("all")
    plt.figure(figsize=(6,6))
    plt.imshow(terrain, origin='upper', cmap="magma")

    # Rysowanie ścieżki
    X = [p[0] for p in best_path]
    Y = [p[1] for p in best_path]
    plt.plot(X, Y, 'ro-', linewidth=2)

    # Zaznaczenie start i end
    plt.scatter(end[0], end[1], 100, marker='*', c='k')
    plt.scatter(start[0], start[1], 100, marker='o', c='k')
    plt.title("GA TSP 3D - optimized init")
    plt.show()


#############################
#  2) Klasa GA TSP 3D Path  #
#############################

class GeneticTSP3DPath:
    """
    GA w stylu 'komiwojażer 3D':
      - siatka NxN, miasta = piksele
      - ruch 4-kierunkowy
      - funkcja celu: euklides 3D (x,y,z)
    """

    def __init__(self, terrain):
        self.terrain = terrain
        self.size_x, self.size_y = terrain.shape

        # Buforowanie dystansów (p1, p2) -> dystans
        self.distance_cache = {}
        # Buforowanie kosztów całych ścieżek (tuple(path)) -> cost
        self.path_cost_cache = {}

        # statystyki
        self.invalid_paths = 0
        self.children_mutated = 0


    #############################
    #   Obliczanie odległości  #
    #############################

    def distance_3d(self, p1, p2):
        """
        euklides w 3D
        p1=(r1,c1), p2=(r2,c2)
        z1=terrain[r1,c1], z2=terrain[r2,c2]
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
        dist = euclidean((r1, c1, z1), (r2, c2, z2))
        self.distance_cache[key] = dist
        return dist

    def distance_path(self, path):
        """
        suma dystansów 3D kolejnych punktów
        """
        key = tuple(path)
        if key in self.path_cost_cache:
            return self.path_cost_cache[key]

        cost = 0.0
        for i in range(len(path)-1):
            cost += self.distance_3d(path[i], path[i+1])
        self.path_cost_cache[key] = cost
        return cost


    #############################
    #   Walidacja ścieżki      #
    #############################

    def valid_path(self, path):
        """
        Sprawdzamy:
          1) brak duplikatów w środku
          2) kazdy krok 4-kier.
          3) w granicach NxN
        """
        if len(path)<2:
            return False

        # brak duplikatów w środku
        mid = path[1:-1]
        if len(mid)!=len(set(mid)):
            self.invalid_paths+=1
            return False

        for i in range(len(path)-1):
            r1,c1 = path[i]
            r2,c2 = path[i+1]
            if abs(r2-r1)+abs(c2-c1)!=1:
                self.invalid_paths+=1
                return False
            if not(0<=r2<self.size_x and 0<=c2<self.size_y):
                self.invalid_paths+=1
                return False

        return True


    #############################
    #  Generowanie ścieżek     #
    #############################

    def generate_random_path(self, start, end):
        """
        Tworzymy ścieżkę 4-kier. z preferencją w kierunku end,
        ale nie w 100% deterministyczną.

        1) start
        2) max 2*(Nx+Ny) kroków
        3) w kazdym kroku zbieramy sasiadow 4-kier,
           odrzucamy odwiedzone -> visited
           losowo wybieramy z cześci w stronę end i los.
        4) na koniec dodaj end
        """
        max_steps = 2*(self.size_x + self.size_y)
        visited = set()
        visited.add(start)
        path = [start]

        current = start
        for _ in range(max_steps):
            if current==end:
                break
            r,c = current

            # generowanie 4 sasiadow
            neighbors = []
            for (dx,dy) in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc = r+dx, c+dy
                if 0<=nr<self.size_x and 0<=nc<self.size_y:
                    if (nr,nc) not in visited:
                        neighbors.append((nr,nc))

            if not neighbors:
                break

            # sortujemy wg euklides do end, ale wybieramy z wierzchu i +/- los
            # zachowa troche chaosu, troche preferencji
            neighbors.sort(key=lambda x: abs(x[0]-end[0]) + abs(x[1]-end[1]))
            # weź np. 3 najlepszych do end (lub mniej, jak jest)
            top_k = neighbors[:3]
            nextp = random.choice(top_k)

            path.append(nextp)
            visited.add(nextp)
            current=nextp

        if path[-1]!=end:
            path.append(end)

        return path


    def generate_population(self, pop_size, start, end):
        """
        Tworzymy populację, finalnie sprawdzamy valid_path,
        jeśli ok, dodajemy do populacji
        """
        population = []
        seen = set()

        while len(population)<pop_size:
            new_path = self.generate_random_path(start,end)
            keyp = tuple(new_path)
            if keyp not in seen and self.valid_path(new_path):
                population.append(new_path)
                seen.add(keyp)

        return population

    #############################
    #   Selekcja i krzyżowanie #
    #############################

    def select_elites(self, population, elite_size):
        scored = [(p,self.distance_path(p)) for p in population]
        scored.sort(key=lambda x:x[1])
        return [s[0] for s in scored[:elite_size]]

    def create_pool(self, population, tournament_size, pool_size):
        """
        selekcja turniejowa
        """
        mating_pool = []
        pop_copy = population[:]
        while len(mating_pool)<pool_size and len(pop_copy)>=tournament_size:
            cands = random.sample(pop_copy, tournament_size)
            best_cand = min(cands, key=lambda x: self.distance_path(x))
            mating_pool.append(best_cand)
            pop_copy.remove(best_cand)
        return mating_pool

    def crossover(self, parent1, parent2):
        """
        Bierzemy prefix p1, wklejamy srodki p2 (jesli pasuja 4-kier i brak duplikatow),
        doklejamy end
        """
        if len(parent1)<2 or len(parent2)<2:
            return parent1

        cut=random.randint(1,max(len(parent1)-2,1))
        child=parent1[:cut]
        used=set(child)
        cur=child[-1]
        # srodek p2
        middle=parent2[1:-1]
        for pt in middle:
            if pt not in used:
                # sprawdz 4-kier
                if abs(pt[0]-cur[0]) + abs(pt[1]-cur[1])==1:
                    child.append(pt)
                    used.add(pt)
                    cur=pt

        endp=parent1[-1]
        if child[-1]!=endp:
            child.append(endp)

        return child

    def mutate(self, path):
        """
        Mutacja 1 kroku
        """
        if len(path)<3:
            return path
        newp=path[:]
        idx=random.randint(1,len(newp)-2)
        r,c=newp[idx]
        dirs=[(1,0),(-1,0),(0,1),(0,-1)]
        random.shuffle(dirs)
        used=set(newp)
        for (dx,dy) in dirs:
            nr,nc=r+dx,c+dy
            if 0<=nr<self.size_x and 0<=nc<self.size_y:
                # unikaj duplikatow
                if (nr,nc) not in used:
                    newp[idx]=(nr,nc)
                    break
        return newp

    def generate_children(self, mating_pool, offspring_count):
        kids=[]
        while len(kids)<offspring_count:
            p1=random.choice(mating_pool)
            p2=random.choice(mating_pool)
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
    mutation_rate=0.05
):
    ga=GeneticTSP3DPath(terrain)
    t0=time.time()

    # 1) Inicjalizacja
    population=ga.generate_population(pop_size, tuple(start_2d), tuple(end_2d))
    best=min(population,key=lambda p: ga.distance_path(p))
    best_cost=ga.distance_path(best)
    init_time=time.time()-t0
    print(f"Initial best dist={best_cost:.4f} | init_time={init_time:.2f}s")

    # 2) pętla
    total_start=time.time()
    for gen in range(num_of_generations):
        gen_start=time.time()

        # a) Elity
        elites=ga.select_elites(population, elite_size)
        non_elites=[p for p in population if p not in elites]

        # b) rodzice (turniej)
        pool_size=pop_size-elite_size
        parents=ga.create_pool(non_elites,tournament_size,pool_size)
        parents+=elites

        # c) dzieci
        num_children=int(len(parents)*offspring_rate)
        children=ga.generate_children(parents,num_children)

        # d) mutacja
        for i in range(len(children)):
            if random.random()<mutation_rate:
                mp=ga.mutate(children[i])
                if ga.valid_path(mp):
                    children[i]=mp
                ga.children_mutated+=1

        # e) nowa populacja
        newpop=elites+children
        if len(newpop)<pop_size and len(non_elites)>0:
            needed=pop_size-len(newpop)
            newpop+=random.sample(non_elites, min(needed,len(non_elites)))
        newpop=newpop[:pop_size]
        population=newpop

        # f) aktualizacja best
        curr=min(population, key=lambda p: ga.distance_path(p))
        curr_cost=ga.distance_path(curr)
        if curr_cost<best_cost:
            best=curr
            best_cost=curr_cost

        gen_time=time.time()-gen_start
        print(f"GEN {gen+1}/{num_of_generations} - best so far={best_cost:.4f}, time={gen_time:.2f} sec")

    total_end=time.time()
    print(f"\nCalkowity czas GA: {(total_end-total_start):.2f} sec.")
    return best,best_cost


#############################
#  4) MAIN DEMO             #
#############################

if __name__=="__main__":
    map_size=(30,30)
    start=[0,0]
    end=[25, 27]

    terrain=terrain_generator(
        noise_num=0,
        terrain_size=map_size,
        terrain_type="hills"
    )

    best_path,best_val=run_tsp3d_path(
        terrain,
        start,
        end,
        pop_size=200,          # do testów
        num_of_generations=1000,
        elite_size=5,
        tournament_size=3,
        offspring_rate=0.5,
        mutation_rate=0.3
    )

    print(f"\nDONE. Best cost={best_val:.4f}")
    print("BEST PATH:",best_path)

    plot_graph(best_path, terrain, start, end)
