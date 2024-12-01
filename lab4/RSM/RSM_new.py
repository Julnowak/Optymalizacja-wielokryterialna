from typing import List, Tuple
import numpy as np
from math import sqrt


def is_point1_dominating_point2(
    point1: List[int], point2: List[int], directions: List[str]
):
    result: List[bool] = []
    for i in range(len(directions)):
        if directions[i] == "min":
            result.append(all(x1 <= x2 for x1, x2 in zip(point1, point2)))
        elif directions[i] == "max":
            result.append(all(x1 >= x2 for x1, x2 in zip(point1, point2)))

    if all(result):
        return True
    else:
        return False


def distance(x: List[float], y: List[float]):
    return sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))


def zdominowane(
    decision_matrix: List[List[float]], min_max_criterial: List["str"]
) -> Tuple[List[List[float]], List[List[float]]]:
    lstnzd = []
    lstzd = []

    for i in range(len(decision_matrix)):
        # is_dominated = False
        for j in range(len(decision_matrix)):
            if i == j:
                continue
            # Sprawdzenie czy j dominuje i
            temp = [
                decision_matrix[i][k] >= decision_matrix[j][k]
                if min_max_criterial[k] == "min"
                else decision_matrix[i][k] <= decision_matrix[j][k]
                for k in range(len(min_max_criterial))
            ]
            if all(temp):  # Jeśli wszystkie elementy są True
                # is_dominated = True
                lstzd.append(decision_matrix[i])
                break
        # if not is_dominated:
        else:
            lstnzd.append(decision_matrix[i])

    # Elementy zdominowane to te, które nie są w lstnzd
    # lstzd = [row for row in decision_matrix if row not in lstnzd]

    return lstnzd, lstzd


def rsm_discrete(
    reference_points: List[List[float]],
    decision_points: List[List[float]],
    min_max_criterial: List[str],
):
    """
    Reference Set Method (RSM) w wariancie dyskretnym.
    :param reference_points: punkty referencyjne w przestrzeni kryteriów.
    :param decision_points: punkty decyzyjne
    :param min_max_criterial: lista kryteriów
    :return: Zbiór punktów z obliczonymi odległościami do punktu referencyjnego.
    """
    R_plus, R_minus = zdominowane(reference_points, min_max_criterial)

    scores = []
    for point in decision_points:
        d_plus = min([distance(point, r_plus) for r_plus in R_plus])
        d_minus = min([distance(point, r_minus) for r_minus in R_minus])

        scores.append((point, d_minus - d_plus))

    return scores


def rsm_continuous(
    num_samples: int,
    bounds: List[Tuple[float, float]],
    reference_points: List[List[float]],
    min_max_criterial: List[str],
):
    """
    Reference Set Method (RSM) w wariancie ciągłym.
    :param min_max_criterial: lista kryteriów
    :param num_samples: liczba próbek.
    :param bounds: lista krotek (min, max) dla każdego kryterium.
    :param reference_points: punkt referencyjny w przestrzeni kryteriów.
    :return: Zbiór punktów z obliczonymi odległościami do punktu referencyjnego.
    """
    samples = [np.linspace(b[0], b[1], num_samples) for b in bounds]
    samples_mesh = np.array(np.meshgrid(*samples)).T.reshape(-1, len(bounds)).tolist()

    R_plus, R_minus = zdominowane(reference_points, min_max_criterial)

    # Obliczanie odległości punktów od referencyjnych
    scores = []
    for point in samples_mesh:
        d_plus = min([distance(point, r_plus) for r_plus in R_plus])
        d_minus = min([distance(point, r_minus) for r_minus in R_minus])

        scores.append((point, d_minus - d_plus))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores


# Przykład wariantu ciągłego
if __name__ == "__main__":
    min_max = [np.min, np.min]
    A = [[2, 3], [-1, 1], [1, 3], [1, 1], [2, 2], [0, 0]]  # punkty odniesienia
    B = [[3, 4], [5, 1], [1, 2], [3, 3]]  # punkty dopuszczalne

    # Obliczanie punktów i ich odległości
    discrete_results = rsm_discrete(
        reference_points=A, decision_points=B, min_max_criterial=["min", "min"]
    )

    print("Punkty w wariancie dyskretnym (posortowane według odległości):")
    for point, score in discrete_results:
        print(f"Point: {np.round(point, 4)}, Score: {score:.4f}")

    bounds_continuous = [(3, 1), (2, 1)]  # U ⊂ R⁴
    A = [[0, 0], [5, 5]]

    continuous_results = rsm_continuous(
        num_samples=5,
        bounds=bounds_continuous,
        reference_points=A,
        min_max_criterial=["min", "min"],
    )
    print("\nPunkty w wariancie ciągłym (posortowane według odległości):")
    for point, score in continuous_results:
        print(f"Point: {np.round(point, 4)}, Score: {score:.4f}")
