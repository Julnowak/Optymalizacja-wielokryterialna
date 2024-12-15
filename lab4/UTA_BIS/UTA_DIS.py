import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def find_minmax_criteria(A):
    """Find minimum and maximum values for each criterion."""
    min_gi = np.min(A, axis=0)
    max_gi = np.max(A, axis=0)
    return min_gi, max_gi

import numpy as np
from typing import List, Tuple, Union


def generate_samples(bounds: List[Tuple[float, float]], num_samples: int) -> List[List[float]]:
    """
    Generate a grid of samples in the given bounds using num_samples for each criterion.
    """
    samples = [np.linspace(b[0], b[1], num_samples) for b in bounds]
    return np.array(np.meshgrid(*samples)).T.reshape(-1, len(bounds))


def calc_partial_utilities(A, min_gi, max_gi, minmax, weights, continuous=False, bounds=None, num_samples=10):
    """Calculate partial utilities for both discrete and continuous alternatives."""
    num_variants, num_criteria = A.shape
    U = np.zeros((num_variants, num_criteria))

    for k in range(num_criteria):
        for a in range(num_variants):
            range_value = max_gi[k] - min_gi[k]
            if range_value == 0:
                value = 0.5  # If min == max, assume a middle value
            else:
                value = (A[a, k] - min_gi[k]) / range_value

            if continuous:
                if bounds is None:
                    raise ValueError("Bounds must be provided for continuous alternatives.")
                criterion_range = np.linspace(bounds[k][0], bounds[k][1], num_samples)
                interpolated_value = np.interp(A[a, k], criterion_range, np.linspace(0, 1, num_samples))
                value = interpolated_value

            if minmax[k]:  # Maximization
                U[a, k] = value * weights[k]
            else:  # Minimization
                U[a, k] = (1 - value) * weights[k]

    return U


def calc_total_utilities(U):
    """Calculate total utilities by summing partial utilities."""
    return np.sum(U, axis=1)


def classify_categories(total_utilities, thresholds):
    """Classify utilities into categories based on thresholds."""
    categories = []
    for utility in total_utilities:
        for i, threshold in enumerate(thresholds):
            if utility <= threshold:
                categories.append(i + 1)
                break
        else:
            categories.append(len(thresholds) + 1)
    return categories


def UTA_DIS(A, minmax, weights=None, thresholds=None, continuous=False, bounds=None, num_samples=10):
    """
    UTA-DIS algorithm for both discrete and continuous alternatives.
    :param A: Matrix of alternatives.
    :param minmax: List of boolean values for each criterion (True=maximize, False=minimize).
    :param weights: Weights for each criterion (default=None, equal weights).
    :param thresholds: Thresholds for category classification.
    :param continuous: Boolean, whether the data is continuous.
    :param bounds: Bounds for each criterion (used in continuous mode).
    :param num_samples: Number of samples for interpolation in continuous mode.
    :return: Categories and total utilities.
    """




    # Calculate partial utilities
    if continuous:
        A = generate_samples(bounds, num_samples)

    num_criteria = A.shape[1]
    if weights is None:
        weights = [1 / num_criteria] * num_criteria
    min_g, max_g = find_minmax_criteria(A)
    U = calc_partial_utilities(A, min_g, max_g, minmax, weights, continuous, bounds, num_samples)

    # Calculate total utilities
    total_utilities = calc_total_utilities(U)

    # Classify into categories if thresholds are provided
    if thresholds is not None:
        categories = classify_categories(total_utilities, thresholds)
    else:
        categories = None

    return categories, total_utilities, A


def visualize(alternatives, utilities, title="UTA-DIS Visualization"):
    """Visualize alternatives and utilities in a 3D space."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(
        alternatives[:, 0], alternatives[:, 1], alternatives[:, 2],
        c=utilities, cmap='viridis', s=100, edgecolor='k'
    )
    plt.colorbar(sc, label="Total Utility")
    ax.set_xlabel("Criterion 1")
    ax.set_ylabel("Criterion 2")
    ax.set_zlabel("Criterion 3")
    ax.set_title(title)
    plt.show()


# Przykład testowania
if __name__ == "__main__":
    # Example matrix of alternatives for discrete case
    A_discrete = np.array([
        [12, 8, 15],
        [7, 5, 12],
        [6, 7, 10],
        [5, 6, 8],
        [4, 5, 6],
        [3, 4, 4]
    ])

    # Example matrix of alternatives for continuous case
    A_continuous = np.array([
        [1, 3, 5],
        [22, 24, 26],
        [43, 45, 47],
        [71, 72, 73]
    ])

    # Define minmax for criteria: True for maximization, False for minimization
    minmax = [True, True, True]
    minmax = [False]*3

    # Weights for each criterion
    weights = [0.5, 0.3, 0.2]

    # Thresholds for category classification
    thresholds = [0.3, 0.6, 0.8]

    # Define bounds for each criterion in continuous case
    bounds = [(0, 10), (20, 50), (40, 80)]

    # Run UTA-DIS for discrete alternatives
    categories_discrete, total_utilities_discrete, _ = UTA_DIS(A_discrete, minmax, weights, thresholds, continuous=False)

    # Run UTA-DIS for continuous alternatives
    categories_continuous, total_utilities_continuous, alts = UTA_DIS(
        A_continuous, minmax, weights, thresholds, continuous=True, bounds=bounds, num_samples=10
    )

    # Print results
    print("Discrete Alternatives Utilities:")
    print(total_utilities_discrete)
    print("Discrete Alternatives Categories:")
    print(categories_discrete)

    print("\nContinuous Alternatives Utilities:")
    print(total_utilities_continuous)
    print("Continuous Alternatives Categories:")
    print(categories_continuous)

    # Visualize results
    visualize(A_discrete, total_utilities_discrete, title="UTA-DIS Discrete Alternatives")
    visualize(alts, total_utilities_continuous, title="UTA-DIS Continuous Alternatives")
