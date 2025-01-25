import numpy as np
import random
from scipy.spatial.distance import euclidean

# Parametry PSO
NUM_PARTICLES = 50
NUM_ITERATIONS = 100
INERTIA_WEIGHT = 0.7
COGNITIVE_WEIGHT = 1.5
SOCIAL_WEIGHT = 1.5

# Parametry robota
ROBOT_DISTANCE = 2  # Minimalna odległość między robotami


# Funkcja kosztu uwzględniająca wysokość i odległość

def cost_function(path, terrain, robots_positions):
    terrain_cost = sum(terrain[x, y] for x, y in path)

    distance_cost = 0
    for i in range(len(path) - 1):
        distance_cost += euclidean(path[i], path[i + 1])

    separation_cost = sum(max(0, ROBOT_DISTANCE - euclidean(path[-1], pos)) for pos in robots_positions)

    return terrain_cost + distance_cost + separation_cost


# Inicjalizacja cząsteczek

def initialize_particles(num_particles, start, end, grid_size):
    particles = []
    for _ in range(num_particles):
        path = [(start[0], start[1])]
        while path[-1] != end:
            x, y = path[-1]
            next_step = random.choice([(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)])
            next_step = (max(0, min(next_step[0], grid_size[0] - 1)),
                         max(0, min(next_step[1], grid_size[1] - 1)))
            if next_step not in path:
                path.append(next_step)
        particles.append(path)
    return particles


# Aktualizacja cząsteczek

def update_particles(particles, personal_best, global_best, velocities):
    for i in range(len(particles)):
        new_path = []
        for j in range(len(particles[i])):
            r1, r2 = random.random(), random.random()
            new_x = int(INERTIA_WEIGHT * particles[i][j][0] +
                        COGNITIVE_WEIGHT * r1 * (personal_best[i][j][0] - particles[i][j][0]) +
                        SOCIAL_WEIGHT * r2 * (global_best[j][0] - particles[i][j][0]))
            new_y = int(INERTIA_WEIGHT * particles[i][j][1] +
                        COGNITIVE_WEIGHT * r1 * (personal_best[i][j][1] - particles[i][j][1]) +
                        SOCIAL_WEIGHT * r2 * (global_best[j][1] - particles[i][j][1]))
            new_path.append((new_x, new_y))
        particles[i] = new_path
    return particles


# Funkcja optymalizacji

def pso_path_finding(terrain, start, end, num_robots):
    grid_size = terrain.shape
    robots_positions = [start for _ in range(num_robots)]
    particles = initialize_particles(NUM_PARTICLES, start, end, grid_size)
    personal_best = particles.copy()
    global_best = min(particles, key=lambda p: cost_function(p, terrain, robots_positions))
    velocities = np.zeros_like(particles)

    for iter in range(NUM_ITERATIONS):
        print(iter)
        for i, particle in enumerate(particles):
            cost = cost_function(particle, terrain, robots_positions)
            if cost < cost_function(personal_best[i], terrain, robots_positions):
                personal_best[i] = particle
        global_best = min(personal_best, key=lambda p: cost_function(p, terrain, robots_positions))
        particles = update_particles(particles, personal_best, global_best, velocities)

    return global_best


# Przykładowa mapa terenu
grid_size = (11, 11)
terrain = np.random.randint(1, 10, grid_size)
start = (0, 0)
end = (10, 10)
num_robots = 3

# Uruchomienie algorytmu
best_path = pso_path_finding(terrain, start, end, num_robots)
print("Najlepsza znaleziona ścieżka:", best_path)
