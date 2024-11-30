import matplotlib.pyplot as plt
import numpy as np


def fuzzy_to_crisp(fuzzy_num):
    """Konwertuje liczbę rozmytą (trójkątną) do wartości skalarnej (środek ciężkości)."""
    return sum(fuzzy_num) / 3


# Normalizacja macierzy decyzyjnej
def normalize(matrix, criteria_types):
    """
    Normalizuje macierz decyzji dla każdego kryterium.
    criteria_types: lista typów kryteriów ('max' lub 'min').
    """
    normalized_matrix = []
    for j, crit_type in enumerate(criteria_types):
        column = np.array([fuzzy_to_crisp(row[j]) for row in matrix])
        if crit_type == "max":
            max_val = np.max(column)
            normalized_matrix.append(column / max_val)
        elif crit_type == "min":
            min_val = np.min(column)
            normalized_matrix.append(min_val / column)
    return np.array(normalized_matrix).T


# Wyznaczanie odległości i rankingów
def fuzzy_topsis(matrix, criteria_weights, criteria_types):
    """
    Implementacja metody Fuzzy TOPSIS.
    matrix: macierz decyzji (alternatywy × kryteria) w liczbach rozmytych.
    criteria_weights: wagi kryteriów.
    criteria_types: typy kryteriów ('max' lub 'min').
    """
    normalized_matrix = normalize(matrix, criteria_types)

    # Krok 3: Wyważona macierz normalizacyjna
    weighted_matrix = normalized_matrix * np.array(criteria_weights)

    # Krok 4: Określenie ideału pozytywnego i negatywnego
    ideal_positive = np.max(weighted_matrix, axis=0)
    ideal_negative = np.min(weighted_matrix, axis=0)

    # Krok 5: Obliczanie odległości
    distances_to_positive = np.linalg.norm(weighted_matrix - ideal_positive, axis=1)
    distances_to_negative = np.linalg.norm(weighted_matrix - ideal_negative, axis=1)

    # Krok 6: Wyznaczenie bliskości do ideału
    closeness_coefficients = distances_to_negative / (distances_to_positive + distances_to_negative)

    return closeness_coefficients


if __name__ == '__main__':

    # Przykładowe dane
    # Alternatywy z 4 kryteriami w formacie trójkątnych liczb rozmytych (L, M, U)
    # decision_matrix = [
    #     [(3, 5), (2, 3), (6, 7), (4, 6)],  # A1
    #     [(4, 5), (1, 2), (7, 8), (5, 7)],  # A2
    #     [(2, 3), (3, 4), (5, 6), (3, 5)],  # A3
    #     [(5, 6), (2, 3), (8, 9), (4, 6)]  # A4
    # ]

    decision_matrix = [
        [(3, 5), (2, 3), (6, 7), (4, 6)],  # A1
        [(4, 5), (1, 2), (7, 8), (5, 7)],  # A2
    ]

    # Wagi kryteriów
    weights = [0.3, 0.2, 0.4, 0.1]  # Suma wag = 1

    # Typy kryteriów ('max' dla maksymalizacji, 'min' dla minimalizacji)
    criteria_types = ['max', 'min', 'max', 'max']

    # Obliczanie Fuzzy TOPSIS
    closeness = fuzzy_topsis(decision_matrix, weights, criteria_types)

    # Wyniki
    print("Współczynniki bliskości dla alternatyw:")
    for i, coeff in enumerate(closeness, 1):
        print(f"A{i}: {coeff:.4f}")

    # Najlepsza alternatywa
    best_alternative = np.argmax(closeness) + 1
    print(f"Najlepsza alternatywa: A{best_alternative}")

    plt.plot(decision_matrix)


