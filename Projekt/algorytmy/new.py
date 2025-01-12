import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np

# Generate a random terrain map (for testing)

def generate_terrain_map(rows, cols, max_height):
    return np.random.randint(0, 1, size=(rows, cols))
    return np.random.randint(0, max_height, size=(rows, cols))


# Objective function: calculates the cost of a path
def path_cost(path, terrain_map):
    cost = 0
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        # Horizontal distance
        horizontal_dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        # Height difference
        height_diff = abs(terrain_map[x2, y2] - terrain_map[x1, y1])
        cost += horizontal_dist + height_diff  # Combine horizontal and vertical costs
    return cost

# Generate random paths
def random_path(start, end, terrain_map, num_points=10):
    rows, cols = terrain_map.shape
    path = [start]
    for _ in range(num_points - 2):
        # Random intermediate points
        path.append((np.random.randint(0, rows), np.random.randint(0, cols)))
    path.append(end)
    return path

# PSO parameters
num_particles = 30
max_iterations = 100
w = 0.5  # Inertia weight
phi_p = 1.5  # Cognitive coefficient
phi_g = 1.5  # Social coefficient

# Terrain map
rows, cols = 10, 10
max_height = 100
terrain_map = generate_terrain_map(rows, cols, max_height)

print("Mapa terenu")
print(terrain_map)


# Start and end points
start = (0, 0)
end = (9, 9)

plt.imshow(terrain_map)
plt.scatter(start[0], start[1])
plt.scatter(end[0], end[1])
plt.show()

# Initialize particles
particles = [random_path(start, end, terrain_map) for _ in range(num_particles)]
velocities = [np.zeros_like(p) for p in particles]
personal_best_positions = particles[:]
personal_best_scores = [path_cost(p, terrain_map) for p in particles]
global_best_position = personal_best_positions[np.argmin(personal_best_scores)]
global_best_score = min(personal_best_scores)

# PSO main loop
for iteration in range(max_iterations):
    for i in range(num_particles):
        # Update velocity and path
        rp = np.random.uniform(0, 1)
        rg = np.random.uniform(0, 1)
        for j in range(1, len(particles[i]) - 1):  # Exclude start and end points
            velocities[i][j] = (
                w * velocities[i][j]
                + phi_p * rp * (np.array(personal_best_positions[i][j]) - np.array(particles[i][j]))
                + phi_g * rg * (np.array(global_best_position[j]) - np.array(particles[i][j]))
            )
            particles[i][j] = tuple(np.clip(particles[i][j] + velocities[i][j], 0, rows - 1).astype(int))

        # Evaluate fitness
        fitness = path_cost(particles[i], terrain_map)

        # Update personal best
        if fitness < personal_best_scores[i]:
            personal_best_positions[i] = particles[i]
            personal_best_scores[i] = fitness

            # Update global best
            if fitness < global_best_score:
                global_best_position = particles[i]
                global_best_score = fitness

    print(f"Iteration {iteration + 1}/{max_iterations}, Best score: {global_best_score}")

print("Best path:", global_best_position)
print("Best score:", global_best_score)

plt.imshow(terrain_map)
X = [int(i[0]) for i in global_best_position]
Y = [int(i[1]) for i in global_best_position]
plt.scatter(X, Y)
plt.show()