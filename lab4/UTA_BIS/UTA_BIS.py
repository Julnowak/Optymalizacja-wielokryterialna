import numpy as np


# Funkcja do znajdowania min i max dla każdego kryterium
def find_minmax_criteria(A):
    min_gi = [min(A[:, i]) for i in range(len(A[0]))]
    max_gi = [max(A[:, i]) for i in range(len(A[0]))]
    return min_gi, max_gi


# Funkcja do obliczania cząstkowych użyteczności z iteracyjnym dopasowaniem
def calc_partial_utilities_bis(A, min_gi, max_gi, minmax, weights, epsilon=1e-3):
    """
    Obliczanie cząstkowych użyteczności dla UTA BIS.
    """
    num_variants, num_criteria = A.shape
    U = np.zeros((num_variants, num_criteria))
    for k in range(num_criteria):
        for a in range(num_variants):
            value = (A[a, k] - min_gi[k]) / (max_gi[k] - min_gi[k])
            if minmax[k]:
                U[a, k] = value * weights[k]
            else:
                U[a, k] = (1 - value) * weights[k]

    # Normalizacja funkcji użyteczności w UTA BIS (iteracyjne dopasowanie)
    for k in range(num_criteria):
        u_min = min(U[:, k])
        u_max = max(U[:, k])
        if u_max - u_min > epsilon:
            U[:, k] = (U[:, k] - u_min) / (u_max - u_min) * weights[k]
    return U


# Obliczanie łącznej użyteczności dla każdego wariantu
def calc_total_utilities(U):
    utilities = np.sum(U, axis=1)
    return utilities


# Sortowanie wariantów według użyteczności
def rank_variants(utilities):
    sorted_indices = np.argsort(-utilities)
    return sorted_indices


# Implementacja metody UTA BIS
def UTA_BIS(A, minmax, weights=[], epsilon=1e-3):
    """
    Implementacja metody UTA BIS.
    :param A: Macierz alternatyw (warianty x kryteria).
    :param minmax: Lista określająca, czy kryterium jest do maksymalizacji (True) lub minimalizacji (False).
    :param weights: Wagi kryteriów.
    :param epsilon: Tolerancja dla dopasowania funkcji użyteczności.
    :return: Ranking alternatyw.
    """
    num_criteria = len(minmax)
    if not weights:
        weights = [1 / num_criteria] * num_criteria  # Równomierne wagi

    # Znajdowanie minimalnych i maksymalnych wartości dla każdego kryterium
    min_g, max_g = find_minmax_criteria(A)
    print("Min_g: {}\nMax_g: {}".format(min_g, max_g))

    # Obliczanie cząstkowych użyteczności z iteracyjnym dopasowaniem
    U = calc_partial_utilities_bis(A, min_g, max_g, minmax, weights, epsilon)
    print("\nCząstkowe użyteczności: \n{}".format(U))

    # Obliczanie całkowitej użyteczności dla każdego wariantu
    total_utilities = calc_total_utilities(U)
    print("\nŁączne użyteczności: \n{}".format(total_utilities))

    # Sortowanie wariantów
    ranking = rank_variants(total_utilities)
    return ranking


# Przykład użycia metody UTA BIS
if __name__ == "__main__":
    A = np.array([
        [12, 0.01024, 24.0646],
        [1, 0.00026, 62.1609],
        [4, 0.02004, 24.1212],
        [1, -0.27064, 23.2374],
        [2, 0.00476, 0.0327],
        [1, 0.11461, 33.8748]
    ])

    A = np.array([
        [12, 12, 12],
        [7, 8, 7],
        [6, 7, 6],
        [5, 6, 5],
        [4, 5, 4],
        [3, 4, 3]
    ])
    minmax = [False, False, False]  # Maksymalizacja dla kryteriów 1 i 3, minimalizacja dla kryterium 2
    criteria = ["Liquidity", "Beta", "Return"]
    weights = [0.4, 0.3, 0.3]  # Wagi kryteriów

    ranking = UTA_BIS(A, minmax, weights)
    print("\nRanking alternatyw (UTA BIS):")
    print(ranking)
