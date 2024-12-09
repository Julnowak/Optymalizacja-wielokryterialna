from typing import List, Tuple, Union
import numpy as np
from math import sqrt
import matplotlib
from numpy._typing import NDArray

from UTA_BIS.UTA_DIS import visualize

matplotlib.use("TkAgg")


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
    decision_matrix: List[List[float]], min_max_criterial: List[bool]
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
                if min_max_criterial[k]
                else decision_matrix[i][k] <= decision_matrix[j][k]
                for k in range(len(min_max_criterial))
            ]
            if all(temp):  # Jeśli wszystkie elementy są True
                lstzd.append(decision_matrix[i])
                break
        else:
            lstnzd.append(decision_matrix[i])
    return lstnzd, lstzd


def rsm_discrete(
    reference_points: NDArray[float],
    decision_points: NDArray[float],
    min_max: List[bool],
    classes,
) -> List[Tuple[List, float]]:
    """
    Reference Set Method (RSM) w wariancie dyskretnym.
    :param reference_points: punkty referencyjne w przestrzeni kryteriów.
    :param decision_points: punkty decyzyjne
    :param min_max: Lista True (maksymalizacja) lub False (minimalizacja) dla każdego kryterium.
    :param classes:
    :return: Zbiór punktów z obliczonymi odległościami do punktu referencyjnego.
    """
    reference_points_list = reference_points.tolist()
    decision_points_list = decision_points.tolist()
    R_plus, R_minus = zdominowane(reference_points_list, min_max)

    scores = []
    for point in decision_points_list:
        d_plus = min([distance(point, r_plus) for r_plus in R_plus])
        d_minus = min([distance(point, r_minus) for r_minus in R_minus])

        scores.append((point, d_minus - d_plus))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores


def rsm_continuous(
    num_samples: int,
    reference_points: NDArray[float],
    min_max: List[bool],
    classes,
    bounds: Union[List[Tuple[float, float]], float] = 0,
) -> List[Tuple[List, float]]:
    """
    Reference Set Method (RSM) w wariancie ciągłym.
    :param num_samples: liczba próbek.
    :param bounds: lista krotek (min, max) dla każdego kryterium.
    :param min_max: Lista True (maksymalizacja) lub False (minimalizacja) dla każdego kryterium.
    :param reference_points: punkt referencyjny w przestrzeni kryteriów.
    :return: Zbiór punktów z obliczonymi odległościami do punktu referencyjnego.
    :param classes:
    """
    if bounds == 0:
        bounds = [(0, 10) for _ in range(len(min_max))]

    reference_points_list = reference_points.tolist()
    samples = [np.linspace(b[0], b[1], num_samples) for b in bounds]
    samples_mesh = np.array(np.meshgrid(*samples)).T.reshape(-1, len(bounds)).tolist()

    R_plus, R_minus = zdominowane(reference_points_list, min_max)

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

    # Dla przestrzeni 3D (dyskretne)
    A_3d = np.array(
        [[2, 3, 4],
         [-1, 1, 2],
         [1, 3, 4],
         [1, 1, 2],
         [2, 2, 4],
         [0, 0, 0]])
     # Punkty odniesienia (3D)

    B_3d = np.array(
        [[3, 4, 5],
         [5, 1, 2],
         [1, 2, 3],
         [3, 3, 4]]
    )  # Punkty dopuszczalne (3D)

    # Obliczanie punktów i ich odległości
    discrete_results_3d = rsm_discrete(
        reference_points=A_3d,
        decision_points=B_3d,
        min_max=[False, False, False],
        classes=0,
    )
    data, utilities = zip(*discrete_results_3d)
    data = np.array(data)
    utilities = np.array(utilities)

    visualize(data=data, utilities=utilities)

    print("Punkty w wariancie dyskretnym (posortowane według odległości):")
    for point, score in discrete_results_3d:
        print(f"Point: {np.round(point, 4)}, Score: {score:.4f}")

    # Dla przestrzeni 3D (ciągłe)
    bounds_continuous_3d = [(0, 10), (5, 15), (1, 5)]  # Granice dla przestrzeni 3D
    A_3d_cont = np.array([[0, 0, 0], [5, 5, 5]])  # Punkty odniesienia (3D)

    continuous_results_3d = rsm_continuous(
        num_samples=5,
        bounds=bounds_continuous_3d,
        reference_points=A_3d_cont,
        min_max=[False, False, False],
        classes=0,
    )

    data2, utilities2 = zip(*continuous_results_3d)
    data2 = np.array(data2)
    utilities2 = list(utilities2)

    visualize(data=data2, utilities=utilities2)

    print("\nPunkty w wariancie ciągłym (posortowane według odległości):")
    for point, score in continuous_results_3d[:10]:
        print(f"Point: {np.round(point, 4)}, Score: {score:.4f}")

    # A_4d = np.array([
    #     [2, 3, 4, 5],
    #     [-1, 1, 2, 3],
    #     [1, 3, 4, 5],
    #     [1, 1, 2, 2],
    #     [2, 2, 4, 5],
    #     [0, 0, 0, 0],
    # ])  # Punkty odniesienia (4D)
    # B_4d = np.array([
    #     [3, 4, 5, 6],
    #     [5, 1, 2, 3],
    #     [1, 2, 3, 4],
    #     [3, 3, 4, 5],
    # ])  # Punkty dopuszczalne (4D)
    #
    # discrete_results_4d = rsm_discrete(
    #     reference_points=A_4d,
    #     decision_points=B_4d,
    #     min_max=[False, False, False, False],
    #     classes=0
    # )
    #
    # print("Punkty w wariancie dyskretnym (4D):")
    # for point, score in discrete_results_4d:
    #     print(f"Point: {np.round(point, 4)}, Score: {score:.4f}")
    #
    # # Dla przestrzeni 4D (ciągłe)
    # bounds_continuous_4d = [
    #     (0, 10),
    #     (5, 15),
    #     (1, 5),
    #     (0, 10),
    # ]  # Granice dla przestrzeni 4D
    # A_4d_cont = np.array([[0, 0, 0, 0], [5, 5, 5, 5]])  # Punkty odniesienia (4D)
    #
    # continuous_results_4d = rsm_continuous(
    #     num_samples=5,
    #     bounds=bounds_continuous_4d,
    #     reference_points=A_4d_cont,
    #     min_max=[False, False, False, False],
    #     classes=0
    # )
    #
    # print("\nPunkty w wariancie ciągłym (4D):")
    # for point, score in continuous_results_4d:
    #     print(f"Point: {np.round(point, 4)}, Score: {score:.4f}")
