import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def terrain_generator(noise_num=1, terrain_size=(100, 100), terrain_type="hills"):
    # Generowanie danych do symulacji wysokości terenu
    # np.random.seed(422)  # Ustawienie ziarna losowego dla powtarzalności
    noise = np.random.rand(*terrain_size) * noise_num  # Losowe zakłócenia terenu

    # Dodanie struktury, np. pagórków
    x = np.linspace(0, 1, terrain_size[0])
    y = np.linspace(0, 1, terrain_size[1])
    X, Y = np.meshgrid(x, y)

    # Wybór typu terenu
    if terrain_type == "hills":
        hills = np.sin(4 * np.pi * X) * np.cos(4 * np.pi * Y) * 20
    elif terrain_type == "lines":
        hills = np.sin(4 * np.pi * X)
    elif terrain_type == "slope":
        hills = 2 * X
    elif terrain_type == "razors":
        hills = 2 * Y - np.sin(4 * np.pi * X)
    elif terrain_type == "canyon":
        hills = np.maximum(np.sin(2 * np.pi * X) * np.sin(2 * np.pi * Y), 0)
    elif terrain_type == "bow":
        hills = np.maximum(np.sin(2 * np.pi * X*Y), 0)
    elif terrain_type == "maze":
        # Generowanie wzoru przypominającego labirynt
        maze = np.zeros(terrain_size)
        for i in range(0, terrain_size[0], 4):  # Tworzenie ścian co kilka kroków
            maze[i, :] = 20
        for j in range(0, terrain_size[1], 8):
            maze[:, j] = 20
        # Przypadkowe otwarcia w ścianach
        for _ in range(int(terrain_size[0] * terrain_size[1] * 0.02)):  # Procent otwarć
            maze[np.random.randint(0, terrain_size[0]), np.random.randint(0, terrain_size[1])] = 0
        hills = maze
    else:
        hills = 0

    # Połączenie zakłóceń i struktury
    if terrain_size[0] != terrain_size[1]:
        terrain = noise.T + hills
    else:
        terrain = noise + hills

    return terrain

#
#
# # Tworzenie heatmapy
# plt.figure(figsize=(10, 8))
# terr = terrain_generator()
# print(terr)
# plt.imshow(terr, origin='upper', cmap="magma")
# plt.colorbar(label='Wysokość terenu')
# plt.title('Mapa wysokości terenu')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.show()


if '__name__' == "__main__":
    # Tworzenie heatmapy
    plt.figure(figsize=(10, 8))
    terr = terrain_generator()
    print(terr)
    print(terr)
    plt.imshow(terr, origin='upper', cmap="magma")
    plt.colorbar(label='Wysokość terenu')
    plt.title('Mapa wysokości terenu')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()