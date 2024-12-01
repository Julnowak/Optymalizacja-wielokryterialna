from typing import List, Tuple
import numpy as np
from math import sqrt

def distance(a: List[float], b: List[float], metric: str = 'euclidean') -> float:
    if metric == 'euclidean':
        return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
    elif metric == 'chebyshev':
        return max(abs(x - y) for x, y in zip(a, b))
    else:
        raise ValueError("Unknown metric")

def sp_cs_discrete(
    alternatives: List[List[float]],
    status_quo: List[float],
    aspiration: List[float],
    metric: str = 'euclidean',
    num_t_samples: int = 100
) -> List[Tuple[List[float], float]]:
    """
    SP-CS algorithm for discrete alternatives.

    :param alternatives: List of alternatives in the decision space.
    :param status_quo: Status quo point.
    :param aspiration: Aspiration point.
    :param metric: Distance metric ('euclidean' or 'chebyshev').
    :param num_t_samples: Number of t samples along the skeleton curve.
    :return: List of alternatives with their S(u) values.
    """
    t_values = np.linspace(0, 1, num_t_samples)
    gamma_points = [(1 - t) * np.array(status_quo) + t * np.array(aspiration) for t in t_values]

    results = []
    for alt in alternatives:
        min_Su = float('inf')
        for idx, gamma_point in enumerate(gamma_points):
            d = distance(alt, gamma_point, metric)
            Su = t_values[idx] + d
            if Su < min_Su:
                min_Su = Su
        results.append((alt, min_Su))
    # Sort results by S(u)
    results.sort(key=lambda x: x[1])
    return results

def sp_cs_continuous(
    bounds: List[Tuple[float, float]],
    status_quo: List[float],
    aspiration: List[float],
    metric: str = 'euclidean',
    num_samples: int = 1000,
    num_t_samples: int = 100
) -> List[Tuple[List[float], float]]:
    """
    SP-CS algorithm for continuous alternatives.

    :param bounds: Bounds for each criterion as a list of tuples (min, max).
    :param status_quo: Status quo point.
    :param aspiration: Aspiration point.
    :param metric: Distance metric ('euclidean' or 'chebyshev').
    :param num_samples: Number of samples in the continuous space.
    :param num_t_samples: Number of t samples along the skeleton curve.
    :return: List of alternatives with their S(u) values.
    """
    # Generate random samples within bounds
    np.random.seed(0)
    samples = np.random.uniform(
        low=[b[0] for b in bounds],
        high=[b[1] for b in bounds],
        size=(num_samples, len(bounds))
    ).tolist()

    return sp_cs_discrete(samples, status_quo, aspiration, metric, num_t_samples)

# Example usage
if __name__ == "__main__":
    # DISCRETE VARIANT N=3
    status_quo_N3 = [0, 0, 0]
    aspiration_N3 = [1, 1, 1]
    alternatives_N3 = [
        [0.2, 0.4, 0.6],
        [0.5, 0.7, 0.8],
        [0.3, 0.5, 0.9]
    ]

    results_N3 = sp_cs_discrete(alternatives_N3, status_quo_N3, aspiration_N3, metric='euclidean')
    print("Alternatives in discrete variant N=3 (sorted by S(u)):")
    for alt, Su in results_N3:
        print(f"Alternative: {alt}, S(u): {Su:.4f}")

    # DISCRETE VARIANT N=4
    status_quo_N4 = [0, 0, 0, 0]
    aspiration_N4 = [1, 1, 1, 1]
    alternatives_N4 = [
        [0.2, 0.3, 0.4, 0.5],
        [0.5, 0.6, 0.7, 0.8],
        [0.8, 0.7, 0.6, 0.5]
    ]

    results_N4 = sp_cs_discrete(alternatives_N4, status_quo_N4, aspiration_N4, metric='euclidean')
    print("\nAlternatives in discrete variant N=4 (sorted by S(u)):")
    for alt, Su in results_N4:
        print(f"Alternative: {alt}, S(u): {Su:.4f}")

    # CONTINUOUS VARIANT U⊂R² and N=4
    status_quo_continuous = [0, 0]
    aspiration_continuous = [1, 1]
    bounds = [(0, 1), (0, 1)]  # U⊂R²

    results_continuous = sp_cs_continuous(
        bounds,
        status_quo_continuous,
        aspiration_continuous,
        metric='euclidean',
        num_samples=1000,
        num_t_samples=100
    )

    print("\nAlternatives in continuous variant (top 5 alternatives sorted by S(u)):")
    for alt, Su in results_continuous[:5]:
        print(f"Alternative: {np.round(alt, 4)}, S(u): {Su:.4f}")
