import copy
import random
import math
import time

import numpy as np
import matplotlib

from algorytmy.terrain import terrain_generator

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def plot_graph(best_path, terrain, start, end):
    print(best_path)
    plt.close("all")
    plt.figure(figsize=(5, 5))
    # plt.grid("off")
    # plt.rc("axes", axisbelow=True)
    plt.imshow(
        terrain,
    )

    plt.scatter(end[0], end[1], 100, marker="*", facecolors="k", edgecolors="k")
    plt.scatter(start[0], start[1], 100, marker="o", facecolors="k", edgecolors="k")

    X = [best_path[i][0] for i in range(len(best_path))]
    Y = [best_path[i][1] for i in range(len(best_path))]
    plt.plot(
        X,
        Y,
        "r-",
    )

    for i in range(len(best_path)):
        plt.scatter(
            best_path[i][0],
            best_path[i][1],
            25,
            marker=".",
            facecolors="red",
            edgecolors="face",
        )

    plt.title("Crawler Optimization")
    plt.show()


def loss_function(path, ter):
    cost = 0
    num = 0
    dist_penalty = 0
    for p in path:
        # Kara za odległość od ostatniego punktu
        dist_penalty = np.sqrt((p[0] - path[-1][0]) ** 2 + (p[1] - path[-1][1]) ** 2)

        # koszt terenu + kara za odległość od poprzedniego + długość ścieżki
        cost += ter[p[0]][p[1]] + dist_penalty
    return cost


def calculate_neighbourhood(point, map_size):
    neigh = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            p = [point[0] + i, point[1] + j]

            # Prawidłowy zakres indeksów to [0, map_size[0]) i [0, map_size[1]):
            if (
                0 <= p[0] < map_size[0]
                and 0 <= p[1] < map_size[1]
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
            and n[0] < map_size[0]
            and n[1] < map_size[1]
            and n[0] >= 0
            and n[1] >= 0
        ]

        # Randomly select the next point from valid neighbours
        if valid_neighbours:
            current = random.choice(valid_neighbours)
            # Avoid revisiting points
            if current not in path:
                path.append(current)
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


def fix_neighborhood(path, idx, map_size):
    """Funkcja sprawdzająca i naprawiająca sąsiedztwo wokół zmienionego punktu."""

    def distance(p1, p2):
        """Odległość Manhattan między punktami."""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    original_idx = idx
    original_path = copy.deepcopy(path)
    # Sprawdź punkt przed zmienionym
    if idx > 0:  # Jeśli istnieje punkt przed
        prev_point = path[idx - 1]
        counter = 0
        while path[idx] not in calculate_neighbourhood(path[idx - 1], map_size):
            # Dodaj punkt między `prev_point` a `path[idx]`
            counter += 1
            new_point = min(
                calculate_neighbourhood(path[idx - 1], map_size),
                key=lambda p: distance(p, path[idx]),
            )
            path.insert(idx, new_point)
            idx += 1  # Przesuwamy się, bo wstawiliśmy punkt

    # Sprawdź punkt po zmienionym
    # idx = original_idx  # Przywróć indeks na pierwotną wartość
    if idx < len(path) - 1:  # Jeśli istnieje punkt po
        next_point = path[idx + 1]
        counter = 0
        while next_point not in calculate_neighbourhood(path[idx], map_size):
            # Dodaj punkt między `path[idx]` a `next_point`
            counter += 1
            new_point = min(
                calculate_neighbourhood(path[idx], map_size),
                key=lambda p: distance(p, next_point),
            )
            path.insert(idx + 1, new_point)
            idx += 1  # Przesuwamy się, bo wstawiliśmy punkt

    return path


def cso_step(actual, best, map_size, step=1):
    new_actual = copy.deepcopy(actual)
    idx = 0
    for i in range(1, len(actual)):
        if i >= len(best):
            new_actual.pop(len(best))
        elif actual[i] != best[i]:
            if actual[i][0] < best[i][0] and actual[i][1] < best[i][1]:
                new_actual[i][0] += step
                new_actual[i][1] += step
            elif actual[i][0] < best[i][0] and actual[i][1] == best[i][1]:
                new_actual[i][0] += step
            elif actual[i][0] < best[i][0] and actual[i][1] > best[i][1]:
                new_actual[i][0] += step
                new_actual[i][1] -= step
            elif actual[i][0] == best[i][0] and actual[i][1] < best[i][1]:
                new_actual[i][1] += step
            elif actual[i][0] == best[i][0] and actual[i][1] > best[i][1]:
                new_actual[i][1] -= step
            elif actual[i][0] > best[i][0] and actual[i][1] > best[i][1]:
                new_actual[i][0] -= step
                new_actual[i][1] -= step
            elif actual[i][0] > best[i][0] and actual[i][1] == best[i][1]:
                new_actual[i][0] -= step
            elif actual[i][0] > best[i][0] and actual[i][1] < best[i][1]:
                new_actual[i][0] -= step
                new_actual[i][1] += step
            # Gdy i == len(new_actual) - 1, new_actual[i + 1] wywoła błąd, bo indeks i+1 będzie poza zakresem.
            # Niby mamy break, więc zwykle nie dojdzie do końca listy, ale w rzadkich sytuacjach może się to zdarzyć.
            # Zmieniam na to co niżej
            # if new_actual[i] == new_actual[i - 1]:
            #     if new_actual[i + 1] == new_actual[i - 1]:
            #         new_actual.pop(i + 1)
            #     new_actual.pop(i)
            if i < len(new_actual) - 1:  # Upewniamy się, że i+1 nie przekroczy długości listy
                if new_actual[i] == new_actual[i - 1] or new_actual[i] == new_actual[i + 1]:
                    if new_actual[i + 1] == new_actual[i - 1]:
                        new_actual.pop(i + 1)
                    new_actual.pop(i)
            idx = i
            break
    new_actual = fix_neighborhood(new_actual, idx=idx, map_size=map_size)

    return new_actual


