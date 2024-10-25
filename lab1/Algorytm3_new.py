import numpy as np
from typing import List
import math


def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


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
        # print(f'Punkt {point1} dominuje punkt {point2}')
        return True
    else:
        return False


def algorytm_oparty_o_punkt_idealny(X_new, directions):
    X = X_new.copy()

    all_por = 0
    if not len(directions) == len(X[0]):
        print("Liczba kierunków optymalizacji nie zgadza się z liczbą parametrów")
    else:
        P = []
        unikalne_P = []

        x_min = np.inf
        y_min = np.inf
        for x in X:
            if x_min > x[0]: x_min = x[0]
            if y_min > x[1]: y_min = x[1]

        ideal = [x_min, y_min]
        print(ideal)
        n = len(X)
        j=0
        d = dict()
        while j < n:
            d[j] = distance(ideal, X[j])
            j += 1

        d_sorted = sorted(d.items(), key=lambda v: v[1])
        M = n
        m = 0
        actual = X.copy()
        while m <= M:
            all_por += 2
            for i in range(len(actual)):

                if X[d_sorted[m][0]] <= X[i]:
                    try:
                        actual.remove(X[i])
                    except:
                        pass
            P.append(X[m])
            try:
                actual.remove(X[m])
            except:
                pass
            M = M-1
            m = m+1
        # print(f"Zdominowane: {zdominowane}")
        [unikalne_P.append(p) for p in P if p not in unikalne_P]
        print("Wszystkie porównania: ", all_por)
        return unikalne_P  # Zwróć unikalne punkty jako listę

# Oczekiwane
# Liczba porównań: 24
# (3, 3)
# (4, 1)
# (1, 8)


if __name__ == "__main__":
    X = [
        [5, 5],
        [3, 6],
        [4, 4],
        [5, 3],
        [3, 3],
        [1, 8],
        [3, 4],
        [4, 5],
        [3, 10],
        [6, 6],
        [4, 1],
        [3, 5],
    ]

    P = algorytm_oparty_o_punkt_idealny(X, directions=["min", "min"])
    print("Punkty niezdominowane (punkt idealny):", P)
