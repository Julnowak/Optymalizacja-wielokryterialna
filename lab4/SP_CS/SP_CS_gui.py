from typing import List, Tuple
import numpy as np
from math import sqrt
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd


def distance(a: List[float], b: List[float], metric: str = 'euclidean') -> float:
    if metric == 'euclidean':
        return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
    elif metric == 'chebyshev':
        return max(abs(x - y) for x, y in zip(a, b))
    else:
        raise ValueError("Unknown metric")


def normalize_alternative(
        alternative: List[float],
        status_quo: List[float],
        aspiration: List[float],
        minmax: List[bool],
        debug: bool = False
) -> List[float]:
    normalized = []
    for idx, (x, sq, asp, maximize) in enumerate(zip(alternative, status_quo, aspiration, minmax)):
        if maximize:
            if asp != sq:
                norm_val = (x - sq) / (asp - sq)
            else:
                norm_val = 0
        else:
            # Formuła dla minimalizacji
            if asp != sq:
                norm_val = (sq - x) / (sq - asp)
            else:
                norm_val = 0
        norm_val = max(0, min(norm_val, 1))
        if debug:
            print(
                f"  Criterion {idx + 1}: Original={x}, Normalized={norm_val:.4f}, {'Maximize' if maximize else 'Minimize'}")
        normalized.append(norm_val)
    if debug:
        print(f"  Normalized Alternative: {normalized}")
    return normalized


def determine_status_quo_aspiration(alternatives: List[List[float]], minmax: List[bool], buffer: float = 0.1) -> Tuple[
    List[float], List[float]]:
    num_criteria = len(minmax)
    status_quo = []
    aspiration = []
    for i in range(num_criteria):
        values = [alt[i] for alt in alternatives]
        if minmax[i]:  # Maksymalizacja
            sq = min(values)
            asp = max(values) * (1 + buffer)
        else:  # Minimalizacja
            sq = max(values)
            asp = min(values) * (1 - buffer)
        status_quo.append(sq)
        aspiration.append(asp)
    return status_quo, aspiration


def sp_cs_discrete(
        alternatives: List[List[float]],
        minmax: List[bool],
        metric: str = 'euclidean',
        num_t_samples: int = 100,
        debug: bool = False
) -> List[Tuple[int, float]]:
    """
    Dyskretny wariant metody SP-CS.
    Zwraca listę (index, S(u)) posortowaną według S(u), tak samo jak oryginalna funkcja sp_cs().
    """
    status_quo, aspiration = determine_status_quo_aspiration(alternatives, minmax)

    t_values = np.linspace(0, 1, num_t_samples)
    gamma_points = []
    for t in t_values:
        gamma_raw = [(1 - t) * sq + t * asp for sq, asp in zip(status_quo, aspiration)]
        gamma_norm = normalize_alternative(gamma_raw, status_quo, aspiration, minmax, debug=False)
        gamma_points.append(gamma_norm)

    results = []
    for alt_idx, alt in enumerate(alternatives):
        if debug:
            print(f"\nProcessing Alternative {alt_idx + 1}: {alt}")
        normalized_alt = normalize_alternative(alt, status_quo, aspiration, minmax, debug=debug)
        min_Su = float('inf')
        for idx, gamma_point in enumerate(gamma_points):
            d = distance(normalized_alt, gamma_point, metric)
            Su = t_values[idx] + d
            if Su < min_Su:
                min_Su = Su
        results.append((alt_idx, min_Su))
        if debug:
            print(f"  S(u): {min_Su:.4f}")

    results.sort(key=lambda x: x[1])
    return results


def sp_cs_continuous(
        bounds: List[Tuple[float, float]],
        minmax: List[bool],
        metric: str = 'euclidean',
        num_samples: int = 10,
        num_t_samples: int = 100,
        debug: bool = False
) -> Tuple[List[Tuple[int, float]], List[List[float]]]:
    """
    Ciągły wariant metody SP-CS, tym razem generujący siatkę punktów (jak RSM).
    """
    # Zamiast losowych punktów generujemy siatkę:
    # np.linspace(b[0], b[1], num_samples) dla każdego wymiaru
    axes = [np.linspace(b[0], b[1], num_samples) for b in bounds]
    # Tworzymy siatkę z punktów (meshgrid)
    mesh = np.meshgrid(*axes)
    # Przekształcamy meshgrid w listę punktów
    samples_array = np.vstack([m.ravel() for m in mesh]).T
    samples = samples_array.tolist()

    # Wyliczamy status_quo i aspiration
    status_quo, aspiration = determine_status_quo_aspiration(samples, minmax)

    t_values = np.linspace(0, 1, num_t_samples)
    gamma_points = []
    for t in t_values:
        gamma_raw = [(1 - t) * sq + t * asp for sq, asp in zip(status_quo, aspiration)]
        gamma_norm = normalize_alternative(gamma_raw, status_quo, aspiration, minmax, debug=False)
        gamma_points.append(gamma_norm)

    results = []
    for alt_idx, alt in enumerate(samples):
        normalized_alt = normalize_alternative(alt, status_quo, aspiration, minmax, debug=debug)
        min_Su = float('inf')
        for idx, gamma_point in enumerate(gamma_points):
            d = distance(normalized_alt, gamma_point, metric)
            Su = t_values[idx] + d
            if Su < min_Su:
                min_Su = Su
        results.append((alt_idx, min_Su))

    results.sort(key=lambda x: x[1])
    return results, samples


