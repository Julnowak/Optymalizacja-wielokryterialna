from typing import List, Tuple
import numpy as np
from math import sqrt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

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
            if asp != sq:
                norm_val = (asp - x) / (asp - sq)
            else:
                norm_val = 0
        norm_val = max(0, min(norm_val, 1))
        normalized.append(norm_val)
        if debug:
            print(f"  Criterion {idx + 1}: Original={x}, Normalized={norm_val:.4f}, {'Maximize' if maximize else 'Minimize'}")
    if debug:
        print(f"  Normalized Alternative: {normalized}")
    return normalized

def determine_status_quo_aspiration(alternatives: List[List[float]], minmax: List[bool], buffer: float = 0.1) -> Tuple[List[float], List[float]]:
    num_criteria = len(minmax)
    status_quo = []
    aspiration = []
    for i in range(num_criteria):
        values = [alt[i] for alt in alternatives]
        if minmax[i]:  # Maximize
            sq = min(values)
            asp = max(values) * (1 + buffer)
        else:  # Minimize
            sq = max(values)
            asp = min(values) * (1 - buffer)
        status_quo.append(sq)
        aspiration.append(asp)
    return status_quo, aspiration

def sp_cs_discrete(
    alternatives: List[List[float]],
    status_quo: List[float],
    aspiration: List[float],
    minmax: List[bool],
    metric: str = 'euclidean',
    num_t_samples: int = 100,
    debug: bool = False
) -> List[Tuple[List[float], float, float]]:
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
        results.append((alt, min_Su, min_t))
        if debug:
            print(f"  Selected t*: {min_t:.4f}, S(u): {min_Su:.4f}")
    results.sort(key=lambda x: x[1])
    return results

def sp_cs_continuous(
    bounds: List[Tuple[float, float]],
    status_quo: List[float],
    aspiration: List[float],
    minmax: List[bool],
    metric: str = 'euclidean',
    num_samples: int = 1000,
    num_t_samples: int = 100,
    debug: bool = False
) -> Tuple[List[Tuple[List[float], float, float]], List[List[float]]]:
    np.random.seed(0)
    samples = np.random.uniform(
        low=[b[0] for b in bounds],
        high=[b[1] for b in bounds],
        size=(num_samples, len(bounds))
    ).tolist()
    
    results = sp_cs_discrete(samples, status_quo, aspiration, minmax, metric, num_t_samples, debug=debug)
    return results, samples

def visualize(data, utilities, criterion1=0, criterion2=1, criterion3=2):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')  # 3D plot

    sc = ax.scatter(
        [d[criterion1] for d in data],
        [d[criterion2] for d in data],
        [d[criterion3] for d in data],
        c=utilities,
        cmap='viridis',
        edgecolor='k',
        s=100
    )

    plt.colorbar(sc, label="S(u)")
    ax.set_xlabel(f"Criterion {criterion1 + 1}")
    ax.set_ylabel(f"Criterion {criterion2 + 1}")
    ax.set_zlabel(f"Criterion {criterion3 + 1}")
    ax.set_title("Visualization of Data Points in the Space of Three Criteria")

    plt.show()

