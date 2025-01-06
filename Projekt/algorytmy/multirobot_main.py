import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from algorytmy.terrain import terrain_generator

###############################################################################
# 1. SingleRobotPSO – optymalizacja trasy dla 1 robota
###############################################################################
class SingleRobotPSO:
    def __init__(
        self,
        n_particles,
        n_dimensions,
        bounds,
        n_iterations,
        terrain,
        start,
        end,
        w=0.5,
        c1=1.5,
        c2=1.5
    ):
        """
        Każda cząstka = (n_dimensions, 2) -> trasa jednego robota.
        Funkcja celu = time + damage(terrain).
        """
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

        # Pozycje: (n_particles, n_dimensions, 2)
        self.positions = np.random.uniform(
            bounds[0],
            bounds[1],
            (n_particles, n_dimensions, 2)
        )
        # Wymuszenie start/end
        self.positions[:, 0] = self.start
        self.positions[:, -1] = self.end

        self.velocities = np.zeros_like(self.positions)

        # pbest
        self.pbest_positions = self.positions.copy()
        self.pbest_scores = np.full(n_particles, np.inf)

        # gbest
        self.gbest_position = None
        self.gbest_score = np.inf

    def _compute_cost(self, path):
        """
        Liczymy cost = time + damage(terrain).
        Dla uproszczenia damage = sum( terrain[x,y] / (dist+1e-6) ) po kolejnych krokach.
        """
        total_time = 0.0
        total_damage = 0.0
        for i in range(1, len(path)):
            x, y = path[i]
            x_prev, y_prev = path[i - 1]
            dist = np.sqrt((x - x_prev) ** 2 + (y - y_prev) ** 2)
            total_time += dist

            # terrain
            if 0 <= int(x) < self.terrain.shape[0] and 0 <= int(y) < self.terrain.shape[1]:
                terr_val = self.terrain[int(x), int(y)]
            else:
                terr_val = 100.0
            total_damage += terr_val / (dist + 1e-6)

        return total_time + total_damage

    def evaluate(self, positions):
        scores = np.zeros(self.n_particles)
        for p in range(self.n_particles):
            path = positions[p]
            scores[p] = self._compute_cost(path)
        return scores

    def update(self):
        for it in range(self.n_iterations):
            scores = self.evaluate(self.positions)

            # pbest
            better_mask = scores < self.pbest_scores
            self.pbest_positions[better_mask] = self.positions[better_mask]
            self.pbest_scores[better_mask] = scores[better_mask]

            # gbest
            min_idx = np.argmin(scores)
            if scores[min_idx] < self.gbest_score:
                self.gbest_score = scores[min_idx]
                self.gbest_position = self.positions[min_idx].copy()

            # PSO eq.
            r1 = np.random.rand(*self.positions.shape)
            r2 = np.random.rand(*self.positions.shape)
            cognitive = self.c1 * r1 * (self.pbest_positions - self.positions)
            social = self.c2 * r2 * (self.gbest_position - self.positions)
            self.velocities = self.w * self.velocities + cognitive + social
            self.positions += self.velocities

            # clip
            self.positions = np.clip(self.positions, self.bounds[0], self.bounds[1])
            self.positions[:, 0] = self.start
            self.positions[:, -1] = self.end

            #print(f"[SinglePSO] Iter {it+1}/{self.n_iterations}, best_score={self.gbest_score:.2f}")

        return self.gbest_position, self.gbest_score

