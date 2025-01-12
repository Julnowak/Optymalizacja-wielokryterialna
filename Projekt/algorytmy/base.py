import random


# Funkcja celu
def objective_function(x):
    # Przykładowa funkcja celu: x^2 (minimalizacja)
    return sum([xi ** 2 for xi in x])


# Inicjalizacja parametryczna PSO
def pso(num_particles, dimensions, max_iterations, bounds, w=0.5, c1=0.5, c2=0.5):
    # Inicjalizacja roju
    particles = [{'position': [random.uniform(bounds[0], bounds[1]) for _ in range(dimensions)],
                  'velocity': [random.uniform(-1, 1) for _ in range(dimensions)],
                  'best_position': None,
                  'best_value': float('inf')}
                 for _ in range(num_particles)]

    # Najlepsza globalna pozycja i wartość
    global_best_position = None
    global_best_value = float('inf')

    # Główna pętla PSO
    for iteration in range(max_iterations):
        for particle in particles:
            # Aktualna wartość funkcji celu
            fitness_value = objective_function(particle['position'])

            # Aktualizacja najlepszej lokalnej pozycji
            if fitness_value < particle['best_value']:
                particle['best_value'] = fitness_value
                particle['best_position'] = particle['position'][:]

            # Aktualizacja najlepszej globalnej pozycji
            if fitness_value < global_best_value:
                global_best_value = fitness_value
                global_best_position = particle['position'][:]

        # Aktualizacja pozycji i prędkości cząstek
        for particle in particles:
            for d in range(dimensions):
                r1 = random.random()
                r2 = random.random()

                # Równanie aktualizacji prędkości
                particle['velocity'][d] = (w * particle['velocity'][d] +
                                           c1 * r1 * (particle['best_position'][d] - particle['position'][d]) +
                                           c2 * r2 * (global_best_position[d] - particle['position'][d]))

                # Równanie aktualizacji pozycji
                particle['position'][d] += particle['velocity'][d]

                # Zastosowanie ograniczeń pozycji
                if particle['position'][d] < bounds[0]:
                    particle['position'][d] = bounds[0]
                elif particle['position'][d] > bounds[1]:
                    particle['position'][d] = bounds[1]

        # Wyświetlanie postępu
        print(f"Iteracja {iteration + 1}/{max_iterations}, najlepsza wartość globalna: {global_best_value}")

    return global_best_position, global_best_value


# Parametry PSO
num_particles = 30
dimensions = 2
max_iterations = 50
bounds = (-10, 10)

# Uruchomienie algorytmu PSO
best_position, best_value = pso(num_particles, dimensions, max_iterations, bounds)
print(f"\nNajlepsza pozycja: {best_position}")
print(f"Najlepsza wartość: {best_value}")
