import heapq
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
#  1) A*  do obliczenia
#############################

def astar_path(terrain, start, goal):
    """
    Zwraca ścieżkę minimalną (listę [(r,c), (r2,c2), ...]) wg cost:
       cost(krawędź) = (|z2 - z1|*100) + 1
    Ruch 4-kierunkowy (prawo,lewo,góra,dół).
    """
    rows, cols = terrain.shape
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic_a(start, goal)}

    # Tylko 4 kierunki
    directions = [(0,1),(1,0),(0,-1),(-1,0)]

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            # odtwarzamy ścieżkę
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        x,y = current
        for dx,dy in directions:
            nx, ny = x+dx, y+dy
            if 0<=nx<rows and 0<=ny<cols:
                # cost krawędzi
                height_diff = abs(terrain[nx,ny] - terrain[x,y])
                edge_cost = height_diff*100 + 1

                tentative_g = g_score[current] + edge_cost
                if (nx,ny) not in g_score or tentative_g < g_score[(nx,ny)]:
                    came_from[(nx,ny)] = current
                    g_score[(nx,ny)] = tentative_g
                    f_score[(nx,ny)] = tentative_g + heuristic_a((nx,ny), goal)
                    heapq.heappush(open_set, (f_score[(nx,ny)], (nx,ny)))

    return None

def heuristic_a(a, b):
    # Manhattan w 2D
    (x1, y1), (x2, y2) = a,b
    return abs(x1-x2) + abs(y1-y2)


#############################
#  2) Wizualizacja
#############################

def plot_graph(best_path, terrain, start, end):
    print("\nBEST PATH:", best_path)
    plt.close("all")
    plt.figure(figsize=(6,6))
    plt.imshow(terrain, origin='upper', cmap="magma")

    # rysujemy czerwoną ścieżkę
    X = [p[0] for p in best_path]
    Y = [p[1] for p in best_path]
    plt.plot(X, Y, 'ro-')

    plt.scatter(end[0], end[1], 80, marker='*', c='k')
    plt.scatter(start[0], start[1], 80, marker='o', c='k')

    plt.title("GA TSP 3D - A* style cost (with A* init)")
    plt.show()


#############################
#  3) Klasa GA TSP 3D
#############################

class GeneticTSP3DPath:
    """
    GA w stylu 'komiwojażer 3D' z cost a'la A*:
      cost(krawędź) = (|z2 - z1|*100)+1
    Ruch 4-kierunkowy.
    """
    def __init__(self, terrain):
        self.terrain = terrain
        self.size_x, self.size_y = terrain.shape

        # cache
        self.distance_cache = {}
        self.path_cache = {}

        self.invalid_paths = 0
        self.children_mutated = 0


    def cost_edge(self, p1, p2):
        """
        cost = (|z2 - z1|*100) + 1
        """
        if p1>p2:
            key=(p2,p1)
        else:
            key=(p1,p2)

        if key in self.distance_cache:
            return self.distance_cache[key]

        r1,c1 = p1
        r2,c2 = p2
        z1 = self.terrain[r1,c1]
        z2 = self.terrain[r2,c2]
        diff = abs(z2 - z1)
        cost = diff*100 + 1
        self.distance_cache[key] = cost
        return cost

    def cost_path(self, path):
        """
        Suma costów krawędzi
        """
        pk = tuple(path)
        if pk in self.path_cache:
            return self.path_cache[pk]
        s=0
        for i in range(len(path)-1):
            s+=self.cost_edge(path[i],path[i+1])
        self.path_cache[pk]=s
        return s

    def valid_path(self, path):
        """
        1) brak duplikatów w srodku
        2) kazdy krok 4-kier
        3) w granicach NxN
        """
        if len(path)<2:
            return False

        mid=path[1:-1]
        if len(mid)!=len(set(mid)):
            self.invalid_paths+=1
            return False

        for i in range(len(path)-1):
            r1,c1=path[i]
            r2,c2=path[i+1]
            if abs(r2-r1)+abs(c2-c1)!=1:
                self.invalid_paths+=1
                return False
            if not(0<=r2<self.size_x and 0<=c2<self.size_y):
                self.invalid_paths+=1
                return False

        return True


    def generate_random_path(self, start, end):
        """
        w razie potrzeby: generujemy 'losową' ścieżkę
        max 2*(Nx+Ny), preferujemy mniejszą roznicę wys.
        (ale tu można bardziej heurystycznie)
        """
        max_steps=2*(self.size_x+self.size_y)
        visited=set([start])
        path=[start]
        curr=start
        for _ in range(max_steps):
            if curr==end:
                break
            r,c=curr
            neigh=[]
            for (dx,dy) in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dx,c+dy
                if 0<=nr<self.size_x and 0<=nc<self.size_y:
                    if (nr,nc) not in visited:
                        neigh.append((nr,nc))
            if not neigh:
                break
            neigh.sort(key=lambda n: self.cost_edge(curr,n))
            top_k=neigh[:3]
            nxt=random.choice(top_k)
            path.append(nxt)
            visited.add(nxt)
            curr=nxt

        if path[-1]!=end:
            path.append(end)
        return path


