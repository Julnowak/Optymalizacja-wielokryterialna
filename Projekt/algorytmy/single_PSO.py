from algorytmy.terrain import terrain_generator
import numpy as np
import matplotlib.pyplot as plt
import math

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
        # plt.text(best_location[i][0] + 0.1,best_location[i][1]+0.1,str(i),fontsize=8)
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

    z = (x[0, 0] - START[0]) ** 2 + (x[0, 1] - START[1]) ** 2
    for i in range(DIM - 1):
        z = z + ((x[i, 0] - x[i + 1, 0]) ** 2 + (x[i, 1] - x[i + 1, 1]) ** 2)
    z = z + (x[DIM - 1, 0] - END[0]) ** 2 + (x[DIM - 1, 1] - END[1]) ** 2
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

    # set the location and velocity of the particle's
    particles_loc = np.random.rand(swarm_size, DIM, 2) * 20
    particles_vel = np.random.rand(swarm_size, DIM, 2)

    # set the initial particle best location and value
    particles_lowest_loss = [
        loss_function(particles_loc[i, :, :]) for i in range(0, len(particles_loc))
    ]
    particles_best_location = np.copy(particles_loc)

    # set the initial global best location and value
    global_lowest_loss = np.min(particles_lowest_loss)
    global_best_location = particles_loc[np.argmin(particles_lowest_loss)].copy()

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
        if iteration_i % 20 == 0:
            print(f"{int(iteration_i / max_iterations * 100)}% completed")

        for particle_i in range(swarm_size):
            for dim_i in range(DIM):
                # Update the velocity vector in a given dimension
                error_particle_best = (
                    particles_best_location[particle_i, dim_i]
                    - particles_loc[particle_i, dim_i]
                )
                error_global_best = (
                    global_best_location[dim_i] - particles_loc[particle_i, dim_i]
                )
                new_vel = (
                    inertia * particles_vel[particle_i, dim_i]
                    + c1 * np.random.rand() * error_particle_best
                    + c2 * np.random.rand() * error_global_best
                )

                # Bound a particle's velocity to the maximum value
                new_vel = np.clip(new_vel, -max_vel, max_vel)

                # Update the particle location and velocity
                particles_loc[particle_i, dim_i] += new_vel * step_size
                particles_vel[particle_i, dim_i] = new_vel

            # For the new location, check if this is a new local or global best
            particle_error = loss_function(particles_loc[particle_i])
            if particle_error < particles_lowest_loss[particle_i]:  # Local best
                particles_lowest_loss[particle_i] = particle_error
                particles_best_location[particle_i] = particles_loc[particle_i].copy()

            if particle_error < global_lowest_loss:  # Global best
                global_lowest_loss = particle_error
                global_best_location = particles_loc[particle_i].copy()

    return global_best_location

DIM = 11
START = (1, 1)
END = (10, 20)

if __name__ == "__main__":
    DIM = 11
    best_location = particle_swarm_optimization(
        max_iterations=100,
        swarm_size=100,
        max_vel=3,
        step_size=1,
        inertia=0.9,
        c1=2.05,
        c2=2.05
    )
    print("100% completed!")
    plot_graph(best_location)
    plt.savefig("results", dpi=300)
    plt.show()