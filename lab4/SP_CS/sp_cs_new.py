from typing import Tuple, List

import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d


def sp_cs_continuous(
        num_samples: int, bounds: List[Tuple[float, float]], status_quo: List[float], aspirations: List[float]
):
    """
    Safety Principle-Based Ranking and Compromise Selection (SP-CS) - wariant ciągły.
    :param num_samples: liczba próbek.
    :param bounds: lista krotek (min, max) dla każdego kryterium.
    :param status_quo: punkt status quo (punkt początkowy łamanej γ).
    :param aspirations: punkt aspiracji (punkt końcowy łamanej γ).
    :return: Ranking punktów w przestrzeni decyzyjnej.
    """
    # Generowanie próbek w przestrzeni U ⊂ R⁴
    samples = [np.linspace(b[0], b[1], num_samples) for b in bounds]
    decision_points = np.array(np.meshgrid(*samples)).T.reshape(-1, len(bounds))

    # Tworzenie łamanej γ łączącej status_quo z aspirations
    gamma = [np.linspace(status_quo[i], aspirations[i], num_samples) for i in range(len(status_quo))]
    gamma_points = np.array(gamma).T

    # Obliczanie odległości punktów od łamanej γ
    scores = []
    for point in decision_points:
        min_score = float("inf")
        for i, gamma_point in enumerate(gamma_points):
            chebyshev_dist = np.max(np.abs(point - gamma_point))  # Metryka Czebyszewa
            param_t = i / (len(gamma_points) - 1)  # Parametr t
            score = param_t + chebyshev_dist
            min_score = min(min_score, score)
        scores.append((point, min_score))

    # Sortowanie punktów według funkcji scoringowej
    scores.sort(key=lambda x: x[1])
    return scores


def sp_cs_discrete(
        alternatives: List[List[float]], status_quo: List[float], aspirations: List[float]
):
    """
    Safety Principle-Based Ranking and Compromise Selection (SP-CS) - wariant dyskretny.
    :param alternatives: lista alternatyw w przestrzeni decyzyjnej.
    :param status_quo: punkt status quo.
    :param aspirations: punkt aspiracji.
    :return: Ranking alternatyw.
    """
    # Tworzenie łamanej γ łączącej status_quo z aspirations
    num_samples = len(alternatives)
    gamma = [np.linspace(status_quo[i], aspirations[i], num_samples) for i in range(len(status_quo))]
    gamma_points = np.array(gamma).T

    # Obliczanie odległości punktów od łamanej γ
    scores = []
    for alt in alternatives:
        min_score = float("inf")
        for i, gamma_point in enumerate(gamma_points):
            chebyshev_dist = np.max(np.abs(np.array(alt) - gamma_point))  # Metryka Czebyszewa
            param_t = i / (len(gamma_points) - 1)  # Parametr t
            score = param_t + chebyshev_dist
            min_score = min(min_score, score)
        scores.append((alt, min_score))

    # Sortowanie punktów według funkcji scoringowej
    scores.sort(key=lambda x: x[1])
    return scores


# Przykład użycia dla wariantu ciągłego
if __name__ == "__main__":
    bounds_continuous = [(0, 1), (0, 1), (0, 1), (0, 1)]  # U ⊂ R⁴
    status_quo_point = [0.2, 0.2, 0.2, 0.2]
    aspirations_point = [0.8, 0.8, 0.8, 0.8]
    num_samples = 10

    # Obliczanie rankingów punktów
    continuous_results = sp_cs_continuous(
        num_samples, bounds_continuous, status_quo_point, aspirations_point
    )

    print("Ranking punktów w wariancie ciągłym (posortowane według funkcji scoringowej):")
    for point, score in continuous_results[:10]:  # Wyświetl tylko pierwsze 10
        print(f"Point: {np.round(point, 4)}, Score: {score:.4f}")

    # Dane dla N = 3
    alternatives_3 = [
        [3, 5, 1],
        [4, 4, 2],
        [5, 3, 3],
    ]
    status_quo_3 = [2, 4, 1]
    aspirations_3 = [6, 6, 4]

    discrete_results_3 = sp_cs_discrete(alternatives_3, status_quo_3, aspirations_3)
    print("\nRanking alternatyw w wariancie dyskretnym dla N=3:")
    for point, score in discrete_results_3:
        print(f"Point: {point}, Score: {score:.4f}")

    # Dane dla N = 4
    alternatives_4 = [
        [2, 7, 4],
        [3, 5, 6],
        [1, 8, 5],
        [4, 3, 7],
    ]
    status_quo_4 = [2, 5, 4]
    aspirations_4 = [5, 9, 7]

    discrete_results_4 = sp_cs_discrete(alternatives_4, status_quo_4, aspirations_4)
    print("\nRanking alternatyw w wariancie dyskretnym dla N=4:")
    for point, score in discrete_results_4:
        print(f"Point: {point}, Score: {score:.4f}")
