import random
import numpy as np


def calculate_neighbourhood(point, map_size):
    neigh = []
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            p = [point[0] + i, point[1]+j]
            if p[0] >= 0 and p[1] >= 0 and p[0] <= map_size[0] and p[1] <= map_size[1] and p != point:
                neigh.append(p)
    return neigh

# print(calculate_neighbourhood([0,0], [20,20]))
# print(calculate_neighbourhood([1,1], [20,20]))


def count_fits(large):
    counter = 0
    actual = large.copy()
    # pełne
    while actual[0] != 0 and actual[1] != 0:
        # Oblicz ile razy mniejszy prostokąt zmieści się w dużym wzdłuż każdej os
        actual[0] -= 1
        actual[1] -= 1
        counter += 1

    # reszty
    if actual[0] != 0:
        counter += actual[0]
    elif actual[1] != 0:
        counter += actual[1]

    # Zwróć całkowitą liczbę mniejszych prostokątów
    return counter


def step_distance(p1, p2):
    suma = 0
    if len(p1) < len(p2):
        for i in range(len(p2)):
            if i < len(p1):
                n = [np.abs(p1[i][0] - p2[i][0]), np.abs(p1[i][1] - p2[i][1])]
            else:
                n = [np.abs(0 - p2[i][0]), np.abs(0 - p2[i][1])]
            suma += count_fits(n)
            print(suma)

    elif len(p2) < len(p1):
        for i in range(len(p1)):
            if i < len(p2):
                n = [np.abs(p1[i][0] - p2[i][0]), np.abs(p1[i][1] - p2[i][1])]
            else:
                n = [np.abs(p1[i][0] - 0), np.abs(p1[i][1] - 0)]
            suma += count_fits(n)
    else:

        for i in range(len(p1)):
            n = [np.abs(p1[i][0] - p2[i][0]), np.abs(p1[i][1] - p2[i][1])]
            suma += count_fits(n)

    return suma

#
# print(step_distance([[1,2], [3,4]], [[1,1], [6,4]]))
# print(step_distance([[1,2], [3,4]], [[1,1], [6,4], [4,2]]))
# print(step_distance([[1,2], [3,4], [0,0]], [[1,1], [6,4]]))


def cso_step(actual, best):
    new_actual = actual.copy()
    print(new_actual)
    if len(actual) < len(best):
        new_actual.append(best[-1])
    elif len(best) < len(actual):
        new_actual.pop(-1)
    else:
        for i in range(len(actual)):
            if actual[i] != best[i]:
                if actual[i][0] < best[i][0] and actual[i][1] < best[i][1]:
                    new_actual[i][0] += 1
                    new_actual[i][1] += 1
                elif actual[i][0] < best[i][0] and actual[i][1] == best[i][1]:
                    new_actual[i][0] += 1
                elif actual[i][0] < best[i][0] and actual[i][1] > best[i][1]:
                    new_actual[i][0] += 1
                    new_actual[i][0] -= 1
                elif actual[i][0] == best[i][0] and actual[i][1] < best[i][1]:
                    new_actual[i][1] += 1
                elif actual[i][0] == best[i][0] and actual[i][1] > best[i][1]:
                    new_actual[i][1] -= 1
                elif actual[i][0] > best[i][0] and actual[i][1] > best[i][1]:
                    new_actual[i][0] -= 1
                    new_actual[i][1] -= 1
                elif actual[i][0] > best[i][0] and actual[i][1] == best[i][1]:
                    new_actual[i][0] -= 1
                elif actual[i][0] > best[i][0] and actual[i][1] < best[i][1]:
                    new_actual[i][0] -= 1
                    new_actual[i][0] += 1
                break
    return new_actual




#
# print(cso_step([[1,2], [4,4]],[[1,1], [6,4]]))
# print(cso_step([[1,2], [4,4], [9,9]],[[1,1], [6,4]]))
# print(cso_step([[1,1], [6,4]], [[1,2], [4,4], [9,9]],))



