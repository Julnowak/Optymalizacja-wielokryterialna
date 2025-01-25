import heapq
import matplotlib.pyplot as plt
import numpy as np

from algorytmy.terrain import terrain_generator
import matplotlib.animation as animation


def plot_graph(paths, terrain, starts, goal):
    plt.close("all")
    plt.figure(figsize=(5, 5))
    plt.imshow(terrain)

    colors = ["red", "blue", "green", "purple", "orange"]

    for i, path in enumerate(paths):
        for point in path:
            plt.scatter(point[1], point[0], 25, marker=".",
                        facecolors=colors[i % len(colors)],
                        edgecolors="face")

    plt.scatter(goal[1], goal[0], 100, marker="*", facecolors="k", edgecolors="k")
    for start in starts:
        plt.scatter(start[1], start[0], 100, marker="o", facecolors="k", edgecolors="k")

    plt.title("Multi-Robot Pathfinding")
    plt.show()


def plot_graph_animation(paths, terrain, starts, goal):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(terrain)

    colors = ["red", "blue", "purple", "black"]

    def update(frame):
        ax.clear()
        ax.imshow(terrain)

        # Rysowanie punktów z poprzednich tras
        for i, path in enumerate(paths):
            if frame < len(path):
                point = path[frame]
                ax.scatter(point[1], point[0], 25, marker=".",
                           facecolors=colors[i % len(colors)],
                           edgecolors="face")

        # Ponownie rysowanie punktu docelowego i początkowych
        ax.scatter(goal[1], goal[0], 100, marker="*", facecolors="k", edgecolors="k")
        for start in starts:
            ax.scatter(start[1], start[0], 100, marker="o", facecolors="k", edgecolors="k")

        ax.set_title("Multi-Robot Pathfinding")

    max_frames = max(len(path) for path in paths)
    ani = animation.FuncAnimation(fig, update, frames=max_frames, repeat=False)
    plt.show()


def heuristic(a, b):
    (x1, y1), (x2, y2) = a, b
    return abs(x1 - x2) + abs(y1 - y2)

def is_valid(pos, terrain):
    """Sprawdza, czy pozycja mieści się w granicach mapy."""
    x, y = pos
    rows, cols = len(terrain), len(terrain[0])
    return 0 <= x < rows and 0 <= y < cols

def movement_cost(current, neighbor, terrain):
    """
    Minimalna funkcja kosztu, uwzględniająca chociażby wysokość terenu.
    Możesz dodać tu inne 'kary', np. za duże różnice wysokości itd.
    """
    height_diff = abs(terrain[neighbor[0]][neighbor[1]] - terrain[current[0]][current[1]])
    base_cost = 1 + height_diff * 10000
    return base_cost

def reconstruct_path(came_from, current_state):
    """Odtwarza ścieżkę (tylko współrzędne x,y) z mapy rodziców."""
    path = []
    while current_state in came_from:
        (pos, t) = current_state
        current_state = came_from[current_state]
        path.append(pos)
    # Dodaj jeszcze pierwszy stan
    path.append(current_state[0])
    path.reverse()
    return path

def astar_time(terrain, start, goal, blocked, max_steps=500):
    """
    A* w rozszerzonej domenie (x, y, t).
    - blocked to zbiór (pos, t), które są 'zajęte' w chwili t przez inne roboty.
    - max_steps to limit, żeby algorytm nie szukał ścieżki w nieskończoność.
    Zwraca listę (x,y) do celu lub None.
    """

    # f_score, g_score = { (start, 0): ... }, ale w Pythonie lepiej osobno: dict[(pos, t)]
    open_set = []
    came_from = {}

    g_score = {(start, 0): 0}
    f_score = {(start, 0): heuristic(start, goal)}

    heapq.heappush(open_set, (f_score[(start, 0)], (start, 0)))

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                  (1, 1), (-1, -1), (-1, 1), (1, -1)]

    while open_set:
        _, (current_pos, current_t) = heapq.heappop(open_set)

        # Jeśli osiągnęliśmy cel, odtwarzamy ścieżkę
        if current_pos == goal:
            return reconstruct_path(came_from, (current_pos, current_t))

        # Ograniczenie czasu, żeby się nie zapętlać
        if current_t >= max_steps:
            continue

        # Rozwijamy sąsiadów
        for dx, dy in directions:
            neighbor = (current_pos[0] + dx, current_pos[1] + dy)
            next_t = current_t + 1

            if not is_valid(neighbor, terrain):
                continue

            # Sprawdzamy, czy (neighbor, next_t) jest już zablokowane przez inny robot
            if (neighbor, next_t) in blocked:
                continue

            # Policzenie kosztu
            cost = g_score[(current_pos, current_t)] + movement_cost(current_pos, neighbor, terrain)

            if (neighbor, next_t) not in g_score or cost < g_score[(neighbor, next_t)]:
                g_score[(neighbor, next_t)] = cost
                f_score[(neighbor, next_t)] = cost + heuristic(neighbor, goal)
                came_from[(neighbor, next_t)] = (current_pos, current_t)
                heapq.heappush(open_set, (f_score[(neighbor, next_t)], (neighbor, next_t)))

    return None  # Brak ścieżki

# ----------------------------------------------------------------
#                GŁÓWNY KAWAŁEK KODU WYKONAWCZEGO
# ----------------------------------------------------------------

# 1) Tworzymy mapę terenu
terrain = terrain_generator(0, terrain_size=(51, 51), terrain_type="hills")

# 2) Ustalamy punkty startowe i cel
start_positions = [(5, 5), (10, 0), (0, 10), (1, 1)]
goal = (48, 49)

# 3) Struktura blocked - zbiór zajętych stanów (x, y, t)
blocked = set()

# 4) Dla wizualizacji przechowujemy tylko listę (x,y) ścieżek
paths = []

# 5) Sekwencyjnie planujemy trasy dla kolejnych robotów
for start in start_positions:
    path = astar_time(terrain, start, goal, blocked, max_steps=300)
    if not path:
        print(f"Brak możliwej ścieżki dla robota z pozycji {start}")
        paths.append([])  # wstaw pustą ścieżkę
        continue

    # Jeśli mamy ścieżkę, zapamiętujemy ją do rysowania
    paths.append(path)

    # Oznaczamy zablokowane stany: (pozycja, krok_czasowy)
    # W path[i] robot jest w kroku i. Zatem blokujemy (path[i], i).
    # Można też blokować do i+1, jeśli chcemy dodatkowo unikać "zderzeń na przejściu".
    for t, pos in enumerate(path):
        blocked.add((pos, t))

# 6) Rysujemy (uwaga: to rysuje tylko finalne przebiegi)
plot_graph(paths, terrain, start_positions, goal)
plot_graph_animation(paths, terrain, start_positions, goal)

if any(paths):
    for i, path in enumerate(paths):
        print(f"Najkrótsza ścieżka dla robota {i + 1}: {path}")
else:
    print("Brak możliwych ścieżek dla wszystkich robotów.")
