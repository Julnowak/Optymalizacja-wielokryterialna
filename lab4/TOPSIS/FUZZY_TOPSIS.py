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
    bounds=None
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
        return [(value[0] / ideal[2]), (value[1] / ideal[1]), (value[2] / ideal[0])]

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

    # Normalize alternatives
    normalized = [
        [normalize_fuzzy(alt[j], ideal[j]) for j in range(num_criteria)]
        for alt in alternatives
    ]

    # Weighted normalized fuzzy decision matrix
    weighted = [
        [[val[0] * weights[j][0], val[1] * weights[j][1], val[2] * weights[j][2]] for j, val in enumerate(alt)]
        for alt in normalized
    ]

    # Distance to fuzzy ideal and anti-ideal solutions
    def fuzzy_distance(val, ref):
        """Calculate fuzzy distance."""
        return np.sqrt(sum((val[k] - ref[k]) ** 2 for k in range(3)))

    distances_ideal = [sum(fuzzy_distance(val, ideal[j]) for j, val in enumerate(alt)) for alt in weighted]
    distances_anti_ideal = [sum(fuzzy_distance(val, anti_ideal[j]) for j, val in enumerate(alt)) for alt in weighted]

    # Calculate closeness coefficient
    closeness = [dist_anti / (dist_anti + dist_ideal) for dist_anti, dist_ideal in zip(distances_anti_ideal, distances_ideal)]

    # Generate points for the continuous variant if needed
    if variant == "continuous" and bounds is not None and num_samples > 0:
        samples = [np.linspace(b[0], b[1], num_samples) for b in bounds]
        samples_mesh = np.array(np.meshgrid(*samples)).T.reshape(-1, len(bounds)).tolist()

        # Calculate distances for continuous points
        continuous_scores = []
        for point in samples_mesh:
            d_plus = min([fuzzy_distance(point, r_plus) for r_plus in ideal])
            d_minus = min([fuzzy_distance(point, r_minus) for r_minus in anti_ideal])
            continuous_scores.append((point, d_minus - d_plus))

        continuous_scores.sort(key=lambda x: x[1], reverse=True)
        return continuous_scores, {
        "normalized": normalized,
        "weighted": weighted,
        "distances_ideal": distances_ideal,
        "distances_anti_ideal": distances_anti_ideal,
        "closeness": closeness,
    }

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
    ranking_order = np.argsort(closeness)[::-1]
    colors = plt.cm.viridis(np.linspace(0, 1, len(alternatives)))[ranking_order]

    # 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, (point, color) in enumerate(zip(middle_points, colors)):
        ax.scatter(
            point[0], point[1], point[2],
            color=color,
            label=f"Alternative {i + 1} (Rank: {ranking_order.tolist().index(i) + 1})"
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

    criteria_continuous = [False, False, False, False]
    weights_continuous = [(0.2, 0.5, 0.8),
                          (0.3, 0.6, 0.9),
                          (0.4, 0.7, 1.0),
                          (0.1, 0.4, 0.7)]

    ranking_continuous, details_continuous = fuzzy_topsis(alternatives_continuous, criteria_continuous, weights_continuous, variant="continuous", num_samples=5, bounds=[(0, 10), (0, 10), (0, 10), (0, 10)])

    print("Continuous Case Ranking:", ranking_continuous)
    print("Details (Continuous):", details_continuous)
    visualize_fuzzy_topsis(alternatives_continuous, details_continuous['closeness'], title="Discrete Alternatives")

    # Example for discrete case with N=3 and N=4
    alternatives_discrete = [
        [(1, 2, 3), (3, 4, 5), (2, 3, 4)],
        [(2, 3, 4), (1, 2, 3), (3, 4, 5)],
        [(3, 4, 5), (2, 3, 4), (1, 2, 3)],
    ]

    criteria_discrete = [False, False, False]
    weights_discrete = [(0.3, 0.6, 0.9),
                        (0.2, 0.5, 0.8),
                        (0.5, 0.8, 1.0)]

    ranking_discrete, details_discrete = fuzzy_topsis(alternatives_discrete, criteria_discrete, weights_discrete, variant="discrete")

    print("\nDiscrete Case Ranking:", ranking_discrete)
    print("Details (Discrete):", details_discrete)

    # Visualize discrete data
    visualize_fuzzy_topsis(alternatives_discrete, details_discrete['closeness'], title="Discrete Alternatives")
