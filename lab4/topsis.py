from typing import List, Tuple
import numpy as np

def f1(x):
    return 2 * x + 5

def f2(x):
    return x * x - 3

def discrete_values(number_of_samples, min, max, function_lst):
    arg = np.linspace(min, max, number_of_samples)
    return [[function_lst[i](a) for i in range(len(function_lst))] for a in arg]

def get_minimum(x1, x2):
    min_x1 = [0 if x1[i] <= x2[i] else 1 for i in range(len(x1))]
    min_x2 = [0 if x2[i] <= x1[i] else 1 for i in range(len(x2))]
    if max(min_x1) == 0:
        return x1
    elif max(min_x2) == 0:
        return x2
    else:
        return None

def alg2(X):
    P = []
    dominated_points = []
    i = 0
    while i < len(X):
        was_removed = False
        Y = X[i]
        j = i + 1
        while j < len(X):
            min_val = get_minimum(Y, X[j])
            if min_val == Y:
                dominated_points.append(X[j])
                X.remove(X[j])
                was_removed = True
            elif min_val == X[j]:
                Y_temp = Y
                Y = X[j]
                dominated_points.append(Y_temp)
                X.remove(Y_temp)
                was_removed = True
            else:
                j += 1
        P.append(Y)
        k = 0
        X.remove(Y)
        while k < len(X):
            min_val = get_minimum(Y, X[k])
            if min_val == Y:
                dominated_points.append(X[k])
                X.remove(X[k])
                was_removed = True
            else:
                k += 1
        if len(X) == 1:
            P.append(X[0])
            return P, dominated_points
        if not was_removed:
            i += 1
    return P, dominated_points

def point_between_references(point: List[float], reference_points: [List[List[float]]]) -> bool:
    for i, p in enumerate(point):
        if p < reference_points[0][i] or p > reference_points[1][i]:
            return False
    return True


def topsis(alternatives: List[List[float]], reference_points: List[List[float]], weights: List[float]) -> List[Tuple[List[float], int]]:
    """
    Topsis method
    :param reference_points: list of reference points, alternatives should be between them
    :param alternatives: alternatives matrix (rows - alternatives, cols - criteria)
    :param weights: weights vector
    :return: Ranked alternatives (points and topsis score)
    """
    alternatives, _ = alg2(alternatives)
    # alternatives_number = len(alternatives)
    criteria_number = len(alternatives[0])
    # alternatives_OK_id = [i if point_between_references(alternatives[i], reference_points) else None for i in range(alternatives_number)]
    evaluation_list = []
    for alt in alternatives:
        if point_between_references(alt, reference_points):
            evaluation_list.append(alt)
    alternatives_number = len(evaluation_list)
    evaluation_matrix = np.array(evaluation_list)
    normalized_evaluation_matrix = evaluation_matrix / np.sqrt(np.sum(np.power(evaluation_matrix, 2)))
    scaled_matrix = normalized_evaluation_matrix * weights
    ideal_point = scaled_matrix.min(axis=0)
    antyideal_point = scaled_matrix.max(axis=0)
    distance_best = np.array([np.sqrt(np.sum(np.power(scaled_matrix[i] - ideal_point, 2))) for i in range(alternatives_number)])
    distance_worst = np.array([np.sqrt(np.sum(np.power(scaled_matrix[i] - antyideal_point, 2))) for i in range(alternatives_number)])
    topsis_score = distance_worst / (distance_best + distance_worst)
    result = [(evaluation_list[i], topsis_score[i]) for i in range(alternatives_number)]
    result.sort(key=lambda x: x[1], reverse=True)
    return result
    # dodać listę z krotkami id, topsis i uszeregować od największego topsis do najmniejszego

if __name__ == '__main__':
    alternatives = [[2, 2], [3, 1], [6, 7], [1, 3]]
    reference = [[0, 0], [7, 6]]
    weights = [0.6, 0.4]
    tops = topsis(alternatives, reference, weights)
    print(tops)
    print(discrete_values(10, 0, 5, [f1, f2]))