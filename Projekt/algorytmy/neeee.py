import random

from algorytmy.TSP3D_multi import GeneticTSP3DPath, run_tsp3d_path_single_robot, plot_graphs_static
from algorytmy.terrain import terrain_generator


class GeneticTSP3DPathPareto:

    def __init__(self, terrain, occupied_paths=None, robot_distance=1):
        self.terrain = terrain
        self.size_x, self.size_y = terrain.shape
        self.robot_distance = robot_distance
        self.cost_cache = {}
        self.path_cost_cache = {}
        self.invalid_paths = 0
        self.children_mutated = 0
        self.occupied_paths = occupied_paths if occupied_paths else []
        self.collision_penalty = 1e10
        self.directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

    def heuristic(self, a, b):
        (x1, y1), (x2, y2) = a, b
        return abs(x1 - x2) + abs(y1 - y2)

    def distance_path(self, path):
        cost_elevation = sum(
            abs(self.terrain[path[i][0]][path[i][1]] - self.terrain[path[i - 1][0]][path[i - 1][1]])
            for i in range(1, len(path))
        )
        cost_distance = sum(self.heuristic(path[i], path[i - 1]) for i in range(1, len(path)))
        return cost_elevation, cost_distance

    def valid_path(self, path):
        if len(path) < 2:
            return False
        mid = path[1:-1]
        if len(mid) != len(set(mid)):
            self.invalid_paths += 1
            return False
        for i in range(len(path) - 1):
            dr, dc = path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]
            if (dr, dc) not in self.directions:
                return False
            if not (0 <= path[i + 1][0] < self.size_x and 0 <= path[i + 1][1] < self.size_y):
                return False
        return True

    def generate_random_path(self, start, end):
        max_steps = 2 * (self.size_x + self.size_y)
        path = [start]
        current = start
        for _ in range(max_steps):
            if current == end:
                break
            neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in self.directions]
            neighbors = [p for p in neighbors if 0 <= p[0] < self.size_x and 0 <= p[1] < self.size_y and p not in path]
            if not neighbors:
                break
            neighbors.sort(key=lambda p: self.heuristic(p, end))
            current = random.choice(neighbors[:3])
            path.append(current)
        if path[-1] != end:
            path.append(end)
        return path

    def generate_population(self, pop_size, start, end):
        population = []
        while len(population) < pop_size:
            new_path = self.generate_random_path(start, end)
            if self.valid_path(new_path):
                population.append(new_path)
        return population

    def pareto_dominates(self, p1, p2):
        return all(x <= y for x, y in zip(p1, p2)) and any(x < y for x, y in zip(p1, p2))

    def pareto_front(self, population):
        pareto_front = []
        for path in population:
            cost = self.distance_path(path)
            if not any(self.pareto_dominates(other_cost, cost) for other_cost in pareto_front):
                pareto_front.append(cost)
        return pareto_front

    def select_elites(self, population, elite_size):
        pareto = self.pareto_front(population)
        return sorted(population, key=lambda p: self.distance_path(p))[:elite_size]

    def crossover(self, parent1, parent2):
        split = len(parent1) // 2
        child = parent1[:split] + [p for p in parent2 if p not in parent1[:split]]
        return child

    def mutate(self, path):
        idx = random.randint(1, len(path) - 2)
        r, c = path[idx]
        dirs_8 = self.directions[:]
        random.shuffle(dirs_8)
        for dx, dy in dirs_8:
            nr, nc = r + dx, c + dy
            if 0 <= nr < self.size_x and 0 <= nc < self.size_y and (nr, nc) not in path:
                path[idx] = (nr, nc)
                break
        return path

    def run_algorithm(self, start, end, pop_size=30, generations=20, elite_size=5, mutation_rate=0.05):
        population = self.generate_population(pop_size, start, end)
        best_path = min(population, key=lambda p: self.distance_path(p))
        for _ in range(generations):
            elites = self.select_elites(population, elite_size)
            offspring = [self.crossover(random.choice(elites), random.choice(elites)) for _ in
                         range(pop_size - elite_size)]
            offspring = [self.mutate(child) if random.random() < mutation_rate else child for child in offspring]
            population = elites + offspring
            best_path = min(population, key=lambda p: self.distance_path(p))
        return best_path, self.distance_path(best_path)

import numpy as np
import random

# Inicjalizacja terenu
terrain = terrain_generator(
        noise_num=0,
        terrain_size=[50,50],
        terrain_type="hills"
    )

# Inicjalizacja klasy
pathfinder = GeneticTSP3DPath(terrain)

# Ustawienia
start_points = [(0, 0), (5, 5)]
end_points = [(40, 40), (40, 40),(40, 40), (40, 40)]
pop_size = 50
num_of_generations = 30
elite_size = 10
tournament_size = 5
offspring_rate = 0.6
mutation_rate = 0.1

# Uruchomienie algorytmu dla wielu robotów
solutions = []
paths = []
for start, end in zip(start_points, end_points):
    best_path, cost_list = run_tsp3d_path_single_robot(
        pathfinder, start, end, pop_size, num_of_generations, elite_size, tournament_size, offspring_rate, mutation_rate
    )
    solutions.append((best_path, cost_list))

    paths.append(best_path)

plot_graphs_static(paths, terrain, start_points, end_points)


# Wypisanie wyników
for idx, (path, cost) in enumerate(solutions):
    print(f"Robot {idx + 1}: Najlepsza ścieżka = {path}")
    print(f"Robot {idx + 1}: Koszt ścieżki = {cost[-1]}")
