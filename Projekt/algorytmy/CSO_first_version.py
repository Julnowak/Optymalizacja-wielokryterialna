import random
import math
import time

import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from terrain import terrain_generator


def plot_graph(best_path):
    plt.close("all")
    plt.figure(figsize=(5, 5))
    # plt.grid("off")
    # plt.rc("axes", axisbelow=True)
    plt.imshow(
        terrain,
    )

    X = [best_path[i][0] for i in range(len(best_path))]
    Y = [best_path[i][1] for i in range(len(best_path))]
    plt.plot(
        X,
        Y,
        "ro-",
    )

    for i in range(len(best_path)):
        plt.scatter(
            best_path[i][0],
            best_path[i][1],
            25,
            marker=".",
            facecolors="blue",
            edgecolors="face",
        )
    plt.scatter(end[0], end[1], 100, marker="*", facecolors="k", edgecolors="k")
    plt.scatter(start[0], start[1], 100, marker="o", facecolors="k", edgecolors="k")
    plt.title("Crawler Optimization")


# def loss_function(path, ter):
#     cost = 0
#     for p in path:
#         cost += ter[p[0]][p[1]] * 100
#     return cost


def loss_function(path, ter):
    cost = 0
    num = 0
    dist_penalty = 0
    p_last = None
    for p in path:
        if num != 0:
            dist_penalty = np.sqrt((p[0] - p_last[0]) ** 2 + (p[1] - p_last[1]) ** 2)
        p_last = p
        cost += ter[p[0]][p[1]] * 100 + dist_penalty * 200000
    return cost


def calculate_neighbourhood(point, map_size):
    neigh = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            p = [point[0] + i, point[1] + j]
            if (
                p[0] >= 0
                and p[1] >= 0
                and p[0] <= map_size[0]
                and p[1] <= map_size[1]
                and p != point
            ):
                neigh.append(p)
    return neigh


def initial_path(start, end, map_size):
    # Initialize the path with the start point
    path = [start]

    # Current point starts at the beginning
    current = start

    while end != current:
        # Get all valid neighbours of the current point
        neighbours = calculate_neighbourhood(current, map_size)
        # Filter neighbours to ensure movement towards the end point
        valid_neighbours = [
            n
            for n in neighbours
            if n[0] >= current[0]
            and n[1] >= current[1]
            and n[0] <= end[0]
            and n[1] <= end[1]
        ]

        # Randomly select the next point from valid neighbours
        if valid_neighbours:
            current = random.choice(valid_neighbours)
            # Avoid revisiting points
            if current not in path:
                path.append(current)
    path.append(end)
    return path


def count_fits(large):
    counter = 0
    actual = large.copy()
    # pełne
    while actual[0] != 0 and actual[1] != 0:
        # Oblicz ile razy mniejszy prostokąt zmieści się w dużym wzdłuż każdej os
        actual[0] -= 1
        actual[1] -= 1
        counter += 1

    # reszty
    if actual[0] != 0:
        counter += actual[0]
    elif actual[1] != 0:
        counter += actual[1]

    # Zwróć całkowitą liczbę mniejszych prostokątów
    return counter


def step_distance(p1, p2):
    suma = 0
    if len(p1) < len(p2):
        for i in range(len(p2)):
            if i < len(p1):
                n = [np.abs(p1[i][0] - p2[i][0]), np.abs(p1[i][1] - p2[i][1])]
            else:
                n = [np.abs(0 - p2[i][0]), np.abs(0 - p2[i][1])]
            suma += count_fits(n)

    elif len(p2) < len(p1):
        for i in range(len(p1)):
            if i < len(p2):
                n = [np.abs(p1[i][0] - p2[i][0]), np.abs(p1[i][1] - p2[i][1])]
            else:
                n = [np.abs(p1[i][0] - 0), np.abs(p1[i][1] - 0)]
            suma += count_fits(n)
    else:
        for i in range(len(p1)):
            n = [np.abs(p1[i][0] - p2[i][0]), np.abs(p1[i][1] - p2[i][1])]
            suma += count_fits(n)

    return suma


def cso_step(actual, best):
    new_actual = actual.copy()
    print(new_actual)
    if len(actual) < len(best):
        new_actual.append(best[-1])
    elif len(best) < len(actual):
        new_actual.pop(-1)
    else:
        for i in range(len(actual)):
            if actual[i] != best[i]:
                if actual[i][0] < best[i][0] and actual[i][1] < best[i][1]:
                    new_actual[i][0] += 1
                    new_actual[i][1] += 1
                elif actual[i][0] < best[i][0] and actual[i][1] == best[i][1]:
                    new_actual[i][0] += 1
                elif actual[i][0] < best[i][0] and actual[i][1] > best[i][1]:
                    new_actual[i][0] += 1
                    new_actual[i][0] -= 1
                elif actual[i][0] == best[i][0] and actual[i][1] < best[i][1]:
                    new_actual[i][1] += 1
                elif actual[i][0] == best[i][0] and actual[i][1] > best[i][1]:
                    new_actual[i][1] -= 1
                elif actual[i][0] > best[i][0] and actual[i][1] > best[i][1]:
                    new_actual[i][0] -= 1
                    new_actual[i][1] -= 1
                elif actual[i][0] > best[i][0] and actual[i][1] == best[i][1]:
                    new_actual[i][0] -= 1
                elif actual[i][0] > best[i][0] and actual[i][1] < best[i][1]:
                    new_actual[i][0] -= 1
                    new_actual[i][0] += 1
                break
    return new_actual