###############################################################################
# 2. MultiRobotsPSO – optymalizacja wspólna (z density penalty)
###############################################################################
class MultiRobotsPSO:
    """
    n_robots: ile robotów
    cost = sum( time_r + damage_r ),
    damage_r: terrain + bliskość do innych robotów
    """
    def __init__(
        self,
        n_particles,
        n_robots,
        n_dimensions,
        bounds,
        n_iterations,
        terrain,
        starts,
        ends,
        # paramy do SinglePSO:
        single_particles=10,
        single_iter=50,
        # paramy do MultiPSO:
        w=0.5,
        c1=1.5,
        c2=1.5
    ):
        self.n_particles = n_particles
        self.n_robots = n_robots
        self.n_dimensions = n_dimensions
        self.bounds = bounds
        self.n_iterations = n_iterations
        self.terrain = terrain
        self.starts = starts
        self.ends = ends

        self.w = w
        self.c1 = c1
        self.c2 = c2

        # 1) Najpierw automatycznie wywołujemy SingleRobotPSO
        print("=== Stage 1: SinglePSO for each robot ===")
        initial_paths = []
        for r in range(self.n_robots):
            single_pso = SingleRobotPSO(
                n_particles=single_particles,
                n_dimensions=self.n_dimensions,
                bounds=self.bounds,
                n_iterations=single_iter,
                terrain=self.terrain,
                start=self.starts[r],
                end=self.ends[r],
                w=self.w, c1=self.c1, c2=self.c2
            )
            single_pso.update()
            initial_paths.append(single_pso.gbest_position)  # shape (n_dimensions,2)

        initial_paths = np.array(initial_paths)  # shape (n_robots, n_dimensions,2)

        # 2) Inicjalizacja populacji MultiPSO (n_particles, n_robots, n_dimensions, 2)
        self.positions = np.zeros((self.n_particles, self.n_robots, self.n_dimensions, 2))
        for p in range(self.n_particles):
            self.positions[p] = initial_paths  # kopiujemy wstępne ścieżki

        self.velocities = np.zeros_like(self.positions)

        # pbest
        self.pbest_positions = self.positions.copy()
        self.pbest_scores = np.full(n_particles, np.inf)

        # gbest
        self.gbest_position = None
        self.gbest_score = np.inf

    def _compute_robot_cost(self, path, all_paths):
        """
        cost = time + terrain + density
        """
        cost = 0.0
        n_robots = all_paths.shape[0]
        for i in range(1, self.n_dimensions):
            x, y = path[i]
            x_prev, y_prev = path[i-1]
            dist = np.sqrt((x - x_prev)**2 + (y - y_prev)**2)
            cost += dist  # time

            # terrain
            if 0 <= int(x) < self.terrain.shape[0] and 0 <= int(y) < self.terrain.shape[1]:
                terr_val = self.terrain[int(x), int(y)]
            else:
                terr_val = 100.0
            dmg_step = terr_val

            # density
            for other_r in range(n_robots):
                if np.all(all_paths[other_r] == path):
                    continue
                x2, y2 = all_paths[other_r][i]
                dd = np.sqrt((x - x2)**2 + (y - y2)**2) + 1e-6
                dmg_step += 1.0/dd

            cost += dmg_step
        return cost

    def evaluate(self, positions):
        """
        Zwraca (n_particles,) – cost
        """
        scores = np.zeros(self.n_particles)
        for p in range(self.n_particles):
            part_pos = positions[p]  # shape (n_robots, n_dimensions, 2)
            total_cost = 0.
            for r in range(self.n_robots):
                path_r = part_pos[r]
                total_cost += self._compute_robot_cost(path_r, part_pos)
            scores[p] = total_cost
        return scores

    def update(self):
        print("=== Stage 2: MultiRobotsPSO ===")
        for it in range(self.n_iterations):
            scores = self.evaluate(self.positions)

            # pbest
            better_mask = scores < self.pbest_scores
            self.pbest_positions[better_mask] = self.positions[better_mask].copy()
            self.pbest_scores[better_mask] = scores[better_mask]

            # gbest
            min_idx = np.argmin(scores)
            if scores[min_idx] < self.gbest_score:
                self.gbest_score = scores[min_idx]
                self.gbest_position = self.positions[min_idx].copy()

            # PSO eq
            r1 = np.random.rand(*self.positions.shape)
            r2 = np.random.rand(*self.positions.shape)
            cognitive = self.c1 * r1 * (self.pbest_positions - self.positions)
            social    = self.c2 * r2 * (self.gbest_position - self.positions)
            self.velocities = self.w * self.velocities + cognitive + social
            self.positions += self.velocities

            # clip
            self.positions = np.clip(self.positions, self.bounds[0], self.bounds[1])
            # wymuszenie start/end
            for p in range(self.n_particles):
                for r in range(self.n_robots):
                    self.positions[p, r, 0] = self.starts[r]
                    self.positions[p, r, -1] = self.ends[r]

            print(f"   [MultiPSO] Iter {it+1}/{self.n_iterations}, best_score={self.gbest_score:.2f}")

    def plot_best(self):
        """
        Rysuje terrain + gbest_position
        """
        if self.gbest_position is None:
            print("Brak best_position")
            return
        plt.imshow(self.terrain, origin="lower", cmap="terrain")
        plt.colorbar(label="Terrain")
        for r in range(self.n_robots):
            path = self.gbest_position[r]
            plt.plot(path[:,1], path[:,0], label=f"Robot_{r}")
        # start/end
        for r in range(self.n_robots):
            plt.scatter(self.starts[r][1], self.starts[r][0], color="blue")
            plt.scatter(self.ends[r][1],   self.ends[r][0],   color="red")
        plt.title(f"MultiPSO best_score={self.gbest_score:.2f}")
        plt.legend()
        plt.show()