#############################
#  4) run_tsp3d_path
#############################

def run_tsp3d_path(
    terrain,
    start,
    end,
    pop_size=50,
    generations=50,
    elite_size=5,
    tournament_size=5,
    offspring_rate=0.5,
    mutation_rate=0.1
):
    ga = GeneticTSP3DPath(terrain)

    # 1) Tworzymy populację
    #    -> w tym momencie wstawiamy do populacji
    #       a) scieżkę z A*, b) scieżki losowe
    population=[]
    # a) scieżka z A*
    astar_sol = astar_path(terrain, tuple(start), tuple(end))
    if astar_sol:
        population.append(astar_sol)
    # b) generuj resztę losowo
    while len(population)<pop_size:
        newp=ga.generate_random_path(tuple(start), tuple(end))
        if ga.valid_path(newp):
            population.append(newp)

    # sprawdzamy best
    best=min(population, key=lambda p: ga.cost_path(p))
    best_cost=ga.cost_path(best)
    print(f"init best={best_cost:.4f}")

    # 2) pętla GA
    t0=time.time()
    for gen in range(generations):
        # a) elity
        scored=[(p, ga.cost_path(p)) for p in population]
        scored.sort(key=lambda x: x[1])
        elites=[s[0] for s in scored[:elite_size]]
        non_elites=[s[0] for s in scored[elite_size:]]

        # b) mating pool
        mating=[]
        pop_copy=non_elites[:]
        while len(mating)<(pop_size-elite_size) and len(pop_copy)>=tournament_size:
            cands=random.sample(pop_copy,tournament_size)
            bestcand=min(cands,key=lambda x:ga.cost_path(x))
            mating.append(bestcand)
            pop_copy.remove(bestcand)
        mating+=elites

        # c) dzieci
        num_children=int(len(mating)*offspring_rate)
        children=[]
        while len(children)<num_children:
            p1=random.choice(mating)
            p2=random.choice(mating)
            if p1!=p2:
                c=ga_crossover(p1,p2, ga)
                if ga.valid_path(c):
                    children.append(c)

        # d) mutacja
        for i in range(len(children)):
            if random.random()<mutation_rate:
                mp=ga_mutate(children[i],ga)
                if ga.valid_path(mp):
                    children[i]=mp
                ga.children_mutated+=1

        # e) nowa populacja
        newpop=elites+children
        if len(newpop)<pop_size and len(non_elites)>0:
            need=pop_size-len(newpop)
            newpop+=random.sample(non_elites, min(need,len(non_elites)))
        newpop=newpop[:pop_size]
        population=newpop

        # f) best
        curr_best=min(population,key=lambda p: ga.cost_path(p))
        curr_cost=ga.cost_path(curr_best)
        if curr_cost<best_cost:
            best=curr_best
            best_cost=curr_cost
        print(f"GEN {gen+1}/{generations} best so far={best_cost:.4f}")

    print(f"\nCzas: {time.time()-t0:.2f}s")
    return best, best_cost

#############################
# Dodatkowe funkcje GA
#############################

def ga_crossover(parent1, parent2, ga):
    """
    Podobny do Twojego crossover:
     - prefix z p1
     - wklejamy srodki p2 (omijamy duplikaty, sprawdz. 4-kier)
    """
    if len(parent1)<2 or len(parent2)<2:
        return parent1

    cut=random.randint(1,max(len(parent1)-2,1))
    child=parent1[:cut]
    used=set(child)
    cur=child[-1]
    # srodek p2
    mid2=parent2[1:-1]
    for pt in mid2:
        if pt not in used:
            if abs(pt[0]-cur[0])+abs(pt[1]-cur[1])==1:
                child.append(pt)
                used.add(pt)
                cur=pt
    endp=parent1[-1]
    if child[-1]!=endp:
        child.append(endp)
    return child

def ga_mutate(path, ga):
    """
    Zmieniamy 1 punkt (poza start/end) na sąsiada 4-kier.
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
        if 0<=nr<ga.size_x and 0<=nc<ga.size_y:
            if (nr,nc) not in used:
                newp[idx]=(nr,nc)
                break
    return newp


#############################
#  MAIN DEMO
#############################

if __name__=="__main__":
    map_size=(30,30)
    start=(0,0)
    end=(25,27)

    terrain=terrain_generator(
        noise_num=1,
        terrain_size=map_size,
        terrain_type="hills"
    )

    best_path,best_cost=run_tsp3d_path(
        terrain,
        start,
        end,
        pop_size=200,
        generations=100,
        elite_size=5,
        tournament_size=5,
        offspring_rate=0.5,
        mutation_rate=0.3
    )

    print(f"\nBEST COST={best_cost:.4f}")
    print("BEST PATH:", best_path)
    plot_graph(best_path, terrain, start, end)
