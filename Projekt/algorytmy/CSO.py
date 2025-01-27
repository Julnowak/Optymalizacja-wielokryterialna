import copy
import random

import numpy as np
import matplotlib

from algorytmy.TSP3D_multi import plot_graphs_animation, plot_graphs_static
from algorytmy.terrain import terrain_generator

matplotlib.use("TkAgg")
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


def generate_neighborhood(point, size, directions, terrain_size):
    # Inicjalizujemy zbiór na sąsiedztwo
    neighborhood = []
    x, y = point
    max_rows, max_cols = terrain_size

    for dx, dy in directions:
        for dist in range(1, size + 1):
            new_x = x + dx * dist
            new_y = y + dy * dist

            # Sprawdzenie, czy nowa pozycja mieści się w granicach mapy terenu
            if 0 <= new_x < max_rows and 0 <= new_y < max_cols:
                neighborhood.append((new_x, new_y))

    return neighborhood


def distance(p1, p2):
    """Odległość Manhattan między punktami."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def loss_function(
    path,
    terrain,
    occupied_positions,
    end,
    robot_distance=2,
    terrain_weight=100,
    robot_distance_weight=1,

):
    cost = 0
    for i in range(len(path) - 1):
        (x1, y1), (x2, y2) = path[i], path[i + 1]
        height_diff = abs(terrain[x2][y2] - terrain[x1][y1]) * terrain_weight * distance(path[i], end)
        cost += height_diff

        occupied_future_positions = []
        for row in occupied_positions:
            for offset in range(
                -robot_distance, robot_distance + 1
            ):  # Uwzględniamy dystans
                index = i + offset
                if 0 <= index < len(row):  # Sprawdzenie, czy indeks jest w zakresie
                    occupied_future_positions.append(row[index])

        neighbors = generate_neighborhood(
            path[i],
            robot_distance,
            [
                (0, 1),
                (1, 0),
                (0, -1),
                (-1, 0),
                (1, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (0, 0),
            ],
            (len(terrain), len(terrain[0])),
        )

        # Jeśli dany ruch prowadzi do zajętej pozycji, nakładamy dużą karę
        if path[i] in occupied_future_positions:
            cost += (
                1000000000 * robot_distance_weight
            )  # Duża kara za kolizję, ale nie nieskończoność

        # Dodatkowa kara za bliskość do zajętych pozycji (im bliżej, tym większa kara)
        for n in neighbors:
            if n in occupied_future_positions:
                cost += (
                    10* robot_distance_weight / max(distance(path[i], n), 1)
                )  # Dynamiczna kara

    return cost


def calculate_neighbourhood(point, map_size):
    neigh = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            p = [point[0] + i, point[1] + j]

            # Prawidłowy zakres indeksów to [0, map_size[0]) i [0, map_size[1]):
            if 0 <= p[0] < map_size[0] and 0 <= p[1] < map_size[1] and p != point:
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
            if abs(n[0] - end[0]) <= abs(current[0] - end[0])
            and abs(n[1] - end[1]) <= abs(current[1] - end[1])
            # and n[0] <= end[0]
            # and n[1] <= end[1]
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


def fix_neighborhood(path, idx, map_size, occupied_positions):
    """Funkcja sprawdzająca i naprawiająca sąsiedztwo wokół zmienionego punktu."""

    original_idx = idx
    original_path = copy.deepcopy(path)
    # Sprawdź punkt przed zmienionym
    if idx > 0:  # Jeśli istnieje punkt przed
        prev_point = path[idx - 1]
        while path[idx] not in calculate_neighbourhood(path[idx - 1], map_size):
            # Dodaj punkt między `prev_point` a `path[idx]`
            neighbourhood = calculate_neighbourhood(path[idx - 1], map_size)
            for neighbour in neighbourhood:
                if is_occupied(
                    point=neighbour, idx=idx, occupied_positions=occupied_positions
                ):
                    neighbourhood.remove(neighbour)
            new_point = min(
                neighbourhood,
                key=lambda p: distance(p, path[idx]),
            )
            path.insert(idx, new_point)
            idx += 1  # Przesuwamy się, bo wstawiliśmy punkt

    # Sprawdź punkt po zmienionym
    # idx = original_idx  # Przywróć indeks na pierwotną wartość
    if idx < len(path) - 1:  # Jeśli istnieje punkt po
        next_point = path[idx + 1]
        while next_point not in calculate_neighbourhood(path[idx], map_size):
            neighbourhood = calculate_neighbourhood(path[idx], map_size)
            for neighbour in neighbourhood:
                if is_occupied(
                    point=neighbour, idx=idx + 1, occupied_positions=occupied_positions
                ):
                    neighbourhood.remove(neighbour)
            new_point = min(
                neighbourhood,
                key=lambda p: distance(p, next_point),
            )
            path.insert(idx + 1, new_point)
            idx += 1  # Przesuwamy się, bo wstawiliśmy punkt

    return path


def bring_point_closer_to_best(point, best_point, step=1):
    new_point = copy.deepcopy(point)
    if point[0] < best_point[0] and point[1] < best_point[1]:
        new_point[0] += step
        new_point[1] += step
    elif point[0] < best_point[0] and point[1] == best_point[1]:
        new_point[0] += step
    elif point[0] < best_point[0] and point[1] > best_point[1]:
        new_point[0] += step
        new_point[1] -= step
    elif point[0] == best_point[0] and point[1] < best_point[1]:
        new_point[1] += step
    elif point[0] == best_point[0] and point[1] > best_point[1]:
        new_point[1] -= step
    elif point[0] > best_point[0] and point[1] > best_point[1]:
        new_point[0] -= step
        new_point[1] -= step
    elif point[0] > best_point[0] and point[1] == best_point[1]:
        new_point[0] -= step
    elif point[0] > best_point[0] and point[1] < best_point[1]:
        new_point[0] -= step
        new_point[1] += step
    return new_point


def is_occupied(point, idx, occupied_positions):
    for path in occupied_positions:
        if not idx >= len(path):
            if point == path[idx]:
                return True
    return False


def cso_step(actual, best, map_size, occupied_positions, step=1):
    new_actual = copy.deepcopy(actual)
    idx = 0
    for i in range(1, len(actual)):
        if i >= len(best):
            new_actual.pop(len(best))
        elif actual[i] != best[i]:
            best_point = copy.deepcopy(best[i])
            new_point = copy.deepcopy(actual[i])
            is_new_point_occupied = True

            while is_new_point_occupied:
                new_point = bring_point_closer_to_best(
                    point=new_point, best_point=best_point
                )

                is_new_point_occupied = is_occupied(
                    point=new_point, idx=i, occupied_positions=occupied_positions
                )
                # Jeśli nowy punkt jest zajęty i jest już punktem z najlepszej ścieżki to trzeba zmienić punkt docelowy bo będzie pętla nieskończona
                if is_new_point_occupied and new_point == best_point:
                    neighbourhood = calculate_neighbourhood(best_point, map_size)
                    for neighbour in neighbourhood:
                        if (
                            is_occupied(
                                point=neighbour,
                                idx=i + 1,
                                occupied_positions=occupied_positions,
                            )
                            or neighbour in best[:i]
                        ):
                            neighbourhood.remove(neighbour)
                    best_point = random.choice(neighbourhood)

            new_actual[i] = new_point

            if (
                i < len(new_actual) - 1
            ):  # Upewniamy się, że i+1 nie przekroczy długości listy
                if (
                    new_actual[i] == new_actual[i - 1]
                    or new_actual[i] == new_actual[i + 1]
                ):
                    if new_actual[i + 1] == new_actual[i - 1]:
                        new_actual.pop(i + 1)
                    new_actual.pop(i)
            idx = i
            break
    new_actual = fix_neighborhood(
        path=new_actual,
        idx=idx,
        map_size=map_size,
        occupied_positions=occupied_positions,
    )

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
        # new_actual = fix_neighborhood(path=new_actual, idx=-2, map_size=map_size)
    elif x == 2:
        if len(new_actual) > 1:
            new_actual.pop(-2)
            # new_actual = fix_neighborhood(path=new_actual, idx=-2, map_size=map_size)
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
    occupied_positions,
    num_of_iterations: int = 10,
    cockroaches_num: int = 10,
    probability_of_dispersion: float = 10,
    max_step: int = 1,
):
    solutions = []
    best_solution = Solution(None, np.inf)  # path, cost,
    loss_funcion_values_minimums_per_iter = []
    for i in range(cockroaches_num):
        new_path = initial_path(start, end, map_size)
        calc_new = loss_function(
            path=new_path, terrain=terrain, end=end, occupied_positions=occupied_positions
        )
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
                        actual=copy.deepcopy(solutions[sol_i].path),
                        best=pg.path,
                        map_size=map_size,
                        occupied_positions=occupied_positions,
                    )
            else:
                for _ in range(max_step):
                    solutions[sol_i].path = cso_step(
                        actual=copy.deepcopy(solutions[sol_i].path),
                        best=pi.path,
                        map_size=map_size,
                        occupied_positions=occupied_positions,
                    )

            for sol in solutions:
                sol.loss_value = loss_function(
                    path=sol.path,
                    terrain=terrain,
                    occupied_positions=occupied_positions,
                    end=end
                )
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
                sol.loss_value = loss_function(
                    path=sol.path,
                    terrain=terrain,
                    occupied_positions=occupied_positions,
                    end=end
                )
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
                occupied_positions=occupied_positions,
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

    # 4 roboty, każdy ma wspólny cel
    starts = [[5, 10], [20, 0], [0, 30], [1, 1]]
    ends = [[48, 49], [48, 49], [48, 49], [48, 49]]

    # Teren 51x51 (jak w A*)
    map_size = (51, 51)
    terrain = terrain_generator(
        noise_num=0, terrain_size=map_size, terrain_type="hills"
    )

    occupied_positions = []
    paths = []

    for start, end in zip(starts, ends):
        result_path, _ = algorithm(
            start=start,
            end=end,
            map_size=map_size,
            terrain=terrain,
            visibility_range=5,
            num_of_iterations=50,
            occupied_positions=occupied_positions,
            cockroaches_num=20
        )
        print("poszło")
        paths.append(result_path)
        occupied_positions.append(result_path)

    # best_path, _ = algorithm(start, end, map_size, terrain, visibility_range=10)
    print("100% completed!")
    # plot_graph(best_path, terrain, start=start, end=end)
    # plt.show()
    plot_graphs_animation(all_paths=paths, terrain=terrain, starts=starts, ends=ends)
    plot_graphs_static(all_paths=paths, terrain=terrain, starts=starts, ends=ends)
