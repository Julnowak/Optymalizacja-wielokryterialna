import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Funkcje metryk
def euclidean_distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def chebyshev_distance(a, b):
    return np.max(np.abs(np.array(a) - np.array(b)))

# Funkcja SP-CS dla wariantu dyskretnego
def sp_cs_discrete(alternatives, status_quos, aspirations, metric='euclidean', num_t_samples=100):
    """
    SP-CS algorithm for discrete alternatives.

    :param alternatives: List of alternatives in decision space.
    :param status_quos: List of status quo points.
    :param aspirations: List of aspiration points.
    :param metric: Distance metric ('euclidean' or 'chebyshev').
    :param num_t_samples: Number of t samples along the skeleton curves.
    :return: List of alternatives with their S(u) values, sorted from best to worst.
    """
    # Select distance function
    if metric == 'euclidean':
        distance_function = euclidean_distance
    elif metric == 'chebyshev':
        distance_function = chebyshev_distance
    else:
        raise ValueError("Unknown metric")
    
    # Generate t values
    t_values = np.linspace(0, 1, num_t_samples)
    
    # Generate all skeleton curves γ_{ij}(t)
    gamma_curves = []
    for a0 in status_quos:
        for a1 in aspirations:
            gamma_points = [(1 - t) * np.array(a0) + t * np.array(a1) for t in t_values]
            gamma_curves.append({'a0': a0, 'a1': a1, 'gamma_points': gamma_points})
    
    # Compute S(u) for each alternative
    results = []
    for alt_idx, alt in enumerate(alternatives):
        min_Su = float('inf')
        best_t = None
        best_gamma = None
        for gamma in gamma_curves:
            distances = [distance_function(alt, gamma_point) for gamma_point in gamma['gamma_points']]
            min_dist = min(distances)
            best_t_index = distances.index(min_dist)
            t_star = t_values[best_t_index]
            Su = t_star + min_dist
            if Su < min_Su:
                min_Su = Su
                best_t = t_star
                best_gamma = gamma
        results.append({'Alternative': f'A{alt_idx + 1}', 'S(u)': min_Su, 't*': best_t, 'Alternative Values': alt})
    
    # Sort alternatives by S(u)
    results.sort(key=lambda x: x['S(u)'])
    
    return results

# Funkcja SP-CS dla wariantu ciągłego
def sp_cs_continuous(bounds, status_quos, aspirations, metric='euclidean', num_t_samples=100, num_points=1000):
    """
    SP-CS algorithm for continuous alternatives.

    :param bounds: List of tuples defining the bounds for each criterion.
    :param status_quos: List of status quo points.
    :param aspirations: List of aspiration points.
    :param metric: Distance metric ('euclidean' or 'chebyshev').
    :param num_t_samples: Number of t samples along the skeleton curves.
    :param num_points: Number of points to sample in the continuous space.
    :return: List of alternatives with their S(u) values, sorted from best to worst.
    """
    # Generate random alternatives within the bounds
    np.random.seed(0)  # For reproducibility
    alternatives = np.random.uniform(
        low=[b[0] for b in bounds],
        high=[b[1] for b in bounds],
        size=(num_points, len(bounds))
    ).tolist()
    
    # Use the same function as discrete
    results = sp_cs_discrete(
        alternatives=alternatives,
        status_quos=status_quos,
        aspirations=aspirations,
        metric=metric,
        num_t_samples=num_t_samples
    )
    
    return results, alternatives

# Funkcja normalizacji kryteriów do przedziału [0, 1]
def normalize_criteria(alternatives):
    """
    Normalize criteria values to [0, 1].

    :param alternatives: List of alternatives.
    :return: Normalized alternatives.
    """
    alternatives = np.array(alternatives)
    min_values = alternatives.min(axis=0)
    max_values = alternatives.max(axis=0)
    normalized_alternatives = []
    for alt in alternatives:
        normalized_alt = []
        for i, value in enumerate(alt):
            if max_values[i] == min_values[i]:
                norm_value = 0.0  # Avoid division by zero
            else:
                norm_value = (value - min_values[i]) / (max_values[i] - min_values[i])
            normalized_alt.append(norm_value)
        normalized_alternatives.append(normalized_alt)
    return normalized_alternatives

