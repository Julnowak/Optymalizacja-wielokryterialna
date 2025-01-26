import heapq
import matplotlib.pyplot as plt
import numpy as np

from algorytmy.terrain import terrain_generator


def plot_graph(paths, terrain, starts, goal):
    plt.close("all")
    plt.figure(figsize=(5, 5))
    plt.imshow(terrain)

    colors = ["red", "blue", "orange", "yellow", "magenta"]

    for i, path in enumerate(paths):
        for point in path:
            plt.scatter(point[1], point[0], 25, marker=".", facecolors=colors[i % len(colors)], edgecolors="face")

    plt.scatter(goal[1], goal[0], 100, marker="*", facecolors="k", edgecolors="k")
    for start in starts:
        plt.scatter(start[1], start[0], 100, marker="o", facecolors="k", edgecolors="k")

    plt.title("Multi-Robot Pathfinding")
    plt.show()


import matplotlib.animation as animation


def plot_graph_animation(paths, terrain, starts, goal):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(terrain)

    colors = ["red", "blue", "orange", "yellow", "magenta"]

    # Utwórz pustą listę, w której będziemy przechowywać obiekty scatter
    scatter_plots = []

    # Stwórz punkt docelowy
    ax.scatter(goal[1], goal[0], 100, marker="*", facecolors="k", edgecolors="k")

    # Stwórz punkty startowe
    for start in starts:
        ax.scatter(start[1], start[0], 100, marker="o", facecolors="k", edgecolors="k")

    # Przygotowanie do animacji: będziemy stopniowo rysować punkty z każdej trasy
    def update(frame):
        ax.clear()
        ax.imshow(terrain)  # Wyświetl teren na nowo

        # Rysowanie punktów z poprzednich tras (dla animacji, aby były widoczne na każdym etapie)
        for i, path in enumerate(paths):
            if frame < len(path):
                point = path[frame]
                ax.scatter(point[1], point[0], 25, marker=".", facecolors=colors[i % len(colors)], edgecolors="face")

        # Ponownie rysowanie punktu docelowego i początkowych
        ax.scatter(goal[1], goal[0], 100, marker="*", facecolors="k", edgecolors="k")
        for start in starts:
            ax.scatter(start[1], start[0], 100, marker="o", facecolors="k", edgecolors="k")

        ax.set_title("Multi-Robot Pathfinding")

    # Liczba klatek animacji (na podstawie najdłuższej ścieżki)
    max_frames = max(len(path) for path in paths)

    ani = animation.FuncAnimation(fig, update, frames=max_frames, repeat=False)

    plt.show()



# Funkcja heurystyczna (odległość Manhattan)
def heuristic(a, b):
    (x1, y1), (x2, y2) = a, b
    return abs(x1 - x2) + abs(y1 - y2)


def generate_neighborhood(point, size, directions):
    # Inicjalizujemy zbiór na sąsiedztwo
    neighborhood = []

    x, y = point

    # Iterujemy po wszystkich kierunkach
    for dx, dy in directions:
        for dist in range(1, size + 1):
            # Obliczamy nowe współrzędne punktu
            new_x = x + dx * dist
            new_y = y + dy * dist
            neighborhood.append((new_x, new_y))

    return neighborhood


# Funkcja kosztu, uwzględniająca teren i odległości między robotami
def movement_cost(current, neighbor, terrain, oc_pos, stp_num, robot_distance=2, terrain_weight=1, robot_distance_weight=1):
    height_diff = abs(terrain[neighbor[0]][neighbor[1]] - terrain[current[0]][current[1]])
    distance_cost = 0

    # Pobieramy zajęte pozycje w czasie i przestrzeni (przeszłość/przyszłość)
    occupied_future_positions = set()
    for row in oc_pos:
        for offset in range(-robot_distance, robot_distance + 1):  # Uwzględniamy dystans
            index = stp_num + offset
            if 0 <= index < len(row):  # Sprawdzenie, czy indeks jest w zakresie
                occupied_future_positions.add(row[index])

    # Generowanie sąsiedztwa dla potencjalnego konfliktu
    neighbors = generate_neighborhood(neighbor, robot_distance, [
        (0, 1), (1, 0), (0, -1), (-1, 0),
        (1, 1), (-1, -1), (-1, 1), (1, -1),
    ])

    # Jeśli dany ruch prowadzi do zajętej pozycji, nakładamy dużą karę
    if neighbor in occupied_future_positions:
        distance_cost += 10**6  # Duża kara za kolizję, ale nie nieskończoność

    # Dodatkowa kara za bliskość do zajętych pozycji (im bliżej, tym większa kara)
    for n in neighbors:
        if n in occupied_future_positions:
            distance_cost += 100 / max(heuristic(neighbor, n), 1)  # Dynamiczna kara

    # Zwracanie całkowitego kosztu, łącznie z wysokością terenu i karami za dystans
    return (height_diff * 15 * terrain_weight) + (distance_cost * robot_distance_weight)


