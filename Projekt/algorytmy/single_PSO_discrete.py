import random
import math
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from terrain import terrain_generator

TERRAIN = terrain_generator(terrain_size=(20, 20))

def plot_graph(best_location):
    plt.close("all")
    plt.figure(figsize=(5, 5))
    # plt.grid("off")
    # plt.rc("axes", axisbelow=True)
    plt.imshow(TERRAIN,)
    plt.scatter(END[0], END[1], 100, marker="*", facecolors="k", edgecolors="k")
    plt.scatter(START[0], START[1], 100, marker="o", facecolors="k", edgecolors="k")
    X = [best_location[i][0] for i in range(DIM)]
    X.insert(0, START[0])
    X.append(END[0])
    Y = [best_location[i][1] for i in range(DIM)]
    Y.insert(0, START[1])
    Y.append(END[1])
    plt.plot(X, Y, "o-")
    for i in range(DIM):
        plt.scatter(
            best_location[i][0],
            best_location[i][1],
            25,
            marker=".",
            facecolors="blue",
            edgecolors="face",
        )

    plt.title("Particle Swarm Optimization")


def loss_function(x):
    # Funkcja straty: oblicza sumę kwadratów odległości między punktami
    print(x)
    print([x[0][0], x[0][1]])
    print(TERRAIN[x[0][0], x[0][1]])
    z = (x[0][0] - START[0]) ** 2 + (x[0][1] - START[1]) ** 2 + np.abs(TERRAIN[x[0][0], x[0][1]]) * 20000
    for i in range(DIM - 1):
        z += (x[i][0] - x[i + 1][0]) ** 2 + (x[i][1] - x[i + 1][1]) ** 2
    z += (x[DIM - 1][0] - END[0]) ** 2 + (x[DIM - 1][1] - END[1]) ** 2
    return np.sqrt(z)


def random_initialization(swarm_size, grid_size):

    # początkowe ścieżki DIM-punktowe
    particles_loc = [
        [(random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1)) for _ in range(DIM)]
        for _ in range(swarm_size)
    ]

    print(particles_loc)
    particles_vel = [
        [random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)]) for _ in range(DIM)]
        for _ in range(swarm_size)
    ]

    particles_lowest_loss = []
    print("==========================")
    for i in range(swarm_size):
        loss = loss_function(particles_loc[i])
        particles_lowest_loss.append(loss)
    print("==========================")

    particles_best_location = [loc.copy() for loc in particles_loc]

    global_lowest_loss = min(particles_lowest_loss)

    global_best_location = particles_loc[particles_lowest_loss.index(global_lowest_loss)].copy()

    return (
        particles_loc,
        particles_vel,
        particles_lowest_loss,
        particles_best_location,
        global_lowest_loss,
        global_best_location,
    )


def particle_swarm_optimization(max_iterations, swarm_size, inertia, c1, c2, grid_size,  max_vel=3, step_size=1,):

    particles_loc, particles_vel, particles_lowest_loss, particles_best_location, global_lowest_loss, global_best_location = random_initialization(
        swarm_size, grid_size)

    for iteration in range(max_iterations):
        for particle_i in range(swarm_size):
            for dim_i in range(DIM):
                # Aktualizacja prędkości (ruch cząstki w jednym z 4 kierunków)
                error_particle_best = (
                    particles_best_location[particle_i][dim_i][0] - particles_loc[particle_i][dim_i][0],
                    particles_best_location[particle_i][dim_i][1] - particles_loc[particle_i][dim_i][1]
                )

                error_global_best = (
                    global_best_location[dim_i][0] - particles_loc[particle_i][dim_i][0],
                    global_best_location[dim_i][1] - particles_loc[particle_i][dim_i][1]
                )

                new_vel = (
                    inertia * particles_vel[particle_i][dim_i][0] + c1 * random.random() * error_particle_best[
                        0] + c2 * random.random() * error_global_best[0],
                    inertia * particles_vel[particle_i][dim_i][1] + c1 * random.random() * error_particle_best[
                        1] + c2 * random.random() * error_global_best[1]
                )

                # Zaktualizowanie pozycji w przestrzeni dyskretnej (w obrębie granic siatki)
                new_x = particles_loc[particle_i][dim_i][0] + new_vel[0]
                new_y = particles_loc[particle_i][dim_i][1] + new_vel[1]


                # Utrzymanie pozycji w granicach siatki
                new_x = round(max(0, min(grid_size[0] - 1, new_x)))
                new_y = round(max(0, min(grid_size[1] - 1, new_y)))


                particles_loc[particle_i][dim_i] = (new_x, new_y)
                particles_vel[particle_i][dim_i] = (new_vel[0], new_vel[1])

            # Sprawdzenie, czy ta pozycja jest lepsza niż poprzednia
            particle_error = loss_function(particles_loc[particle_i])
            if particle_error < particles_lowest_loss[particle_i]:  # Najlepsza lokalna
                particles_lowest_loss[particle_i] = particle_error
                particles_best_location[particle_i] = particles_loc[particle_i].copy()

            if particle_error < global_lowest_loss:  # Najlepsza globalna
                global_lowest_loss = particle_error
                global_best_location = particles_loc[particle_i].copy()

    return global_best_location


# Ile punktów ścieżki
DIM = 40
START = (0, 0)  # Początek w siatce 2D
END = (19, 19)  # Koniec w siatce 2D
GRID_SIZE = (20, 20)  # Rozmiar siatki 20x20

if __name__ == "__main__":
    best_location = particle_swarm_optimization(
        max_iterations=1000,
        swarm_size=20,
        inertia=0.5,
        c1=0.5,
        c2=1,
        grid_size=GRID_SIZE
    )
    print("100% completed!")
    plot_graph(best_location)
    plt.show()
