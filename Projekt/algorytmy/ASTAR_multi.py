import heapq
import matplotlib.pyplot as plt
import numpy as np

from algorytmy.terrain import terrain_generator


def plot_graph(paths, terrain, starts, goal):
    plt.close("all")
    plt.figure(figsize=(5, 5))
    plt.imshow(terrain)

    colors = ["red", "blue", "green", "purple", "orange"]

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

    colors = ["red", "blue", "purple", "black"]

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
def movement_cost(current, neighbor, terrain, oc_pos, step_num):
    height_diff = abs(terrain[neighbor[0]][neighbor[1]] - terrain[current[0]][current[1]])
    base_cost = 1 + height_diff * 10000  # Podstawowy koszt z wysokością
    # print([row[step_num] for row in occupied_positions])
    columns = []
    for row in oc_pos:
        for t in range(-2, 3):
            if step_num + t >= 0:
                try:
                    columns.append(row[step_num + t])
                except:
                    pass

    neigh = generate_neighborhood(neighbor, 3, [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1), (0,0)])
    # TODO: poprawić
    for x in neigh:
        if x in occupied_positions:
            print("-------", heuristic(neighbor, x)," " , neighbor," ", x )
            dis = heuristic(current, x)
            if dis != 0:
                base_cost += 10000/dis # Kara za bliskość do innego robota
            else:
                base_cost += 10000

    print(f"Base {base_cost}, {current} --> {neighbor} " )
    return base_cost


# Algorytm A* dla każdego robota
def astar(terrain, start, goal, occupied_positions):
    rows, cols = len(terrain), len(terrain[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    step_num = 0

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        x, y = current
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                cost = movement_cost(current, neighbor, terrain, occupied_positions, step_num)
                tentative_g_score = g_score[current] + cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        step_num += 1
    return None  # Brak ścieżki


# Inicjalizacja mapy terenu 51x51
terrain = terrain_generator(0, terrain_size=(51, 51), terrain_type="hills")

# Punkty startowe dla N robotów
start_positions = [(5, 5), (10, 0), (0, 10), (1, 1)]
# start_positions = [(0, 1), (1, 0), (0, 0), (1, 1)]
goal = (48, 49)

# Lista pozycji zajętych przez roboty (początkowo puste)
occupied_positions = list()
paths = []

for start in start_positions:
    path = astar(terrain, start, goal, occupied_positions)
    print(" -------------------- ")
    if path:
        paths.append(path)
        occupied_positions.append(path)  # Aktualizacja zajętych pozycji
    else:
        print(f"Brak możliwej ścieżki dla robota z pozycji {start}")

# Rysowanie wyników
plot_graph(paths, terrain, start_positions, goal)
plot_graph_animation(paths, terrain, start_positions, goal)

if paths:
    for i, path in enumerate(paths):
        print(f"Najkrótsza ścieżka dla robota {i + 1}: {path}")
else:
    print("Brak możliwych ścieżek dla wszystkich robotów.")