def dispersal(actual, map_size):
    new_actual = actual.copy()
    x = random.randint(1, 10)
    i = random.randint(0, len(actual) - 1)
    if x == 1:
        new = new_actual[0]
        while new in new_actual:
            new = [
                random.randint(1, map_size[0] - 1),
                random.randint(1, map_size[1] - 1),
            ]
        new_actual.append(new)
    elif x == 2:
        if len(new_actual) > 1:
            new_actual.pop()
    else:
        addon = 1
        if x == 3:
            new_actual[i][0] += addon if new_actual[i][0] < map_size[0] else 0
            new_actual[i][1] += addon if new_actual[i][1] < map_size[1] else 0
        elif x == 4:
            new_actual[i][0] += addon if new_actual[i][0] < map_size[0] else 0
        elif x == 5:
            new_actual[i][0] += addon if new_actual[i][0] < map_size[0] else 0
            new_actual[i][1] -= addon if new_actual[i][1] > 0 else 0
        elif x == 6:
            new_actual[i][1] += addon if new_actual[i][1] < map_size[1] else 0
        elif x == 7:
            new_actual[i][1] -= addon if new_actual[i][1] > 0 else 0
        elif x == 8:
            new_actual[i][0] -= addon if new_actual[i][0] > 0 else 0
            new_actual[i][1] -= addon if new_actual[i][1] > 0 else 0
        elif x == 9:
            new_actual[i][0] -= addon if new_actual[i][0] > 0 else 0
        elif x == 10:
            new_actual[i][0] -= addon if new_actual[i][0] > 0 else 0
            new_actual[i][1] += addon if new_actual[i][1] < map_size[1] else 0

    for i in new_actual:
        if (
            i[0] > map_size[0]
            or i[1] > map_size[1]
            or i[0] < map_size[0]
            or i[1] < map_size[1]
        ):
            return actual
    return new_actual


class Solution:
    def __init__(self, path, loss_value):
        self.path = path
        self.loss_value = loss_value


def algorithm(
    start,
    end,
    map_size,
    terrain,
    visibility_range,
    num_of_iterations: int = 100,
    cockroaches_num: int = 20,
    probability_of_dispersion: float = 10,
    max_step: int = 1,
):
    solutions = []
    best_solution = Solution(None, np.inf)  # path, cost,
    for i in range(cockroaches_num):
        new_path = initial_path(start, end, map_size)
        calc_new = loss_function(new_path, terrain)
        new_sol = Solution(new_path, calc_new)
        solutions.append(new_sol)

        if best_solution.loss_value > calc_new:
            best_solution = new_sol

    pi = None
    pg = best_solution
    pg_list = [pg]

    N = len(solutions)
    for _ in range(num_of_iterations):
        # 2 - Znalezienie minimum lokalnego i globalnego
        for sol_i in range(N):
            pi = solutions[sol_i]
            for sol_j in range(N):
                if (
                    0
                    < step_distance(solutions[sol_i].path, solutions[sol_j].path)
                    <= visibility_range
                    and solutions[sol_j].loss_value < solutions[sol_i].loss_value
                ):
                    pi = solutions[sol_j]

            # 3 - Implementacja ruchu roju oraz ponowne uaktualnienie pg
            if pi is solutions[sol_i]:
                for _ in range(max_step):
                    solutions[sol_i].path = cso_step(solutions[sol_i].path, pg.path)
            else:
                for _ in range(max_step):
                    solutions[sol_i].path = cso_step(solutions[sol_i].path, pi.path)

            for sol in solutions:
                sol.loss_value = loss_function(sol.path, terrain)
                if best_solution.loss_value > sol.loss_value:
                    best_solution = sol
            pg_list.append(best_solution)

        # 4 - Dyspersja i ponowne uaktualnienie pg
        # generated_number = random.randint(1, 100)
        # if generated_number <= probability_of_dispersion:
        #     for disp_i in range(N):
        #         solutions[disp_i].path = dispersal(solutions[disp_i].path, map_size)
        #
        #     for sol in solutions:
        #         sol.loss_value = loss_function(sol.path, terrain)
        #         if best_solution.loss_value > sol.loss_value:
        #             best_solution = sol
        #     pg_list.append(best_solution)

        k = random.randint(0, N - 1)

        solutions[k] = pg
        pg_list.append(pg)

        # 4 - Dyspersja i ponowne uaktualnienie pg
    best = pg_list[0]
    for p in pg_list:
        if best.loss_value > p.loss_value:
            best = p
    print(best_solution)
    return best.path


if __name__ == "__main__":
    start = [0, 0]
    end = [19, 19]
    map_size = [20, 20]
    terrain = terrain_generator(terrain_size=map_size)

    best_path = algorithm(start, end, map_size, terrain, visibility_range=10)

    #     particle_swarm_optimization(
    #     max_iterations=1000,
    #     swarm_size=20,
    #     inertia=0.5,
    #     c1=0.5,
    #     c2=1,
    #     grid_size=GRID_SIZE
    # )
    print("100% completed!")
    plot_graph(best_path)
    plt.show()