if __name__ == "__main__":
    from UTA_BIS.UTA_DIS import visualize
    import numpy as np

    # Dane testowe takie jak w przykładzie RSM
    # Dla przestrzeni 3D (dyskretne)
    A_3d = np.array([[2, 3, 4], [-1, 1, 2], [1, 3, 4], [1, 1, 2], [2, 2, 4], [0, 0, 0]])  # Punkty odniesienia
    B_3d = np.array([[3, 4, 5], [5, 1, 2], [1, 2, 3], [3, 3, 4]])  # Punkty decyzyjne (dyskretne)

    # Zakładamy minimalizację wszystkich kryteriów (jak w przykładzie RSM)
    minmax_3d = [False, False, False]

    # Test dyskretnego wariantu SP-CS na takich samych danych wejściowych jak RSM:
    # Tutaj, w przeciwieństwie do RSM, SP-CS nie używa punktów odniesienia w taki sam sposób.
    # Po prostu potraktujmy B_3d jako "alternatywy".
    alternatives_3d = B_3d.tolist()
    results_discrete_3d = sp_cs_discrete(alternatives_3d, minmax_3d, metric='euclidean')
    # Wynik: lista (index, S(u)), gdzie index odnosi się do indeksu alternatywy w B_3d

    print("SP-CS Discrete 3D Results (Sorted by S(u)):")
    for i, su in results_discrete_3d:
        print(f"Alternative {i+1}, S(u)={su:.4f}")

    # Wizualizacja wyników dyskretnych (3D)
    utilities_3d = [su for (i, su) in results_discrete_3d]
    visualize(B_3d, utilities_3d)

    # Test ciągłego wariantu SP-CS dla 3D:
    bounds_continuous_3d = [(0, 10), (5, 15), (1, 5)]
    results_cont_3d, samples_3d = sp_cs_continuous(bounds_continuous_3d, minmax_3d, metric='euclidean')
    # results_cont_3d: (index, S(u)), samples_3d: wygenerowane punkty

    print("\nSP-CS Continuous 3D Results (Sorted by S(u)):")
    for i, su in results_cont_3d[:10]:
        print(f"Sample {i+1}, S(u)={su:.4f}")

    # Wizualizacja wyników ciągłych (3D)
    data_3d_cont = np.array(samples_3d)
    utilities_3d_cont = [su for (i, su) in results_cont_3d]
    visualize(data_3d_cont, utilities_3d_cont)

    # Analogicznie możesz przetestować dane 4D:
    A_4d = np.array([
        [2, 3, 4, 5],
        [-1, 1, 2, 3],
        [1, 3, 4, 5],
        [1, 1, 2, 2],
        [2, 2, 4, 5],
        [0, 0, 0, 0],
    ])  # Punkty odniesienia (4D)
    B_4d = np.array([
        [3, 4, 5, 6],
        [5, 1, 2, 3],
        [1, 2, 3, 4],
        [3, 3, 4, 5],
    ])  # Punkty decyzyjne (4D)

    minmax_4d = [False, False, False, False]
    alternatives_4d = B_4d.tolist()

    # Dyskretny wariant SP-CS dla 4D
    results_discrete_4d = sp_cs_discrete(alternatives_4d, minmax_4d, metric='euclidean')
    print("\nSP-CS Discrete 4D Results (Sorted by S(u)):")
    for i, su in results_discrete_4d:
        print(f"Alternative {i+1}, S(u)={su:.4f}")

    # Wizualizacja 4D jest trudniejsza (funkcja visualize jest dla 3D),
    # ale można zredukować do pierwszych 3 wymiarów, albo pominąć.

    # Ciągły wariant SP-CS dla 4D
    bounds_continuous_4d = [
        (0, 10),
        (5, 15),
        (1, 5),
        (0, 10),
    ]
    results_cont_4d, samples_4d = sp_cs_continuous(bounds_continuous_4d, minmax_4d, metric='euclidean')
    print("\nSP-CS Continuous 4D Results (Sorted by S(u)):")
    for i, su in results_cont_4d:
        print(f"Sample {i+1}, S(u)={su:.4f}")

    # Możesz wizualizować tylko pierwsze 3 kryteria z 4D (obciąć do 3 wymiarów):
    data_4d_cont = np.array(samples_4d)
    utilities_4d_cont = [su for (i, su) in results_cont_4d]
    # Bierzemy pierwsze 3 wymiary do wizualizacji
    data_4d_cont_3d = data_4d_cont[:, :3]
    visualize(data_4d_cont_3d, utilities_4d_cont)
