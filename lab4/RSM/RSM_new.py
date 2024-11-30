from typing import List, Tuple

import numpy as np


def rsm_continuous(
        num_samples: int, bounds: List[Tuple[float, float]], reference_points: List[float]
):
    """
    Reference Set Method (RSM) w wariancie ciągłym.
    :param num_samples: liczba próbek.
    :param bounds: lista krotek (min, max) dla każdego kryterium.
    :param reference_points: punkt referencyjny w przestrzeni kryteriów.
    :return: Zbiór punktów z obliczonymi odległościami do punktu referencyjnego.
    """
    # Generowanie próbek w przestrzeni decyzyjnej
    samples = [np.linspace(b[0], b[1], num_samples) for b in bounds]
    samples_mesh = np.array(np.meshgrid(*samples)).T.reshape(-1, len(bounds))

    # Obliczanie odległości punktów od referencyjnych
    distances = [
        (point, np.linalg.norm(np.array(point) - np.array(reference_points)))
        for point in samples_mesh
    ]

    # Sortowanie punktów według odległości (rosnąco)
    distances.sort(key=lambda x: x[1])
    return distances


def rsm_discrete(alternatives: List[List[float]], reference_point: List[float]):
    """
    Reference Set Method (RSM) w wariancie dyskretnym.
    :param alternatives: lista alternatyw w przestrzeni decyzyjnej.
    :param reference_point: punkt referencyjny.
    :return: Zbiór punktów z obliczonymi odległościami do punktu referencyjnego.
    """
    distances = [
        (alt, np.linalg.norm(np.array(alt) - np.array(reference_point)))
        for alt in alternatives
    ]

    # Sortowanie punktów według odległości (rosnąco)
    distances.sort(key=lambda x: x[1])
    return distances


# Przykład wariantu ciągłego
if __name__ == "__main__":
    bounds_continuous = [(3, 1), (2, 1), (4, 4), (6, 7)]  # U ⊂ R⁴
    reference_point = [0.5, 0.5, 0.5, 0.5]  # Punkt referencyjny
    num_samples = 10

    # Obliczanie punktów i ich odległości
    continuous_results = rsm_continuous(num_samples, bounds_continuous, reference_point)

    print("Punkty w wariancie ciągłym (posortowane według odległości):")
    for point, distance in continuous_results[:10]:  # Wyświetl tylko pierwsze 10
        print(f"Point: {np.round(point, 4)}, Distance: {distance:.4f}")

    # Dane dla N=3
    alternatives_3 = [
        [3, 5, 1],
        [4, 4, 2],
        [5, 3, 3],
    ]
    reference_point_3 = [4, 4, 2]  # Punkt referencyjny

    discrete_results_3 = rsm_discrete(alternatives_3, reference_point_3)
    print("\nPunkty w wariancie dyskretnym dla N=3:")
    for point, distance in discrete_results_3:
        print(f"Point: {point}, Distance: {distance:.4f}")

    # Dane dla N=4
    alternatives_4 = [
        [2, 7, 4],
        [3, 5, 6],
        [1, 8, 5],
        [4, 3, 7],
    ]
    reference_point_4 = [3, 5, 6]  # Punkt referencyjny

    discrete_results_4 = rsm_discrete(alternatives_4, reference_point_4)
    print("\nPunkty w wariancie dyskretnym dla N=4:")
    for point, distance in discrete_results_4:
        print(f"Point: {point}, Distance: {distance:.4f}")