import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Funkcja do znajdowania minimalnych i maksymalnych wartości dla każdego kryterium
def find_minmax_criteria(A):
    min_gi = np.min(A, axis=0)  # Minimalne wartości dla każdego kryterium
    max_gi = np.max(A, axis=0)  # Maksymalne wartości dla każdego kryterium
    return min_gi, max_gi


# Funkcja do obliczania cząstkowych użyteczności
def calc_partial_utilities_dis(A, min_gi, max_gi, minmax, weights):
    """
    Obliczanie cząstkowych użyteczności dla UTA-DIS.
    """
    num_variants, num_criteria = A.shape
    U = np.zeros((num_variants, num_criteria))  # Macierz użyteczności cząstkowych

    for k in range(num_criteria):
        for a in range(num_variants):
            # Normalizacja wartości kryteriów do zakresu [0, 1]
            value = (A[a, k] - min_gi[k]) / (max_gi[k] - min_gi[k])

            # Dopasowanie w zależności od minimalizacji/maksymalizacji
            if minmax[k]:  # Maksymalizacja
                U[a, k] = value * weights[k]
            else:  # Minimalizacja
                U[a, k] = (1 - value) * weights[k]

    return U


# Funkcja obliczająca całkowitą użyteczność dla każdego wariantu
def calc_total_utilities(U):
    utilities = np.sum(U, axis=1)  # Suma użyteczności cząstkowych dla każdego wariantu
    return utilities


# Funkcja do przypisywania kategorii na podstawie progów
def classify_categories(total_utilities, thresholds):
    """
    Klasyfikacja alternatyw do kategorii na podstawie progów.
    :param total_utilities: Wektor całkowitych użyteczności alternatyw.
    :param thresholds: Lista progów definiujących granice kategorii.
    :return: Lista kategorii dla każdej alternatywy.
    """
    categories = []
    for utility in total_utilities:
        for i, threshold in enumerate(thresholds):
            if utility <= threshold:
                categories.append(i + 1)
                break
        else:
            categories.append(len(thresholds) + 1)
    return categories


# Implementacja metody UTA-DIS
def UTA_DIS(A, minmax, weights=None, thresholds=None):
    """
    Implementacja metody UTA-DIS.
    :param A: Macierz alternatyw (warianty x kryteria).
    :param minmax: Lista True (maksymalizacja) lub False (minimalizacja) dla każdego kryterium.
    :param weights: Wagi kryteriów (opcjonalne).
    :param thresholds: Lista progów definiujących granice kategorii (opcjonalne).
    :return: Kategorie przypisane do każdej alternatywy.
    """
    num_criteria = A.shape[1]
    if weights is None:
        weights = [1 / num_criteria] * num_criteria  # Równomierne wagi domyślne

    # Znajdowanie minimalnych i maksymalnych wartości dla każdego kryterium
    min_g, max_g = find_minmax_criteria(A)

    # Obliczanie cząstkowych użyteczności
    U = calc_partial_utilities_dis(A, min_g, max_g, minmax, weights)

    # Obliczanie całkowitej użyteczności
    total_utilities = calc_total_utilities(U)

    # Przypisywanie kategorii na podstawie progów
    if thresholds is None:
        raise ValueError("Progi (thresholds) muszą być zdefiniowane dla metody UTA-DIS.")
    categories = classify_categories(total_utilities, thresholds)

    return categories, total_utilities


def visualize(data, utilities, criterion1=0, criterion2=1, criterion3=2):
    """
    Wizualizuje punkty danych w przestrzeni trzech wybranych kryteriów.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')  # Dodanie wykresu 3D

    # Wykres punktów
    sc = ax.scatter(
        data[:, criterion1],
        data[:, criterion2],
        data[:, criterion3],
        c=utilities,
        cmap='viridis',
        edgecolor='k',
        s=100
    )

    # Dodanie skali kolorów
    plt.colorbar(sc, label="Użyteczność")

    # Opis osi
    ax.set_xlabel(f"Kryterium {criterion1 + 1}")
    ax.set_ylabel(f"Kryterium {criterion2 + 1}")
    ax.set_zlabel(f"Kryterium {criterion3 + 1}")
    ax.set_title("Wizualizacja punktów danych w przestrzeni trzech kryteriów")

    fig.show()
    plt.show()


# Przykład użycia
if __name__ == "__main__":
    # Macierz alternatyw (wartości dla 3 kryteriów)
    A = np.array([
        [12, 0.01024, 24.0646],
        [1, 0.00026, 62.1609],
        [4, 0.02004, 24.1212],
        [1, -0.27064, 23.2374],
        [2, 0.00476, 0.0327],
        [1, 0.11461, 33.8748]
    ])

    # A = np.array([
    #     [12, 12, 12],
    #     [7, 8, 7],
    #     [6, 7, 6],
    #     [5, 6, 5],
    #     [4, 5, 4],
    #     [3, 4, 3]
    # ])

    # Maksymalizacja dla 1. i 3. kryterium, minimalizacja dla 2.
    minmax = [True, False, True]

    # Wagi kryteriów
    weights = [0.4, 0.3, 0.3]

    # Progi definiujące kategorie
    thresholds = [0.3, 0.5, 0.7]

    # Klasyfikacja alternatyw do kategorii
    categories, total_utilities = UTA_DIS(A, minmax, weights, thresholds)
    print("\nCałkowite użyteczności alternatyw:")
    print(total_utilities)
    print("\nPrzypisane kategorie:")
    print(categories)

    visualize(A, total_utilities)