# Funkcja do wyświetlania rankingu
def print_ranking(results, title="Ranking of alternatives:"):
    print(f"\n{title}")
    df = pd.DataFrame(results)
    df.index += 1  # Start index from 1
    print(df[['Alternative', 'S(u)', 't*', 'Alternative Values']])

# Wizualizacja dla 2D
def visualize_2d(alternatives, gamma_curves, status_quos, aspirations, title):
    plt.figure(figsize=(8, 6))
    
    # Plot skeleton curves
    for gamma in gamma_curves:
        gamma_points = np.array(gamma['gamma_points'])
        plt.plot(gamma_points[:, 0], gamma_points[:, 1], linestyle='--', color='gray')
    
    # Plot alternatives
    alternatives_array = np.array(alternatives)
    plt.scatter(alternatives_array[:, 0], alternatives_array[:, 1], color='red', label='Alternatives')
    
    # Plot status quo and aspiration points
    for sq in status_quos:
        plt.scatter(sq[0], sq[1], color='green', marker='o', label='Status Quo')
    for ap in aspirations:
        plt.scatter(ap[0], ap[1], color='blue', marker='x', label='Aspiration')
    
    plt.xlabel('Criterion 1')
    plt.ylabel('Criterion 2')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Główne wykonanie
if __name__ == "__main__":
    # -------------------------------
    # WARIANT CIĄGŁY (U ⊂ R², N = 4)
    # -------------------------------
    
    # Definiujemy przedziały dla każdego kryterium (tutaj dwa kryteria dla R²)
    bounds_continuous = [(0, 1), (0, 1)]  # U ⊂ R²
    
    # Punkty status quo i aspiracji
    status_quos_continuous = [[0, 0]]
    aspirations_continuous = [[1, 1]]
    
    # Uruchomienie algorytmu dla wariantu ciągłego z metryką Euklidesową
    results_continuous_euclidean, alternatives_continuous = sp_cs_continuous(
        bounds=bounds_continuous,
        status_quos=status_quos_continuous,
        aspirations=aspirations_continuous,
        metric='euclidean',
        num_t_samples=100,
        num_points=1000
    )
    
    # Wyświetlenie najlepszych 5 alternatyw
    print_ranking(results_continuous_euclidean[:5], "Continuous Variant - Euclidean Metric")
    
    # Wizualizacja
    visualize_2d(
        alternatives_continuous,
        gamma_curves=[{'gamma_points': [(1 - t) * np.array(status_quos_continuous[0]) + t * np.array(aspirations_continuous[0]) for t in np.linspace(0, 1, 100)]}],
        status_quos=status_quos_continuous,
        aspirations=aspirations_continuous,
        title='Continuous Variant - Euclidean Metric'
    )
    
    # -------------------------------
    # WARIANT DYSKRETNY (N = 3)
    # -------------------------------
    
    # Alternatywy
    alternatives_discrete_N3 = [
        [0.2, 0.4, 0.6],
        [0.5, 0.7, 0.8],
        [0.3, 0.5, 0.9]
    ]
    
    # Punkty status quo i aspiracji
    status_quos_N3 = [[0, 0, 0]]
    aspirations_N3 = [[1, 1, 1]]
    
    # Uruchomienie algorytmu z metryką Euklidesową
    results_discrete_N3_euclidean = sp_cs_discrete(
        alternatives=alternatives_discrete_N3,
        status_quos=status_quos_N3,
        aspirations=aspirations_N3,
        metric='euclidean',
        num_t_samples=100
    )
    
    # Uruchomienie algorytmu z metryką Czebyszewa
    results_discrete_N3_chebyshev = sp_cs_discrete(
        alternatives=alternatives_discrete_N3,
        status_quos=status_quos_N3,
        aspirations=aspirations_N3,
        metric='chebyshev',
        num_t_samples=100
    )
    
    # Wyświetlenie wyników
    print_ranking(results_discrete_N3_euclidean, "Discrete Variant N=3 - Euclidean Metric")
    print_ranking(results_discrete_N3_chebyshev, "Discrete Variant N=3 - Chebyshev Metric")
    
    # -------------------------------
    # ANALIZA WRAŻLIWOŚCI
    # -------------------------------
    
    # Zmiana punktów odniesienia
    status_quos_new = [[0.1, 0.1, 0.1]]
    aspirations_new = [[0.9, 0.9, 0.9]]
    
    results_discrete_N3_euclidean_new_ref = sp_cs_discrete(
        alternatives=alternatives_discrete_N3,
        status_quos=status_quos_new,
        aspirations=aspirations_new,
        metric='euclidean',
        num_t_samples=100
    )
    
    print_ranking(results_discrete_N3_euclidean_new_ref, "Discrete Variant N=3 - Euclidean Metric with New Reference Points")
    
    # Zmiana rozdzielczości Δt
    results_discrete_N3_euclidean_fine_t = sp_cs_discrete(
        alternatives=alternatives_discrete_N3,
        status_quos=status_quos_N3,
        aspirations=aspirations_N3,
        metric='euclidean',
        num_t_samples=1000  # Finer t resolution
    )
    
    print_ranking(results_discrete_N3_euclidean_fine_t, "Discrete Variant N=3 - Euclidean Metric with Fine t Resolution")
    
    # -------------------------------
    # WARIANT DYSKRETNY (N = 4)
    # -------------------------------
    
    # Alternatywy
    alternatives_discrete_N4 = [
        [0.2, 0.3, 0.4, 0.5],
        [0.5, 0.6, 0.7, 0.8],
        [0.8, 0.7, 0.6, 0.5]
    ]
    
    # Punkty status quo i aspiracji
    status_quos_N4 = [[0, 0, 0, 0]]
    aspirations_N4 = [[1, 1, 1, 1]]
    
    # Uruchomienie algorytmu z metryką Euklidesową
    results_discrete_N4_euclidean = sp_cs_discrete(
        alternatives=alternatives_discrete_N4,
        status_quos=status_quos_N4,
        aspirations=aspirations_N4,
        metric='euclidean',
        num_t_samples=100
    )
    
    print_ranking(results_discrete_N4_euclidean, "Discrete Variant N=4 - Euclidean Metric")
    
    # -------------------------------
    # WIZUALIZACJA DLA N=3
    # -------------------------------
    
    # Projekcje par kryteriów
    def visualize_3d_projections(alternatives, gamma_curves, status_quos, aspirations, title):
        criteria_pairs = [(0, 1), (0, 2), (1, 2)]
        for idx, (i, j) in enumerate(criteria_pairs):
            plt.figure(figsize=(6, 5))
            # Plot skeleton curves
            for gamma in gamma_curves:
                gamma_points = np.array(gamma['gamma_points'])
                plt.plot(gamma_points[:, i], gamma_points[:, j], linestyle='--', color='gray')
            # Plot alternatives
            alternatives_array = np.array(alternatives)
            plt.scatter(alternatives_array[:, i], alternatives_array[:, j], color='red', label='Alternatives')
            # Plot status quo and aspiration points
            for sq in status_quos:
                plt.scatter(sq[i], sq[j], color='green', marker='o', label='Status Quo')
            for ap in aspirations:
                plt.scatter(ap[i], ap[j], color='blue', marker='x', label='Aspiration')
            plt.xlabel(f'Criterion {i + 1}')
            plt.ylabel(f'Criterion {j + 1}')
            plt.title(f'{title} - Projection {i + 1} vs {j + 1}')
            plt.legend()
            plt.grid(True)
            plt.show()
    
    # Wizualizacja projekcji dla N=3
    visualize_3d_projections(
        alternatives_discrete_N3,
        gamma_curves=[{'gamma_points': [(1 - t) * np.array(status_quos_N3[0]) + t * np.array(aspirations_N3[0]) for t in np.linspace(0, 1, 100)]}],
        status_quos=status_quos_N3,
        aspirations=aspirations_N3,
        title='Discrete Variant N=3 - Euclidean Metric'
    )
