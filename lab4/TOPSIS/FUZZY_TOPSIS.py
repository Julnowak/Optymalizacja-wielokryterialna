import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def fuzzy_topsis(
    alternatives,
    criteria,
    weights,
    variant="continuous",  # Określamy typ wariantu: "continuous" lub "discrete"
    num_samples=0,
    bounds=None,
    metric="euclidean"
):
    """
    Fuzzy TOPSIS Algorithm.
    :param alternatives: Array of alternatives, each represented as an array of triangular fuzzy numbers.
    :param criteria: Type of each criterion ('benefit' or 'cost').
    :param weights: Array of weights, each represented as a triangular fuzzy number.
    :param variant: Type of Fuzzy TOPSIS ('continuous' or 'discrete').
    :param num_samples: Number of samples for continuous variant (if applicable).
    :param bounds: List of tuples (min, max) for each criterion (if applicable).
    :return: Ranking of alternatives and intermediate matrices.
    """
    num_alternatives, num_criteria = len(alternatives), len(criteria)

    def normalize_fuzzy(value, ideal):
        """Normalize a fuzzy value based on ideal solution."""
        return [(value[0] / ideal[0]), (value[1] / ideal[1]), (value[2] / ideal[2])]

    # Calculate fuzzy ideal and anti-ideal solutions
    ideal = []
    anti_ideal = []
    for j in range(num_criteria):
        col = [alt[j] for alt in alternatives]
        if criteria[j] is True:
            ideal.append([max(c[0] for c in col), max(c[1] for c in col), max(c[2] for c in col)])
            anti_ideal.append([min(c[0] for c in col), min(c[1] for c in col), min(c[2] for c in col)])
        elif criteria[j] is False:
            ideal.append([min(c[0] for c in col), min(c[1] for c in col), min(c[2] for c in col)])
            anti_ideal.append([max(c[0] for c in col), max(c[1] for c in col), max(c[2] for c in col)])

    print(ideal)
    print(anti_ideal)

    # Normalize alternatives
    normalized = [
        [normalize_fuzzy(alt[j], ideal[j]) for j in range(num_criteria)]
        for alt in alternatives
    ]

    print(ideal)
    ideal = [
        [1.0 for _ in range(num_criteria)] for _ in ideal
    ]

    print(normalized)

    # Weighted normalized fuzzy decision matrix
    weighted = [
        [[val[k] * weights[j][k] for k in range(3)] for j, val in enumerate(alt)]
        for alt in normalized
    ]

    print(weighted)

    # Distance to fuzzy ideal and anti-ideal solutions
    def fuzzy_distance(val, ref, met="euclidean"):
        """Calculate fuzzy distance."""
        if met == 'euclidean':
            return np.sqrt(sum((val[k] - ref[k]) ** 2 for k in range(3)))
        elif met == 'chebyshev':
            return max((abs(val[k] - ref[k]) ** 2 for k in range(3)))
        else:
            raise ValueError("Unknown metric")

    distances_ideal = [sum(fuzzy_distance(val, ideal[j], metric) for j, val in enumerate(alt)) for alt in weighted]

    print(distances_ideal)

    distances_anti_ideal = [sum(fuzzy_distance(val, anti_ideal[j], metric) for j, val in enumerate(alt)) for alt in weighted]

    # Calculate closeness coefficient
    closeness = [dist_anti / (dist_anti + dist_ideal) for dist_anti, dist_ideal in zip(distances_anti_ideal, distances_ideal)]

    print(closeness)

    if variant == "continuous" and bounds is not None and num_samples > 0:
        samples = [np.linspace(b[0], b[1], num_samples) for b in bounds]
        print(samples)
        samples_mesh = np.array(np.meshgrid(*samples)).T.reshape(-1, len(bounds)).tolist()

        # Calculate distances for continuous points
        continuous_scores = []
        for point in samples_mesh:
            d_plus = min([fuzzy_distance(point, r_plus) for r_plus in ideal])
            d_minus = min([fuzzy_distance(point, r_minus) for r_minus in anti_ideal])
            continuous_scores.append(d_minus / (d_minus + d_plus))

        closeness = continuous_scores

    # Return ranking for the discrete variant
    ranking = np.argsort(closeness)[::-1]
    return ranking, {
        "normalized": normalized,
        "weighted": weighted,
        "distances_ideal": distances_ideal,
        "distances_anti_ideal": distances_anti_ideal,
        "closeness": closeness,
    }


