import heapq

import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from algorytmy.terrain import terrain_generator

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
    for i in range(len(best_path)):
        plt.scatter(
            best_path[i][1],
            best_path[i][0],
            25,
            marker=".",
            facecolors="red",
            edgecolors="face",
        )

    plt.title("Crawler Optimization")
    plt.show()

# Funkcja heurystyczna (odległość Manhattan + różnica wysokości)
def heuristic(a, b):
    (x1, y1), (x2, y2) = a, b
    return abs(x1 - x2) + abs(y1 - y2)


# Algorytm A* do wyznaczania najkrótszej trasy
def astar(terrain, start, goal):
    rows, cols = len(terrain), len(terrain[0])
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]  # ruchy: prawo, dół, lewo, góra

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Zwrócenie ścieżki od startu do celu

        x, y = current
        print("--------")
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                # Koszt ruchu bazujący na różnicy wysokości z bieżącego punktu do sąsiedniego
                height_diff = abs(terrain[neighbor[0]][neighbor[1]] - terrain[x][y])
                print(f"PUNKT: {(x,y)} z sąsidem {neighbor} ----> {height_diff}")
                print("Sąsiad koszt: ", terrain[neighbor[0]][neighbor[1]], "Punkt koszt: ", terrain[x][y])

                tentative_g_score = g_score[current] + height_diff*100
                print("Score: ", tentative_g_score)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        print("--------")
    return None  # Brak ścieżki


# Przykładowa mapa wysokości terenu 11x11
terrain = terrain_generator(0, terrain_size=(30,30), terrain_type="hills")

print(terrain)
# zerowa
# terrain = np.random.randint(0, 1, (51, 51))

start = (0, 0)
goal = (25, 27)

path = astar(terrain, start, goal)
plot_graph(path, terrain, start, goal)

if path:
    print("Najkrótsza ścieżka:", path)
else:
    print("Brak możliwej ścieżki.")
