import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Fuzzy TOPSIS core functions
def fuzzy_topsis(alternatives, criteria, weights):
    """
    Fuzzy TOPSIS implementation for 2D fuzzy numbers.
    :param alternatives: List of alternatives with criteria values (2D tuples per criterion).
    :param criteria: List of criteria types ('benefit' or 'cost').
    :param weights: List of weights as 2D tuples.
    :return: Ranking and details (scores).
    """
    # Transform alternatives and weights to numpy arrays
    alternatives = np.array(alternatives)
    weights = np.array(weights)

    # Step 1: Normalize fuzzy decision matrix
    norm_matrix = []
    for j, crit in enumerate(criteria):
        values = alternatives[:, j]
        if crit == 'benefit':
            max_val = np.max(values, axis=0)[1]  # max upper bound
            norm = [(l / max_val, u / max_val) for l, u in values]
        elif crit == 'cost':
            min_val = np.min(values, axis=0)[0]  # min lower bound
            norm = [(min_val / u, min_val / l) for l, u in values]
        norm_matrix.append(norm)
    norm_matrix = np.array(norm_matrix).transpose(1, 0, 2)

    # Step 2: Weighted normalized matrix
    weighted_matrix = np.zeros_like(norm_matrix)
    for j in range(len(criteria)):
        for i in range(len(alternatives)):
            l, u = norm_matrix[i, j]
            wl, wu = weights[j]
            weighted_matrix[i, j] = (l * wl, u * wu)

    # Step 3: Determine fuzzy ideal solutions
    positive_ideal = np.max(weighted_matrix, axis=0)
    negative_ideal = np.min(weighted_matrix, axis=0)

    # Step 4: Calculate distances to ideal solutions
    def fuzzy_distance(a, b):
        return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    distances_positive = [
        sum(fuzzy_distance(weighted_matrix[i, j], positive_ideal[j]) for j in range(len(criteria)))
        for i in range(len(alternatives))
    ]
    distances_negative = [
        sum(fuzzy_distance(weighted_matrix[i, j], negative_ideal[j]) for j in range(len(criteria)))
        for i in range(len(alternatives))
    ]

    # Step 5: Calculate closeness coefficient
    scores = [
        distances_negative[i] / (distances_negative[i] + distances_positive[i])
        for i in range(len(alternatives))
    ]

    # Ranking
    ranking = np.argsort(scores)[::-1]  # Descending order
    return ranking, scores


# Plot ranking results
def plot_ranking(alternatives, ranking, title="Fuzzy TOPSIS Ranking"):
    """
    Visualizes the ranking results of fuzzy TOPSIS as points.
    """
    plt.figure(figsize=(10, 6))
    for i, rank in enumerate(ranking):
        x = i + 1
        # Plot the lower and upper bounds for each alternative
        l, u = alternatives[rank][0]  # Using the first criterion value (can change for other criteria)
        plt.plot([x, x], [l, u], color="blue", marker='o', markersize=5, label="Alternative {}".format(rank + 1) if i == 0 else "")

    plt.title(title)
    plt.xlabel("Alternatives (Ranked)")
    plt.ylabel("Fuzzy Values (Lower and Upper Bounds)")
    plt.xticks(range(1, len(alternatives) + 1), [f"Alt {i + 1}" for i in range(len(alternatives))])
    plt.legend()
    plt.grid(True)
    plt.show()


# Example for continuous case with U⊂R^4 and N=4
alternatives_continuous = [
    [(1, 5), (2, 6), (3, 7), (1, 3)],
    [(2, 6), (1, 5), (2, 6), (2, 4)],
    [(3, 7), (3, 7), (1, 5), (2, 6)],
    [(1, 3), (2, 4), (3, 7), (3, 7)],
]
criteria_continuous = ['benefit', 'cost', 'benefit', 'cost']
weights_continuous = [(0.2, 0.8), (0.3, 0.9), (0.4, 1.0), (0.1, 0.7)]

ranking_continuous, scores_continuous = fuzzy_topsis(
    alternatives_continuous, criteria_continuous, weights_continuous
)
print("Continuous Case Ranking:", ranking_continuous)
print("Scores (Continuous):", scores_continuous)

# Generate plot for continuous case
plot_ranking(alternatives_continuous, ranking_continuous, title="Fuzzy TOPSIS Continuous Case")