def visualize_fuzzy_topsis(alternatives, closeness, title="Fuzzy TOPSIS Ranking"):
    """
    Visualize Fuzzy TOPSIS results in 3D.
    :param alternatives: Original alternatives, represented as arrays of triangular fuzzy numbers.
    :param closeness: Closeness coefficients of the alternatives.
    :param title: Title of the plot.
    """
    # Extract middle points (m values) for visualization
    middle_points = [[(l[1]) for l in alt] for alt in alternatives]
    middle_points = np.array(middle_points)

    # Sort by closeness coefficients (for coloring)
    ranking_order = list(closeness.keys())
    colors = plt.cm.viridis_r(np.linspace(0, 1, len(alternatives)))[ranking_order]

    # 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, (point, color) in enumerate(zip(middle_points, colors)):
        ax.scatter(
            point[0], point[1], point[2],
            color=color,
            label=f"Alternative {i + 1} (Rank: {ranking_order[i] + 1})"
        )

    ax.set_title(title)
    ax.set_xlabel("Criterion 1 (Middle Points)")
    ax.set_ylabel("Criterion 2 (Middle Points)")
    ax.set_zlabel("Criterion 3 (Middle Points)")
    ax.legend()
    plt.show()


# Example usage
if __name__ == "__main__":
    # Fuzzy triangular numbers: (l, m, u)
    alternatives_continuous = [
        [(1, 3, 5), (2, 4, 6), (3, 5, 7), (1, 2, 3)],
        [(2, 4, 6), (1, 3, 5), (2, 4, 6), (2, 3, 4)],
        [(3, 5, 7), (3, 5, 7), (1, 3, 5), (2, 4, 6)],
        [(1, 2, 3), (2, 3, 4), (3, 5, 7), (3, 5, 7)],
    ]
    alternatives_continuous = [
        [(1, 3, 5), (2, 4, 6), (3, 5, 7), (1, 2, 3)],
        [(22, 24, 26), (21, 23, 25), (22, 24, 26), (22, 23, 24)],
        [(43, 45, 47), (43, 45, 47), (41, 43, 45), (42, 44, 46)],
        [(71, 72, 73), (72, 73, 74), (73, 75, 77), (73, 75, 77)],
    ]

    criteria_continuous = [False, False, False, False]
    # criteria_continuous = [True] *4
    weights_continuous = [(1.0, 1.0, 1.0),
                          (1.0, 1.0, 1.0),
                          (1.0, 1.0, 1.0),
                          (1.0, 1.0, 1.0)]

    ranking_continuous, details_continuous = fuzzy_topsis(alternatives_continuous, criteria_continuous, weights_continuous, variant="continuous", num_samples=5, bounds=[(0, 10), (0, 10), (0, 10), (0, 10)])

    ranks = dict()
    for i in ranking_continuous:
        ranks[i] = details_continuous['closeness'][i]

    print("Continuous Case Ranking:", ranking_continuous)
    print("Details (Continuous):", details_continuous)
    visualize_fuzzy_topsis(alternatives_continuous, ranks, title="Discrete Alternatives")

    # Example for discrete case with N=3 and N=4
    alternatives_discrete = [
        [(1, 2, 3), (3, 4, 5), (2, 3, 4)],
        [(42, 43, 44), (41, 42, 43), (43, 44, 45)],
        [(83, 84, 85), (82, 83, 84), (81, 82, 83)],
    ]

    criteria_discrete = [True, True, True]
    criteria_discrete = [False, False, False]
    weights_discrete = [(1.0, 1.0, 1.0),
                        (1.0, 1.0, 1.0),
                        (1.0, 1.0, 1.0)]

    ranking_discrete, details_discrete = fuzzy_topsis(alternatives_discrete, criteria_discrete, weights_discrete, variant="discrete")

    print("\nDiscrete Case Ranking:", ranking_discrete)
    print("Details (Discrete):", details_discrete)

    ranks = dict()

    for i in ranking_discrete:
        ranks[i] = details_discrete['closeness'][i]

    # Visualize discrete data
    visualize_fuzzy_topsis(alternatives_discrete, ranks, title="Discrete Alternatives")
