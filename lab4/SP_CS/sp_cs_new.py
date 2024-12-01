import numpy as np
import matplotlib.pyplot as plt

# Funkcje metryk
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def chebyshev_distance(a, b):
    return np.max(np.abs(a - b))

# Funkcja SP-CS dla wariantu dyskretnego
def sp_cs_discrete(alternatives, status_quo, aspirations, metric='euclidean', num_t_samples=100):
    """
    SP-CS algorithm for discrete alternatives.

    :param alternatives: Lista alternatyw w przestrzeni decyzyjnej.
    :param status_quo: Punkt status quo.
    :param aspirations: Punkt aspiracji.
    :param metric: Metryka odległości ('euclidean' lub 'chebyshev').
    :param num_t_samples: Liczba próbek parametru t na krzywej γ.
    :return: Lista alternatyw z ich wartościami S(u), posortowana od najlepszej do najgorszej.
    """
    # Wybór funkcji metryki
    if metric == 'euclidean':
        distance_function = euclidean_distance
    elif metric == 'chebyshev':
        distance_function = chebyshev_distance
    else:
        raise ValueError("Nieznana metryka")

    # Generowanie wartości t
    t_values = np.linspace(0, 1, num_t_samples)

    # Generowanie punktów na krzywej γ
    status_quo = np.array(status_quo)
    aspirations = np.array(aspirations)
    gamma_points = [(1 - t) * status_quo + t * aspirations for t in t_values]

    # Obliczanie wartości S(u) dla każdej alternatywy
    scores = []
    for alt in alternatives:
        alt = np.array(alt)
        min_score = float('inf')
        best_t = 0
        for t, gamma_point in zip(t_values, gamma_points):
            dist = distance_function(alt, gamma_point)
            score = t + dist
            if score < min_score:
                min_score = score
                best_t = t
        scores.append({'alternative': alt, 'S_u': min_score, 'best_t': best_t})

    # Sortowanie alternatyw według S(u)
    scores.sort(key=lambda x: x['S_u'])

    # Zwracanie również t_values i gamma_points do wykorzystania w wizualizacji
    return scores, t_values, gamma_points

# Dane wejściowe
alternatives = [
    [0.2, 0.3, 0.4, 0.5],
    [0.5, 0.6, 0.7, 0.8],
    [0.8, 0.7, 0.6, 0.5]
]
status_quo = [0, 0, 0, 0]
aspirations = [1, 1, 1, 1]

# Uruchomienie algorytmu z metryką Euklidesową
results_euclidean, t_values, gamma_points = sp_cs_discrete(alternatives, status_quo, aspirations, metric='euclidean')

# Wyświetlenie wyników
print("Ranking alternatyw z metryką Euklidesową:")
for idx, result in enumerate(results_euclidean):
    alt = result['alternative']
    S_u = result['S_u']
    print(f"Alternatywa {idx + 1}: {alt}, S(u) = {S_u:.4f}")

# Uruchomienie algorytmu z metryką Czebyszewa
results_chebyshev, _, _ = sp_cs_discrete(alternatives, status_quo, aspirations, metric='chebyshev')

# Wyświetlenie wyników
print("\nRanking alternatyw z metryką Czebyszewa:")
for idx, result in enumerate(results_chebyshev):
    alt = result['alternative']
    S_u = result['S_u']
    print(f"Alternatywa {idx + 1}: {alt}, S(u) = {S_u:.4f}")

# Wizualizacja krzywej γ i alternatyw

# Wybieramy dwa kryteria do wizualizacji
criterion_indices = [0, 1]  # Indeksy kryteriów do wykresu

# Tworzenie wykresu
plt.figure(figsize=(8, 6))

# Krzywa γ
gamma_points_array = np.array(gamma_points)
plt.plot(gamma_points_array[:, criterion_indices[0]], gamma_points_array[:, criterion_indices[1]], label='Krzywa γ')

# Alternatywy
alternatives_array = np.array(alternatives)
plt.scatter(alternatives_array[:, criterion_indices[0]], alternatives_array[:, criterion_indices[1]], color='red', label='Alternatywy')

# Punkty status quo i aspiracji
plt.scatter(status_quo[criterion_indices[0]], status_quo[criterion_indices[1]], color='green', marker='o', label='Status Quo')
plt.scatter(aspirations[criterion_indices[0]], aspirations[criterion_indices[1]], color='blue', marker='x', label='Aspiracje')

plt.xlabel(f'Kryterium {criterion_indices[0] + 1}')
plt.ylabel(f'Kryterium {criterion_indices[1] + 1}')
plt.title('Rzutowanie alternatyw na krzywą γ (Kryteria 1 i 2)')
plt.legend()
plt.grid(True)
plt.show()

# Analiza wrażliwości - zmiana metryki i punktów odniesienia

# Nowe punkty status quo i aspiracji
status_quo_new = [0.1, 0.1, 0.1, 0.1]
aspirations_new = [0.9, 0.9, 0.9, 0.9]

# Uruchomienie algorytmu z nowymi punktami odniesienia i metryką Euklidesową
results_euclidean_new, t_values_new, gamma_points_new = sp_cs_discrete(alternatives, status_quo_new, aspirations_new, metric='euclidean')

# Wyświetlenie wyników
print("\nRanking alternatyw z nowymi punktami odniesienia (metryka Euklidesowa):")
for idx, result in enumerate(results_euclidean_new):
    alt = result['alternative']
    S_u = result['S_u']
    print(f"Alternatywa {idx + 1}: {alt}, S(u) = {S_u:.4f}")

# Uruchomienie algorytmu z nowymi punktami odniesienia i metryką Czebyszewa
results_chebyshev_new, _, _ = sp_cs_discrete(alternatives, status_quo_new, aspirations_new, metric='chebyshev')

# Wyświetlenie wyników
print("\nRanking alternatyw z nowymi punktami odniesienia (metryka Czebyszewa):")
for idx, result in enumerate(results_chebyshev_new):
    alt = result['alternative']
    S_u = result['S_u']
    print(f"Alternatywa {idx + 1}: {alt}, S(u) = {S_u:.4f}")

# Wizualizacja z nowymi punktami odniesienia

# Tworzenie wykresu
plt.figure(figsize=(8, 6))

# Krzywa γ z nowymi punktami odniesienia
gamma_points_new_array = np.array(gamma_points_new)
plt.plot(gamma_points_new_array[:, criterion_indices[0]], gamma_points_new_array[:, criterion_indices[1]], label='Krzywa γ (nowa)')

# Alternatywy
plt.scatter(alternatives_array[:, criterion_indices[0]], alternatives_array[:, criterion_indices[1]], color='red', label='Alternatywy')

# Nowe punkty status quo i aspiracji
plt.scatter(status_quo_new[criterion_indices[0]], status_quo_new[criterion_indices[1]], color='green', marker='o', label='Status Quo (nowy)')
plt.scatter(aspirations_new[criterion_indices[0]], aspirations_new[criterion_indices[1]], color='blue', marker='x', label='Aspiracje (nowe)')

plt.xlabel(f'Kryterium {criterion_indices[0] + 1}')
plt.ylabel(f'Kryterium {criterion_indices[1] + 1}')
plt.title('Rzutowanie alternatyw na krzywą γ (nowe punkty odniesienia)')
plt.legend()
plt.grid(True)
plt.show()
