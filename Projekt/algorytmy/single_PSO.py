from algorytmy.terrain import terrain_generator
import numpy as np
import matplotlib.pyplot as plt
import math
import random


def plot_graph(best_location):
    """
    This function plot the graph.

    Parameters:
        best_location (List[float, float]): Lists of points to plot.
    """


    plt.close("all")
    plt.figure(figsize=(5, 5))
    plt.grid("on")
    plt.rc("axes", axisbelow=True)
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
    plt.xlim(-1, 23)
    plt.ylim(-1, 23)
    plt.title("Particle Swarm Optimization")

def loss_function(x):
    """
    Loss function to find the shortest path.

    Parameters:
        x (List[Point]): List of points representing the path of the agent.

    Returns:
        int: The loss function result
    """

    z = (x[0][0] - START[0]) ** 2 + (x[0][1] - START[1]) ** 2
    for i in range(DIM - 1):
        z += (x[i][0] - x[i + 1][0]) ** 2 + (x[i][1] - x[i + 1][1]) ** 2
    z += (x[DIM - 1][0] - END[0]) ** 2 + (x[DIM - 1][1] - END[1]) ** 2
    return math.sqrt(z)

def random_initialization(swarm_size):
    """
    Random initializations of PSO particles location and velocity.

    Parameters:
        swarm_size (int): How many particles are present.

    Returns:
        List[List[float, float]]: List of starting coordinates of the particles, total number = swarm_size * DIM * 2.
        List[float, float]: List of starting velocity of the particles, total number = swarm_size * DIM * 2.
        List[floats]: Each particle best loss function result.
        List[List[float, float]]: List of best velocity of the particles (there's only the starting in the initialization).
        float: Best loss function result.
        List[float, float]: The best location.
    """

    particles_loc = [[[random.random() * 20, random.random() * 20] for _ in range(DIM)] for _ in range(swarm_size)]
    particles_vel = [[[random.random() for _ in range(2)] for _ in range(DIM)] for _ in range(swarm_size)]

    # set the initial particle best location and value
    particles_lowest_loss = [
        loss_function(particles_loc[i]) for i in range(swarm_size)
    ]
    particles_best_location = [loc.copy() for loc in particles_loc]

    # set the initial global best location and value
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

def particle_swarm_optimization(
    max_iterations, swarm_size, max_vel, step_size, inertia, c1, c2
):
    """
    Implementation of the Particle Swarm Optimization algorithm.

    Parameters:
        max_iterations (int): The maximum number of iterations.
        swarm_size (int): The number of particles.
        max_vel (int): Maximum velocity for a particle.
        step_size (int): The step size for updating each particle (how far a particle travels before its velocity is readjusted).
        inertia (float): The inertia of a particle.
        c1 (float): Factor for the particle's local best.
        c2 (float): Factor for the global best.

    Returns:
        np.ndarray: The best location found by the swarm.
    """
    (
        particles_loc,
        particles_vel,
        particles_lowest_loss,
        particles_best_location,
        global_lowest_loss,
        global_best_location,
    ) = random_initialization(swarm_size)

    for iteration_i in range(max_iterations):
        for particle_i in range(swarm_size):
            for dim_i in range(DIM):
                # Update the velocity vector in a given dimension
                error_particle_best = (
                    particles_best_location[particle_i][dim_i][0] - particles_loc[particle_i][dim_i][0],
                    particles_best_location[particle_i][dim_i][1] - particles_loc[particle_i][dim_i][1]
                )
                error_global_best = (
                    global_best_location[dim_i][0] - particles_loc[particle_i][dim_i][0],
                    global_best_location[dim_i][1] - particles_loc[particle_i][dim_i][1]
                )

                new_vel = [
                    inertia * particles_vel[particle_i][dim_i][0] + c1 * random.random() * error_particle_best[
                        0] + c2 * random.random() * error_global_best[0],
                    inertia * particles_vel[particle_i][dim_i][1] + c1 * random.random() * error_particle_best[
                        1] + c2 * random.random() * error_global_best[1]
                ]

                # Bound a particle's velocity to the maximum value
                new_vel = [
                    max(min(new_vel[0], max_vel), -max_vel),
                    max(min(new_vel[1], max_vel), -max_vel)
                ]

                # Update the particle location and velocity
                particles_loc[particle_i][dim_i][0] += new_vel[0] * step_size
                particles_loc[particle_i][dim_i][1] += new_vel[1] * step_size
                particles_vel[particle_i][dim_i] = new_vel

            # For the new location, check if this is a new local or global best
            particle_error = loss_function(particles_loc[particle_i])
            if particle_error < particles_lowest_loss[particle_i]:  # Local best
                particles_lowest_loss[particle_i] = particle_error
                particles_best_location[particle_i] = [loc.copy() for loc in particles_loc[particle_i]]

            if particle_error < global_lowest_loss:  # Global best
                global_lowest_loss = particle_error
                global_best_location = [loc.copy() for loc in particles_loc[particle_i]]

    return global_best_location


DIM = 11
START = (1, 1)
END = (10, 20)

if __name__ == "__main__":

    best_location = particle_swarm_optimization(
        max_iterations=1000,
        swarm_size=100,
        max_vel=3,
        step_size=1,
        inertia=0.5,
        c1=0.5,
        c2=1
    )
    print("100% completed!")
    plot_graph(best_location)
    plt.show()