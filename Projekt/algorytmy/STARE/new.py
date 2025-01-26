import numpy as np
import random
import heapq
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def generate_random_solution(map, start, end, num_robots):
    """
    Generuje losowe rozwiązanie, czyli zestaw ścieżek dla wszystkich robotów.

    Args:
        map: Macierz reprezentująca mapę terenu
        start: Punkt początkowy
        end: Punkt końcowy
        num_robots: Liczba robotów

    Returns:
        List: Lista ścieżek, gdzie każda ścieżka jest listą współrzędnych.
    """

    solutions = []
    for _ in range(num_robots):
        path = [start]
        while path[-1] != end:
            neighbors = get_neighbors(path[-1], map.shape)
            next_step = random.choice(neighbors)
            path.append(next_step)
        solutions.append(path)
    return solutions

def get_neighbors(node, shape):
    """
    Zwraca listę sąsiadów dla danego węzła.

    Args:
        node: Tuple reprezentujący współrzędne węzła
        shape: Tuple reprezentujący kształt mapy

    Returns:
        List: Lista sąsiadów
    """

    x, y = node
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    neighbors = [n for n in neighbors if 0 <= n[0] < shape[0] and 0 <= n[1] < shape[1]]
    return neighbors


def evaluate_solution(map, solution, dist):
    """
    Oblicza wartość funkcji celu dla danego rozwiązania.

    Args:
        map: Macierz reprezentująca mapę terenu
        solution: Lista ścieżek
        dist: Minimalny dystans między robotami

    Returns:
        float: Wartość funkcji celu
    """

    total_distance = 0
    for path in solution:
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            total_distance += map[x1, y1]  # Zakładamy, że wartość w mapie reprezentuje koszt przejścia

    # Dodaj karę za naruszenie minimalnego dystansu
    penalty = 0
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            if min_distance(solution[i], solution[j]) < dist:
                penalty += 1

    return total_distance + penalty * 100  # Dostosuj wagę kary


def min_distance(path1, path2):
    """
    Oblicza minimalną odległość między dwoma ścieżkami.

    Args:
        path1: Pierwsza ścieżka
        path2: Druga ścieżka

    Returns:
        float: Minimalna odległość
    """

    # Implementacja obliczenia minimalnej odległości (np. korzystając z algorytmu dynamicznego programowania)

def create_vectors(fitness_values, num_vectors):
    """
    Tworzy `num_vectors` wektorów, które dzielą przestrzeń wartości celu na różne regiony.

    Args:
        fitness_values: Lista wartości funkcji celu
        num_vectors: Liczba wektorów

    Returns:
        List: Lista wektorów
    """

    min_value = min(fitness_values)
    max_value = max(fitness_values)
    vectors = []
    for _ in range(num_vectors):
        vector = random.uniform(min_value, max_value)
        vectors.append(vector)
    return vectors

def select_individuals(fitness_values, vector):
    """
    Wybiera osobniki, których wartość funkcji celu jest najbliższa wartości wektora.

    Args:
        fitness_values: Lista wartości funkcji celu
        vector: Wartość wektora

    Returns:
        List: Lista indeksów wybranych osobników
    """

    distances = [abs(value - vector) for value in fitness_values]
    sorted_indices = np.argsort(distances)
    # Wybierz np. 20% najlepszych osobników dla każdego wektora
    num_select = int(0.2 * len(fitness_values))
    return sorted_indices[:num_select]

def crossover_and_mutation(population, crossover_rate, mutation_rate):
    """
    Wykonuje operacje krzyżowania i mutacji na populacji.

    Args:
        population: Lista rozwiązań
        crossover_rate: Prawdopodobieństwo krzyżowania
        mutation_rate: Prawdopodobieństwo mutacji

    Returns:
        List: Nowa populacja po zastosowaniu operatorów genetycznych.
    """

    new_population = []
    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i+1]

        # Krzyżowanie
        if random.random() < crossover_rate:
            child1, child2 = crossover(parent1, parent2)
        else:
            child1, child2 = parent1, parent2

        # Mutacja
        child1 = mutation(child1, mutation_rate)
        child2 = mutation(child2, mutation_rate)

        new_population.append(child1)
        new_population.append(child2)

    return new_population

def crossover(parent1, parent2):
    """
    Wykonuje krzyżowanie jedno-punktowe.

    Args:
        parent1: Pierwszy rodzic
        parent2: Drugi rodzic

    Returns:
        tuple: Dwoje dzieci
    """

    crossover_point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutation(individual, mutation_rate):
    """
    Wykonuje mutację poprzez losową zmianę jednego elementu.

    Args:
        individual: Indywidualne rozwiązanie
        mutation_rate: Prawdopodobieństwo mutacji

    Returns:
        List: Zmutowane rozwiązanie
    """

    for i in range(len(individual)):
        if random.random() < mutation_rate:
            # Zmień ostatni element ścieżki na losowego sąsiada
            neighbors = get_neighbors(individual[i], map.shape)
            individual[i] = random.choice(neighbors)
    return individual

import numpy as np
import random

def vega(map, start, end, num_robots, dist, max_iter, pop_size, num_vectors, crossover_rate, mutation_rate):
    """
    Implementacja algorytmu VEGA dla problemu wielu robotów

    Args:
        map: Macierz reprezentująca mapę terenu
        start: Punkt początkowy
        end: Punkt końcowy
        num_robots: Liczba robotów
        dist: Minimalny dystans między robotami
        max_iter: Maksymalna liczba iteracji
        pop_size: Rozmiar populacji
        num_vectors: Liczba wektorów wartości celu
        crossover_rate: Prawdopodobieństwo krzyżowania
        mutation_rate: Prawdopodobieństwo mutacji
    """

    # Inicjalizacja populacji
    population = [generate_random_solution(map, start, end, num_robots) for _ in range(pop_size)]

    for generation in range(max_iter):
        # Ewaluacja populacji
        fitness_values = [evaluate_solution(map, solution, dist) for solution in population]

        # Tworzenie wektorów wartości celu
        vectors = create_vectors(fitness_values, num_vectors)

        # Selekcja
        new_population = []
        for vector in vectors:
            selected_indices = select_individuals(fitness_values, vector)
            for index in selected_indices:
                new_population.append(population[index])

        # Krzyżowanie i mutacja
        new_population = crossover_and_mutation(new_population, crossover_rate, mutation_rate)

        # Zamiana populacji
        population = new_population

    # Znajdowanie najlepszego rozwiązania
    best_index = np.argmin(fitness_values)
    best_solution = population[best_index]

    return best_solution

# Przykład użycia
map_size = 11
map = np.random.rand(map_size, map_size)  # Przykładowa mapa
start = (0, 0)
end = (10, 10)
num_robots = 4
dist = 2
max_iter = 1000

best_paths, costs, pareto_data = vega(map, start, end, num_robots, dist, max_iter, pop_size=1000, num_vectors=10, crossover_rate=0.3, mutation_rate=0.2)

print("Najlepsze ścieżki:")
for path in best_paths:
    print(path)

print("Koszty:")
print(costs)