# Algorytm A* dla każdego robota
def astar(terrain, start, goal, occupied_positions, robot_distance=2, terrain_weight=1, robot_distance_weight=1):
    rows, cols = len(terrain), len(terrain[0])
    open_set = [(0, start)]  # Lista zamiast kopca
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    step_num = 0

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    costs = []
    costs_f = []

    while open_set:
        open_set.sort()  # Sortowanie listy w celu wyboru elementu o najniższym koszcie
        min_cost, current = open_set.pop(0)  # Pobranie elementu z najmniejszym kosztem

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], min_cost, costs, costs_f

        x, y = current
        costs.append(min_cost)
        costs_f.append(f_score[current])

        for dx, dy in directions:
            neighbor = (x + dx, y + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                # Sprawdzenie, czy pole sąsiada jest zajęte przez inne roboty w przyszłości
                occupied_in_future = False
                for t in range(robot_distance):
                    if step_num + t < len(occupied_positions):
                        if neighbor in occupied_positions[step_num + t]:
                            occupied_in_future = True
                            break

                if occupied_in_future:
                    continue  # Pomijamy ruch, jeśli sąsiad będzie zajęty

                cost = movement_cost(
                    current, neighbor, terrain, occupied_positions, step_num,
                    robot_distance, terrain_weight, robot_distance_weight
                )
                tentative_g_score = g_score[current] + cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                    # Obliczanie aktualnego kroku robota
                    temp_path = []
                    v = current
                    while v in came_from:
                        temp_path.append(v)
                        v = came_from[v]
                    temp_path.append(start)

                    step_num = len(temp_path[::-1])

                    # Dodajemy do listy i sortujemy, aby utrzymać najniższy koszt na początku
                    open_set.append((f_score[neighbor], neighbor))

    return None  # Brak ścieżki


from PIL import Image
import numpy as np

# Open the image file
# image = Image.open('kopup.PNG')
# grayscale_image = image.convert('L')  # 'L' oznacza obraz w skali szarości
# matrix = np.array(grayscale_image)
#
# # Przekonwertuj macierz NumPy na listę list
# matrix_list_of_lists = matrix.tolist()
#
# # # Wyświetl wynik (listę list)
# # for row in matrix_list_of_lists:
# #     print(row)
# terrain = matrix_list_of_lists

# Inicjalizacja mapy terenu 51x51
# terrain = terrain_generator(0, terrain_size=(51, 51), terrain_type="hills")
# print(terrain)
# Punkty startowe dla N robotów
# start_positions = [(2, 2), (10, 0), (0, 10), (1, 1)]
# start_positions = [(0, 2), (2, 0), (0, 0), (2, 2)]
# start_positions = [(0, 0), (10,0)]
# goal = (40, 40)
#
# # Lista pozycji zajętych przez roboty (początkowo puste)
# occupied_positions = list()
# paths = []
#
# all_cost = []
# for start in start_positions:
#     path, min_val, costs = astar(terrain, start, goal, occupied_positions, robot_distance=2, robot_distance_weight=1, terrain_weight=1)
#     all_cost.append(costs)
#     print(" -------------------- ")
#     if path:
#         paths.append(path)
#         occupied_positions.append(path)  # Aktualizacja zajętych pozycji
#     else:
#         print(f"Brak możliwej ścieżki dla robota z pozycji {start}")
#
#
# # Rysowanie wyników
# plot_graph(paths, terrain, start_positions, goal)
# # plot_graph_animation(paths, terrain, start_positions, goal)
#
# num = 0
# for i in all_cost:
#     plt.plot(i, color=["red", "blue", "orange", "yellow", "magenta"][num])
#     num+=1
#
# plt.show()
# if paths:
#     for i, path in enumerate(paths):
#         print(f"Najkrótsza ścieżka dla robota {i + 1}: {path}")
#         print(len(path))
# else:
#     print("Brak możliwych ścieżek dla wszystkich robotów.")
