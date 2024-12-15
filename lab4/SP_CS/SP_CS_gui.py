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
            print(f"  Criterion {idx+1}: Original={x}, Normalized={norm_val:.4f}, {'Maximize' if maximize else 'Minimize'}")
        normalized.append(norm_val)
    if debug:
        print(f"  Normalized Alternative: {normalized}")
    return normalized

def determine_status_quo_aspiration(alternatives: List[List[float]], minmax: List[bool], buffer: float = 0.1) -> Tuple[List[float], List[float]]:
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

def sp_cs(
    alternatives: List[List[float]],
    minmax: List[bool],
    metric: str = 'euclidean',
    num_t_samples: int = 100,
    debug: bool = False
) -> List[Tuple[int, float]]:
    """
    Główna funkcja metody SP-CS.
    Oblicza ranking, wyświetla go w formie tabeli (pandas) w terminalu,
    oraz wywołuje visualize do wizualizacji danych (jeśli są co najmniej 3 kryteria).
    Zwraca listę (index, S(u)).
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
        min_t = None
        for idx, gamma_point in enumerate(gamma_points):
            d = distance(normalized_alt, gamma_point, metric)
            Su = t_values[idx] + d
            if Su < min_Su:
                min_Su = Su
                min_t = t_values[idx]
        results.append((alt_idx, min_Su))
        if debug:
            print(f"  Selected t*: {min_t:.4f}, S(u): {min_Su:.4f}")

    # Sortowanie według S(u)
    results.sort(key=lambda x: x[1])

    # Tworzenie DataFrame i wyświetlenie tabeli w terminalu
    df = pd.DataFrame(results, columns=["Alternative Index", "S(u)"])
    # Numerujemy alternatywy od 1
    df["Alternative Index"] = df["Alternative Index"] + 1
    # Formatowanie S(u)
    df["S(u)"] = df["S(u)"].apply(lambda x: f"{x:.4f}")
    # Wyświetlenie tabeli w terminalu
    print("\nRanking metodą SP-CS:")
    # print(df.to_string(index=False))

    # Wizualizacja 3D jeśli co najmniej 3 kryteria
    # if len(alternatives[0]) >= 3:
    #     # Mapa index->S(u) w kolejności oryginalnych alternatyw
    #     su_map = {r[0]: float(r[1]) for r in results}
    #     utilities = [su_map[i] for i in range(len(alternatives))]
    #     visualize(alternatives, utilities, criterion1=0, criterion2=1, criterion3=2)

    return results

# Przykładowe użycie:
if __name__ == "__main__":
    minmax_example = [True, False, True]
    alternatives_example = [
        [0.2, 0.4, 0.6],
        [0.5, 0.7, 0.8],
        [0.3, 0.5, 0.9],
        [0.4, 0.6, 0.7]
    ]
    ranking = sp_cs(alternatives_example, minmax_example, metric='euclidean', debug=False)

    print(ranking)

    sorted_ranking = sorted(ranking,)