def dispersal(actual, map_size):
    new_actual = copy.deepcopy(actual)
    x = random.randint(1, 10)
    i = random.randint(1, len(actual) - 2)
    if x == 1:
        new = [0, 0]
        while new in new_actual:
            new = [
                random.randint(1, map_size[0] - 1),
                random.randint(1, map_size[1] - 1),
            ]
        new_actual.insert(-1, new)
        new_actual = fix_neighborhood(path=new_actual, idx=-2, map_size=map_size)
    elif x == 2:
        if len(new_actual) > 1:
            new_actual.pop(-2)
            new_actual = fix_neighborhood(path=new_actual, idx=-2, map_size=map_size)
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

    # for i in new_actual:
    #     if (
    #         i[0] > map_size[0]
    #         or i[1] > map_size[1]
    #         or i[0] < map_size[0]  # To zawsze będzie prawda, jeśli i[0] != 100 - Co za tym idzie mamy problem z dyspersją
    #         or i[1] < map_size[1]
    #     ):
    #         return actual
    # return new_actual

    # Jeśli którykolwiek punkt wyjdzie poza [0, map_size[0]) albo [0, map_size[1]),
    # odrzucamy nową ścieżkę (wracamy do 'actual'). W przeciwnym wypadku akceptujemy 'new_actual'.
    for point in new_actual:
        if (
                point[0] < 0
                or point[1] < 0
                or point[0] >= map_size[0]
                or point[1] >= map_size[1]
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
    num_of_iterations: int = 10,
    cockroaches_num: int = 100,
    probability_of_dispersion: float = 10,
    max_step: int = 1,
):
    solutions = []
    best_solution = Solution(None, np.inf)  # path, cost,
    loss_funcion_values_minimums_per_iter = []
    for i in range(cockroaches_num):
        new_path = initial_path(start, end, map_size)
        calc_new = loss_function(new_path, terrain)
        new_sol = Solution(new_path, calc_new)
        solutions.append(new_sol)

        if best_solution.loss_value > calc_new:
            best_solution = new_sol

    # plot_graph(best_solution.path, terrain, start, end)
    pi = None
    pg = best_solution
    pg_list = [pg]

    N = len(solutions)
    for x in range(num_of_iterations):
        print(f"Numer iteracji {x}")
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
                    solutions[sol_i].path = cso_step(
                        copy.deepcopy(solutions[sol_i].path), pg.path, map_size
                    )
            else:
                for _ in range(max_step):
                    solutions[sol_i].path = cso_step(
                        copy.deepcopy(solutions[sol_i].path), pi.path, map_size
                    )

            for sol in solutions:
                sol.loss_value = loss_function(sol.path, terrain)
                if best_solution.loss_value > sol.loss_value:
                    best_solution = sol
            pg_list.append(best_solution)

        # 4 - Dyspersja i ponowne uaktualnienie pg
        # Dyspersja uruchamia się zawsze bo warunek zawsze był prawdziwy - zmieniam na to co niżej
        # generated_number = random.randint(1, 3)
        # if generated_number <= probability_of_dispersion:

        # Poprawny warunek - random.random() zwraca wartość między 0 a 1 - przemnażamy przez 100 bo probability_of_dispersion = 10
        if 100 * random.random() < probability_of_dispersion:
            for disp_i in range(N):
                solutions[disp_i].path = dispersal(solutions[disp_i].path, map_size)

            for sol in solutions:
                sol.loss_value = loss_function(sol.path, terrain)
                if (
                    best_solution.loss_value > sol.loss_value
                    and start in sol.path
                    and end in sol.path
                ):
                    best_solution = sol
            pg_list.append(best_solution)

        k = random.randint(0, N - 1)

        solutions[k] = pg
        pg_list.append(pg)

        for point in best_solution.path:
            best_solution.path = fix_neighborhood(
                best_solution.path,
                idx=best_solution.path.index(point),
                map_size=map_size,
            )
        loss_funcion_values_minimums_per_iter.append(best_solution.loss_value)

    best = pg_list[0]
    for p in pg_list:
        if best.loss_value > p.loss_value:
            best = p
    # print(best_solution)
    # plot_graph(best.path, terrain, start, end)
    # plt.show()
    return best.path, loss_funcion_values_minimums_per_iter


if __name__ == "__main__":
    # while True:
    #     start = [0, 0]
    #     end = [10, 10]
    #     map_size = [20, 20]
    #     terrain = terrain_generator(
    #         terrain_size=map_size, terrain_type="hills", noise_num=0
    #     )
    #
    #     best_path, _ = algorithm(start, end, map_size, terrain, visibility_range=10)

    start = [0, 0]
    end = [40, 40]
    map_size = [50, 50]
    terrain = terrain_generator(
        terrain_size=map_size, terrain_type="hills", noise_num=0
    )

    best_path, _ = algorithm(start, end, map_size, terrain, visibility_range=10)
    print("100% completed!")
    plot_graph(best_path, terrain, start=start, end=end)
    plt.show()
