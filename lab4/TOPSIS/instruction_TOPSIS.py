import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def fuzzy_topsis(alternatives, criteria, weights):
    """
    Fuzzy TOPSIS Algorithm.
    :param alternatives: Array of alternatives, each represented as an array of triangular fuzzy numbers.
    :param criteria: Type of each criterion ('benefit' or 'cost').
    :param weights: Array of weights, each represented as a triangular fuzzy number.
    :return: Ranking of alternatives and intermediate matrices.
    """
    # Fuzzy normalization
    num_alternatives, num_criteria = len(alternatives), len(criteria)

    def normalize_fuzzy(value, ideal):
        """Normalize a fuzzy value based on ideal solution."""
        return [(value[0] / ideal[2]), (value[1] / ideal[1]), (value[2] / ideal[0])]

    # Calculate fuzzy ideal and anti-ideal solutions
    ideal = []
    anti_ideal = []
    for j in range(num_criteria):
        col = [alt[j] for alt in alternatives]
        if criteria[j] == 'benefit':
            ideal.append([max(c[0] for c in col), max(c[1] for c in col), max(c[2] for c in col)])
            anti_ideal.append([min(c[0] for c in col), min(c[1] for c in col), min(c[2] for c in col)])
        elif criteria[j] == 'cost':
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


    # print("\nIdealny punkt:")
    # print(ideal)
    # print("\nAntyidealny punkt:")
    # print(anti_ideal)
    # print("\nOdległości do idealnego:")
    # print(distances_ideal)
    # print("\nOdległości do antyidealnego:")
    # print(distances_anti_ideal)
    # print("\nBliskość:")
    # print(closeness)

    # Return ranking
    return np.argsort(closeness)[::-1], {
        "normalized": normalized,
        "weighted": weighted,
        "distances_ideal": distances_ideal,
        "distances_anti_ideal": distances_anti_ideal,
        "closeness": closeness,
    }


# Fuzzy triangular numbers: (l, m, u)
# Example for continuous case with U⊂R^4 and N=4
alternatives_continuous = [
    [(1, 3, 5), (2, 4, 6), (3, 5, 7), (1, 2, 3)],
    [(2, 4, 6), (1, 3, 5), (2, 4, 6), (2, 3, 4)],
    [(3, 5, 7), (3, 5, 7), (1, 3, 5), (2, 4, 6)],
    [(1, 2, 3), (2, 3, 4), (3, 5, 7), (3, 5, 7)],
]

criteria_continuous = ['benefit', 'cost', 'benefit', 'cost']
weights_continuous = [(0.2, 0.5, 0.8), (0.3, 0.6, 0.9), (0.4, 0.7, 1.0), (0.1, 0.4, 0.7)]

ranking_continuous, details_continuous = fuzzy_topsis(alternatives_continuous, criteria_continuous, weights_continuous)

print("Continuous Case Ranking:", ranking_continuous)
print("Details (Continuous):", details_continuous)

# Example for discrete case with N=3 and N=4
alternatives_discrete = [
    [(1, 2, 3), (3, 4, 5), (2, 3, 4)],
    [(2, 3, 4), (1, 2, 3), (3, 4, 5)],
    [(3, 4, 5), (2, 3, 4), (1, 2, 3)],
]

criteria_discrete = ['benefit', 'cost', 'benefit']
weights_discrete = [(0.3, 0.6, 0.9), (0.2, 0.5, 0.8), (0.5, 0.8, 1.0)]

ranking_discrete, details_discrete = fuzzy_topsis(alternatives_discrete, criteria_discrete, weights_discrete)

print("\nDiscrete Case Ranking:", ranking_discrete)
print("Details (Discrete):", details_discrete)

alternatives_discrete = [
    [(1, 1, 1), (1, 1, 1), (1, 1, 1)],
    [(2, 2, 2), (2, 2, 2), (2, 2, 2)],
    [(3, 3, 3), (3, 3, 3), (3, 3, 3)],
    [(32, 42, 52), (22, 32, 42), (12, 22, 32)],
]

criteria_discrete = ['cost', 'cost', 'cost']
weights_discrete = [(0.3, 0.6, 0.1), (0.2, 0.5, 0.3), (0.1, 0.8, 0.1), (0.5, 0.2, 0.3)]

ranking_discrete, details_discrete = fuzzy_topsis(alternatives_discrete, criteria_discrete, weights_discrete)

print("\nDiscrete Case Ranking:", ranking_discrete)
print("Details (Discrete):", details_discrete)



# Przetwarzanie danych: wybieramy środkowy punkt w każdej liście
x = [item[0][1] for item in alternatives_discrete]
y = [item[1][1] for item in alternatives_discrete]
z = [item[2][1] for item in alternatives_discrete]

# Tworzenie wykresu 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

x = [item[0][1] for item in alternatives_discrete]
y = [item[1][1] for item in alternatives_discrete]
z = [item[2][1] for item in alternatives_discrete]

ax.scatter(x, y, z, color='red')

# Dodanie etykiet
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.legend()

# Wyświetlenie wykresu
plt.show()