###############################################################################
# 3. Dodajemy random search/grid search do optymalizacji w, c1, c2
###############################################################################
def random_search_params(
    param_ranges,
    # paramy do MultiRobotsPSO
    n_particles=10,
    n_robots=3,
    n_dimensions=8,
    bounds=(0,49),
    n_iterations=50,
    terrain=None,
    starts=None,
    ends=None,
    single_particles=10,
    single_iter=30,
    trials=5
):
    """
    Losowo generujemy (w, c1, c2) i uruchamiamy MultiRobotsPSO (który wewn. wywołuje SinglePSO).
    Wybieramy najlepszy wynik.
    """
    best_params = None
    best_score = np.inf

    for t in range(trials):
        w_  = np.random.uniform(*param_ranges['w'])
        c1_ = np.random.uniform(*param_ranges['c1'])
        c2_ = np.random.uniform(*param_ranges['c2'])

        multi_pso = MultiRobotsPSO(
            n_particles=n_particles,
            n_robots=n_robots,
            n_dimensions=n_dimensions,
            bounds=bounds,
            n_iterations=n_iterations,
            terrain=terrain,
            starts=starts,
            ends=ends,
            single_particles=single_particles,
            single_iter=single_iter,
            w=w_,
            c1=c1_,
            c2=c2_
        )
        multi_pso.update()
        if multi_pso.gbest_score < best_score:
            best_score = multi_pso.gbest_score
            best_params = (w_, c1_, c2_)

    return best_params, best_score

###############################################################################
# 4. PRZYKŁAD UŻYCIA
###############################################################################
if __name__ == "__main__":
    terrain = terrain_generator(terrain_size=(50,50), terrain_type="hills")

    starts = [(5,5),   (10,10),  (40,10)]
    ends   = [(45,40), (35,40),  (10,45)]
    n_robots = 3

    # Wprost wywołanie MultiRobotsPSO:
    print("=== MultiRobotsPSO with single calls inside ===")
    multi_pso = MultiRobotsPSO(
        n_particles=10,
        n_robots=n_robots,
        n_dimensions=8,
        bounds=(0,49),
        n_iterations=50,
        terrain=terrain,
        starts=starts,
        ends=ends,
        single_particles=8,  # paramy do SinglePSO
        single_iter=50,
        w=0.5, c1=1.5, c2=1.5
    )
    multi_pso.update()
    print("Final best score =", multi_pso.gbest_score)
    multi_pso.plot_best()

    # Przykład: random search w, c1, c2
    print("\n=== Random search for (w, c1, c2) ===")
    param_ranges = {
        'w':  (0.3, 0.9),
        'c1': (1.0, 2.5),
        'c2': (1.0, 2.5)
    }
    best_params, best_val = random_search_params(
        param_ranges=param_ranges,
        n_particles=10,
        n_robots=n_robots,
        n_dimensions=8,
        bounds=(0,49),
        n_iterations=50,
        terrain=terrain,
        starts=starts,
        ends=ends,
        single_particles=10,
        single_iter=50,
        trials=10
    )
    print("Best params from random search =", best_params, "score=", best_val)
