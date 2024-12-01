import numpy as np

def fuzzy_topsis(decision_matrix, weights, criteria):
    """
    decision_matrix: macierz decyzyjna (alternatywy x kryteria) w formie liczb rozmytych [(l, m, u)]
    weights: lista wag dla każdego kryterium
    criteria: lista znaków ('max' lub 'min') dla kryteriów
    """
    # Normalizacja macierzy decyzyjnej
    normalized = []
    for j in range(len(criteria)):
        col = [x[j][1] for x in decision_matrix]  # Środkowa wartość
        if criteria[j] == 'max':
            divisor = max(col)
        else:
            divisor = min(col)
        normalized.append([(x[0] / divisor, x[1] / divisor, x[2] / divisor) for x in decision_matrix[:, j]])
    normalized = np.array(normalized).T

    # Obliczanie punktów idealnych i anty-idealnych
    ideal = np.max(normalized, axis=0)
    anti_ideal = np.min(normalized, axis=0)

    # Obliczanie odległości od punktów
    dist_ideal = np.sqrt(np.sum((normalized[:, 1] - ideal[1])**2, axis=1))
    dist_anti_ideal = np.sqrt(np.sum((normalized[:, 1] - anti_ideal[1])**2, axis=1))

    # Współczynnik podobieństwa
    scores = dist_anti_ideal / (dist_ideal + dist_anti_ideal)
    return scores

# Przykład użycia
decision_matrix = np.array([
    [(2, 3, 4), (3, 4, 5)],  # Alternatywa 1
    [(4, 5, 6), (2, 3, 4)],  # Alternatywa 2
])
weights = [0.5, 0.5]
criteria = ['max', 'min']
scores = fuzzy_topsis(decision_matrix, weights, criteria)
print("Ranking:", scores)

import numpy as np

def utabis(alternatives, utility_values):
    """
    alternatives: macierz alternatyw (m x n)
    utility_values: funkcje użyteczności dla punktów odniesienia
    """
    # Ekstrapolacja funkcji użyteczności
    weights = np.linalg.lstsq(alternatives, utility_values, rcond=None)[0]
    scores = alternatives @ weights
    return scores

# Przykład użycia
alternatives = np.array([[1, 2], [3, 4], [2, 3]])
utility_values = np.array([0.3, 0.7, 0.5])  # Znane wartości użyteczności
scores = utabis(alternatives, utility_values)
print("Ranking:", scores)