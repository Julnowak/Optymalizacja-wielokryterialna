import numpy as np
import matplotlib

from algorytmy.terrain import terrain_generator

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class MultiObjectivePSO:
    def __init__(self, n_particles, n_dimensions, bounds, n_iterations, terrain, start, end, w=0.5, c1=1.5, c2=1.5):
        self.n_particles = n_particles
        self.n_dimensions = n_dimensions
        self.bounds = bounds
        self.n_iterations = n_iterations
        self.terrain = terrain
        self.start = start
        self.end = end
        self.w = w
        self.c1 = c1
        self.c2 = c2

        self.positions = np.random.uniform(bounds[0], bounds[1], (n_particles, n_dimensions, 2))
        self.positions[:, 0] = self.start  # Set the first position to the start point
        self.velocities = np.zeros_like(self.positions)
        self.pbest_positions = self.positions.copy()
        self.pbest_scores = np.full((n_particles, 2), np.inf)
        self.gbest_positions = None
        self.gbest_scores = np.full(2, np.inf)

    def evaluate(self, positions):
        damage_risk = np.zeros(self.n_particles)
        travel_time = np.zeros(self.n_particles)

        for i, particle in enumerate(positions):
            total_risk = 0
            for j in range(1, len(particle)):
                x, y = particle[j]
                x_prev, y_prev = particle[j - 1]
                if 0 <= int(x) < self.terrain.shape[0] and 0 <= int(y) < self.terrain.shape[1]:
                    terrain_risk = self.terrain[int(x), int(y)]
                else:
                    terrain_risk = 100  # High penalty for out-of-bounds
                distance = np.sqrt((x - x_prev)**2 + (y - y_prev)**2)
                total_risk += terrain_risk / (distance + 1e-6)
            damage_risk[i] = total_risk
            travel_time[i] = np.sum(np.linalg.norm(np.diff(particle, axis=0), axis=1))
        return np.column_stack((damage_risk, travel_time))

    def update(self):
        for iteration in range(self.n_iterations):
            scores = self.evaluate(self.positions)

            better_scores = (scores < self.pbest_scores).all(axis=1)
            self.pbest_positions[better_scores] = self.positions[better_scores]
            self.pbest_scores[better_scores] = scores[better_scores]

            for i, score in enumerate(scores):
                if (score < self.gbest_scores).all():
                    self.gbest_positions = self.positions[i]
                    self.gbest_scores = score

            r1, r2 = np.random.rand(self.n_particles, self.n_dimensions, 2), np.random.rand(self.n_particles, self.n_dimensions, 2)
            cognitive = self.c1 * r1 * (self.pbest_positions - self.positions)
            social = self.c2 * r2 * (self.gbest_positions - self.positions)
            self.velocities = self.w * self.velocities + cognitive + social
            self.positions += self.velocities

            self.positions = np.clip(self.positions, self.bounds[0], self.bounds[1])
            self.positions[:, 0] = self.start  # Reset start point
            self.positions[:, -1] = self.end  # Reset end point

            print(f"Iteration {iteration + 1}/{self.n_iterations}: Best Scores = {self.gbest_scores}")

    def plot_terrain(self):
        plt.imshow(self.terrain, cmap="terrain", origin="lower")
        plt.colorbar(label="Terrain Height")
        plt.scatter(self.start[1], self.start[0], color="blue", label="Start")
        plt.scatter(self.end[1], self.end[0], color="red", label="End")
        plt.legend()

    def plot_best_path(self):
        self.plot_terrain()
        best_path = self.gbest_positions
        if best_path is not None:
            plt.plot(best_path[:, 1], best_path[:, 0], color="yellow", label="Best Path")
            plt.legend()
        plt.show()


if '__name__' == "__main__":
    # Parameters
    terrain = terrain_generator(terrain_size=(100, 100), terrain_type="hills")
    start_point = (10, 10)
    end_point = (90, 90)
    n_particles = 30
    n_dimensions = 10
    bounds = (0, 99)
    n_iterations = 50

    # Run PSO
    pso = MultiObjectivePSO(n_particles, n_dimensions, bounds, n_iterations, terrain, start_point, end_point)
    pso.update()
    pso.plot_best_path()