# Example usage
if __name__ == "__main__":
    # DISCRETE VARIANT N=3
    print("=== Case 1: Mix of Maximization and Minimization ===")
    minmax_N3_case1 = [True, False, True]  # Maximize 1st and 3rd criteria, minimize 2nd
    alternatives_N3 = [
        [0.2, 0.4, 0.6],
        [0.5, 0.7, 0.8],
        [0.3, 0.5, 0.9]
    ]

    # Dynamically determine status quo and aspiration
    status_quo_N3_case1, aspiration_N3_case1 = determine_status_quo_aspiration(alternatives_N3, minmax_N3_case1)

    print(f"Status Quo: {status_quo_N3_case1}")
    print(f"Aspiration: {aspiration_N3_case1}")

    results_N3_case1 = sp_cs_discrete(
        alternatives_N3,
        status_quo_N3_case1,
        aspiration_N3_case1,
        minmax_N3_case1,
        metric='euclidean',
        debug=False
    )
    print("\nAlternatives in discrete variant N=3 (sorted by S(u)):")
    for alt, Su, t_star in results_N3_case1:
        print(f"Alternative: {alt}, S(u): {Su:.4f}, t*: {t_star:.4f}")

    # Visualize the alternatives in 3D space
    data_N3_case1 = [result[0] for result in results_N3_case1]
    utilities_N3_case1 = [result[1] for result in results_N3_case1]
    visualize(data_N3_case1, utilities_N3_case1)

    # DISCRETE VARIANT N=4
    print("\n=== Case 2: Mix of Maximization and Minimization ===")
    minmax_N4 = [True, True, False, True]  # Maximize criteria 1,2,4; minimize 3
    alternatives_N4 = [
        [0.2, 0.3, 0.4, 0.5],
        [0.5, 0.6, 0.7, 0.8],
        [0.8, 0.7, 0.6, 0.5]
    ]

    # Dynamically determine status quo and aspiration for N=4
    status_quo_N4, aspiration_N4 = determine_status_quo_aspiration(alternatives_N4, minmax_N4)

    print(f"Status Quo: {status_quo_N4}")
    print(f"Aspiration: {aspiration_N4}")

    results_N4 = sp_cs_discrete(
        alternatives_N4,
        status_quo_N4,
        aspiration_N4,
        minmax_N4,
        metric='euclidean',
        debug=False
    )
    print("\nAlternatives in discrete variant N=4 (sorted by S(u)):")
    for alt, Su, t_star in results_N4:
        print(f"Alternative: {alt}, S(u): {Su:.4f}, t*: {t_star:.4f}")

    # Visualize the alternatives in 3D space (choosing first 3 criteria)
    data_N4 = [result[0] for result in results_N4]
    utilities_N4 = [result[1] for result in results_N4]
    visualize(data_N4, utilities_N4, criterion1=0, criterion2=1, criterion3=2)

    # CONTINUOUS VARIANT U⊂R²
    print("\n=== Case 3: All Criteria Maximized ===")
    status_quo_continuous = [0, 0]
    aspiration_continuous = [1, 1]
    bounds = [(0, 1), (0, 1)]  # U⊂R²
    minmax_continuous_case1 = [True, True]  # Both criteria maximized

    # Determine dynamic status quo and aspiration for continuous variant
    # Assuming the continuous alternatives are generated within the bounds
    # For demonstration, we use fixed aspiration and status quo

    results_continuous_case1, alternatives_continuous_case1 = sp_cs_continuous(
        bounds,
        status_quo_continuous,
        aspiration_continuous,
        minmax_continuous_case1,
        metric='euclidean',
        num_samples=1000,
        num_t_samples=100,
        debug=False
    )

    print("\nTop 5 alternatives in continuous variant (sorted by S(u)):")
    for alt, Su, t_star in results_continuous_case1[:5]:
        print(f"Alternative: {np.round(alt, 4)}, S(u): {Su:.4f}, t*: {t_star:.4f}")

    # Visualize the top 100 alternatives
    top_100 = results_continuous_case1[:100]
    data_continuous = [result[0] for result in top_100]
    utilities_continuous = [result[1] for result in top_100]
    # 2D scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(
        [d[0] for d in data_continuous],
        [d[1] for d in data_continuous],
        c=utilities_continuous,
        cmap='viridis',
        edgecolor='k',
        s=50
    )
    plt.colorbar(label="S(u)")
    plt.xlabel("Criterion 1")
    plt.ylabel("Criterion 2")
    plt.title("Visualization of Top 100 Alternatives in Continuous Variant")
    plt.grid(True)
    plt.show()

    # ==== New Run: All Criteria Minimized ====
    print("\n=== Case 4: All Criteria Minimized ===")
    minmax_N3_case2 = [False, False, False]  # All criteria minimized for N=3
    alternatives_N3_case2 = [
        [0.2, 0.4, 0.6],
        [0.5, 0.7, 0.8],
        [0.3, 0.5, 0.9]
    ]

    # Dynamically determine status quo and aspiration for Case 4
    status_quo_N3_case2, aspiration_N3_case2 = determine_status_quo_aspiration(alternatives_N3_case2, minmax_N3_case2)

    print(f"Status Quo: {status_quo_N3_case2}")
    print(f"Aspiration: {aspiration_N3_case2}")

    results_N3_case2 = sp_cs_discrete(
        alternatives_N3_case2,
        status_quo_N3_case2,
        aspiration_N3_case2,
        minmax_N3_case2,
        metric='euclidean',
        debug=True  # Enable debugging for this case
    )
    print("\nAlternatives in discrete variant N=3 (sorted by S(u)):")
    for alt, Su, t_star in results_N3_case2:
        print(f"Alternative: {alt}, S(u): {Su:.4f}, t*: {t_star:.4f}")

    # Visualize the alternatives in 3D space
    data_N3_case2 = [result[0] for result in results_N3_case2]
    utilities_N3_case2 = [result[1] for result in results_N3_case2]
    visualize(data_N3_case2, utilities_N3_case2)

    # For N=4
    print("\n=== Case 5: All Criteria Minimized ===")
    minmax_N4_case2 = [False, False, False, False]  # All criteria minimized for N=4
    alternatives_N4_case2 = [
        [0.2, 0.3, 0.4, 0.5],
        [0.5, 0.6, 0.7, 0.8],
        [0.8, 0.7, 0.6, 0.5]
    ]

    # Dynamically determine status quo and aspiration for N=4
    status_quo_N4_case2, aspiration_N4_case2 = determine_status_quo_aspiration(alternatives_N4_case2, minmax_N4_case2)

    print(f"Status Quo: {status_quo_N4_case2}")
    print(f"Aspiration: {aspiration_N4_case2}")

    results_N4_case2 = sp_cs_discrete(
        alternatives_N4_case2,
        status_quo_N4_case2,
        aspiration_N4_case2,
        minmax_N4_case2,
        metric='euclidean',
        debug=True  # Enable debugging for this case
    )
    print("\nAlternatives in discrete variant N=4 (sorted by S(u)):")
    for alt, Su, t_star in results_N4_case2:
        print(f"Alternative: {alt}, S(u): {Su:.4f}, t*: {t_star:.4f}")

    # Visualize the alternatives in 3D space (choosing first 3 criteria)
    data_N4_case2 = [result[0] for result in results_N4_case2]
    utilities_N4_case2 = [result[1] for result in results_N4_case2]
    visualize(data_N4_case2, utilities_N4_case2, criterion1=0, criterion2=1, criterion3=2)

    # CONTINUOUS VARIANT U⊂R²
    print("\n=== Case 6: All Criteria Minimized ===")
    minmax_continuous_case2 = [False, False]  # Both criteria minimized

    # Dynamically determine status quo and aspiration for continuous variant
    # Here, status quo and aspiration should reflect minimization
    # Alternatively, you can adjust the determine_status_quo_aspiration function to handle continuous variants

    results_continuous_case2, alternatives_continuous_case2 = sp_cs_continuous(
        bounds,
        status_quo_continuous,  # For minimization, status quo and aspiration should be set accordingly
        aspiration_continuous,
        minmax_continuous_case2,
        metric='euclidean',
        num_samples=1000,
        num_t_samples=100,
        debug=False
    )

    print("\nTop 5 alternatives in continuous variant (sorted by S(u)):")
    for alt, Su, t_star in results_continuous_case2[:5]:
        print(f"Alternative: {np.round(alt, 4)}, S(u): {Su:.4f}, t*: {t_star:.4f}")

    # Visualize the top 100 alternatives
    top_100_case2 = results_continuous_case2[:100]
    data_continuous_case2 = [result[0] for result in top_100_case2]
    utilities_continuous_case2 = [result[1] for result in top_100_case2]
    # 2D scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(
        [d[0] for d in data_continuous_case2],
        [d[1] for d in data_continuous_case2],
        c=utilities_continuous_case2,
        cmap='viridis',
        edgecolor='k',
        s=50
    )
    plt.colorbar(label="S(u)")
    plt.xlabel("Criterion 1")
    plt.ylabel("Criterion 2")
    plt.title("Visualization of Top 100 Alternatives in Continuous Variant")
    plt.grid(True)
    plt.show()
