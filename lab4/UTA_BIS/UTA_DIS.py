import numpy as np
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# Funkcja do znajdowania minimalnych i maksymalnych wartości dla każdego kryterium
def find_minmax_criteria(A):
    min_gi = np.min(A, axis=0)
    max_gi = np.max(A, axis=0)
    return min_gi, max_gi


# Funkcja do obliczania cząstkowych użyteczności
def calc_partial_utilities_dis(A, min_gi, max_gi, minmax, weights):
    num_variants, num_criteria = A.shape
    U = np.zeros((num_variants, num_criteria))

    for k in range(num_criteria):
        for a in range(num_variants):
            range_value = max_gi[k] - min_gi[k]
            if range_value == 0:
                value = 0.5  # Jeżeli min = max, przyjmujemy wartość pośrednią
            else:
                value = (A[a, k] - min_gi[k]) / range_value

            if minmax[k]:  # Maksymalizacja
                U[a, k] = value * weights[k]
            else:  # Minimalizacja
                U[a, k] = (1 - value) * weights[k]
    return U


# Funkcja obliczająca całkowitą użyteczność
def calc_total_utilities(U):
    return np.sum(U, axis=1)


# Klasyfikacja do kategorii
def classify_categories(total_utilities, thresholds):
    categories = []
    for utility in total_utilities:
        for i, threshold in enumerate(thresholds):
            if utility <= threshold:
                categories.append(i + 1)
                break
        else:
            categories.append(len(thresholds) + 1)
    return categories


# UTA-DIS
def UTA_DIS(A, minmax, weights=None, thresholds=None):
    """
    Funkcja UTA-DIS dla wariantu dyskretnego.
    """
    num_criteria = A.shape[1]
    if weights is None:
        weights = [1 / num_criteria] * num_criteria

    min_g, max_g = find_minmax_criteria(A)

    # Obliczanie cząstkowych użyteczności
    U = calc_partial_utilities_dis(A, min_g, max_g, minmax, weights)

    # Obliczanie całkowitych użyteczności
    total_utilities = calc_total_utilities(U)

    # Jeśli progi są zdefiniowane, klasyfikacja do kategorii
    if thresholds is not None:
        categories = classify_categories(total_utilities, thresholds)
    else:
        categories = None

    return categories, total_utilities


def calc_partial_utilities_continuous(A, min_gi, max_gi, minmax, weights, bounds, step):
    num_variants, num_criteria = A.shape
    U = np.zeros((num_variants, num_criteria))

    for k in range(num_criteria):
        for a in range(num_variants):
            # Generate the continuous range for each criterion based on the bounds and step
            criterion_range = np.arange(bounds[k][0], bounds[k][1] + step, step)

            # Normalize the value for interpolation
            range_value = max_gi[k] - min_gi[k]
            if range_value == 0:
                value = 0.5  # If min == max, assume a middle value
            else:
                value = (A[a, k] - min_gi[k]) / range_value

            # Calculate partial utility
            if minmax[k]:  # Maximization
                U[a, k] = value * weights[k]
            else:  # Minimization
                U[a, k] = (1 - value) * weights[k]
    return U

def UTA_CONTINUOUS(A, minmax, weights=None, thresholds=None, bounds=None, step=0.1):
    num_criteria = A.shape[1]
    if weights is None:
        weights = [1 / num_criteria] * num_criteria

    if bounds is None:
        raise ValueError("Bounds must be defined for each criterion.")

    min_g, max_g = find_minmax_criteria(A)

    # Calculate partial utilities for continuous data
    U = calc_partial_utilities_continuous(A, min_g, max_g, minmax, weights, bounds, step)

    # Calculate total utilities
    total_utilities = calc_total_utilities(U)

    # Classify if thresholds are provided
    if thresholds is not None:
        categories = classify_categories(total_utilities, thresholds)
    else:
        categories = None

    return categories, total_utilities

# Wizualizacja wyników
def visualize(data, utilities, criterion1=0, criterion2=1, criterion3=2):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(
        data[:, criterion1],
        data[:, criterion2],
        data[:, criterion3],
        c=utilities,
        cmap='viridis',
        edgecolor='k',
        s=100
    )
    plt.colorbar(sc, label="Użyteczność")
    ax.set_xlabel(f"Kryterium {criterion1 + 1}")
    ax.set_ylabel(f"Kryterium {criterion2 + 1}")
    ax.set_zlabel(f"Kryterium {criterion3 + 1}")
    ax.set_title("Wizualizacja punktów w przestrzeni kryteriów")
    plt.show()


# Przykład testowania
if __name__ == "__main__":
    # Example matrix of alternatives (values for 3 criteria)
    A = np.array([
        [12, 8, 15],
        [7, 5, 12],
        [6, 7, 10],
        [5, 6, 8],
        [4, 5, 6],
        [3, 4, 4]
    ])

    # Define minmax for criteria: True for maximization, False for minimization
    minmax = [False, False, False]  # Minimizing all criteria

    # Weights for each criterion
    weights = [0.4, 0.3, 0.3]

    # Thresholds for category classification
    thresholds = [0.3, 0.5, 0.7]

    # Define bounds for each criterion (min_value, max_value)
    bounds = [(0, 15), (0, 10), (0, 20)]

    # Step size for interpolation
    step = 0.5

    # Classify alternatives using UTA for continuous data
    categories, total_utilities = UTA_CONTINUOUS(A, minmax, weights, thresholds, bounds, step)

    print("Total Utilities:")
    print(total_utilities)
    print("Categories:")
    print(categories)

    # Wizualizacja w 3D
    visualize(A, total_utilities)
