import numpy as np
import pandas as pd

from copy import deepcopy


def get_rank(A1, A2, D):
    n_alternatives, n_criteria = D.shape
    M1 = []
    M2 = []

    for i in range(n_alternatives):
        condition = False

        for k in range(A1.shape[0]):
            for j in range(n_criteria):
                if D[i, j] >= A1[k, j]:
                    condition = True

                else:
                    condition = False
                    break

        if condition:
            for k in range(A1.shape[0]):
                if np.equal(A1[k, :], D[i, :]).all():
                    break

            else:
                M1.append(D[i, :])

    M1 = np.array(M1)

    for i in range(M1.shape[0]):
        condition = False

        for k in range(A2.shape[0]):
            for j in range(n_criteria):
                if M1[i, j] <= A2[k, j]:
                    condition = True

                else:
                    condition = False
                    break

        if condition:
            for k in range(A2.shape[0]):
                if np.equal(A2[k, :], M1[i, :]).all():
                    break

            else:
                M2.append(M1[i, :])

    return np.array(M2) if M2 else A1


def get_incomparable_for_preference(D, pref):
    n_alternatives, n_criteria = D.shape
    incomparable_points = np.array([])

    for i in range(n_alternatives):
        n_greater = sum([1 for j in range(n_criteria) if pref[j] < D[i, j]])
        n_unequal = sum([1 for j in range(n_criteria) if pref[j] != D[i, j]])

        if n_unequal == 0 or 0 < n_greater < n_unequal:
            if incomparable_points.shape[0] == 0:
                incomparable_points = D[i, :].reshape((1, n_criteria))

            incomparable_points = np.concatenate((incomparable_points, D[i, :].reshape((1, n_criteria))), axis=0)

    return incomparable_points


def internal_contradiction(A):
    n_criteria = A.shape[1]
    incomparable_points_part = get_incomparable_points(A)
    non_dominated_point = incomparable_points_part[0, :]
    incomparable_points = non_dominated_point.reshape((1, n_criteria))

    while incomparable_points_part.shape[0] > 2:
        incomparable_points_part = get_incomparable_points(incomparable_points_part[1:, :])
        non_dominated_point = incomparable_points_part[0,:]
        incomparable_points = np.concatenate((non_dominated_point.reshape((1, n_criteria)), incomparable_points), axis=0)

    if incomparable_points_part.shape[0] == 2:
        incomparable_points = np.concatenate((incomparable_points_part[1, :].reshape((1, n_criteria)), incomparable_points), axis=0)

    return incomparable_points


def external_contradiction(A, B):
    n_criteria = A.shape[1]
    new_A = []

    for i in range(A.shape[0]):
        condition = False

        for k in range(B.shape[0]):
            for j in range(1, n_criteria):
                if A[i, j] >= B[k, j]:
                    condition = True

                else:
                    condition = False
                    break

            if condition:
                comparison = B[k, :]
                break

        if condition:
            if not np.equal(A[i, :], comparison).all():
                new_A.append(A[i, :])

    return np.array(new_A)


def reverse_criteria(D, directions):
    for i, direction in enumerate(directions):
        if direction == "max":
            D[:, i] = -D[:, i]

    return D


def get_incomparable_points(D):
    n_alternatives, n_criteria = D.shape
    incomparable_points = D[0,:].reshape((1, n_criteria))
    non_dominated_point = D[0,:]

    for i in range(1, n_alternatives):
        n_greater = sum([1 for j in range(n_criteria) if non_dominated_point[j] < D[i, j]])
        n_unequal = sum([1 for j in range(n_criteria) if non_dominated_point[j] != D[i, j]])

        if n_unequal == 0 or 0 < n_greater < n_unequal:
            incomparable_points = np.concatenate((incomparable_points, D[i, :].reshape((1, n_criteria))),axis=0)

        elif n_greater == 0:
            incomparable_points_old = incomparable_points
            non_dominated_point = D[i, :]

            if incomparable_points_old.shape[0] == 1:
                incomparable_points = non_dominated_point.reshape((1, n_criteria))

            else:
                incomparable_points_old = np.concatenate((non_dominated_point.reshape((1, n_criteria)), incomparable_points_old), axis=0)
                incomparable_points = get_incomparable_points(incomparable_points_old)

    return incomparable_points


def get_best_points(D, direction, n_criteria):
    if direction == 'max':
        D = -D

    incomparable_points = get_incomparable_points(D)
    non_dominated_point = incomparable_points[0, :]
    incomparable_points_part = incomparable_points
    incomparable_points = non_dominated_point.reshape((1, n_criteria))

    while incomparable_points_part.shape[0] > 2:
        incomparable_points_part = get_incomparable_points(incomparable_points_part[1:, :])
        non_dominated_point = incomparable_points_part[0, :]
        incomparable_points = np.concatenate((non_dominated_point.reshape((1, n_criteria)), incomparable_points), axis=0)

    if incomparable_points_part.shape[0] == 2:
        incomparable_points = np.concatenate((incomparable_points_part[1,:].reshape((1, n_criteria)), incomparable_points), axis=0)

    return -incomparable_points if direction == "max" else incomparable_points


def determine_sets(pref, pref_qwo, D, directions):
    D = reverse_criteria(D, directions)
    n_criteria = D.shape[1]

    A0 = get_best_points(D, 'min', n_criteria)
    A3 = get_best_points(D, 'max', n_criteria)

    A1 = get_incomparable_for_preference(D, pref)

    if A1.shape[0] == 0:
        A1 = deepcopy(A0)

    A1 = internal_contradiction(A1)
    A1 = external_contradiction(A1, A0)

    if A1.shape[0] == 0:
        A1 = deepcopy(A0)

    A2 = get_incomparable_for_preference(D, pref_qwo)

    if A2.shape[0] == 0:
        A2 = deepcopy(A3)

    A2 = internal_contradiction(A2)
    A2 = external_contradiction(A2, A1)

    if A2.shape[0] == 0:
        A2 = deepcopy(A3)

    M = get_rank(A1, A2, D)

    if M.shape[0] == 0:
        M = deepcopy(A1)

    if 'max' in directions:
        M = reverse_criteria(M, directions)

    return M


if __name__ == "__main__":
    pref = np.array([1.2, 15, -5])
    pref_qwo = np.array([3.5, 42, -1])
    D = pd.read_excel("dane.xlsx", sheet_name='Arkusz3', header=None).values
    directions = ['min', 'min', 'max']
    M = determine_sets(pref, pref_qwo, D, directions)
    print(M)