from typing import List
from math import sqrt
from main import is_point1_dominating_point2


def find_optimum_according_to_directions(X: List[List[int]], directions):
    result: List[int] = []

    for i in range(len(directions)):
        if directions[i] == "min":
            result.append(min([x[i] for x in X]))
        elif directions[i] == "max":
            result.append(max([x[i] for x in X]))

    return result


def calculate_distance(x: List[int], y: List[int]):
    return sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))


def punkt_idealny(X_in: List[List], directions: List[str], flag: bool = False):
    X = X_in.copy()

    if not len(directions) == len(X[0]):
        print("Liczba kierunków optymalizacji nie zgadza się z liczbą parametrów")
    else:
        P = []
        xmin = find_optimum_according_to_directions(X=X, directions=directions)

        d = [calculate_distance(xmin, point) for point in X]
        J = sorted(range(len(d)), key=lambda i: d[i])

        D = [d[i] for i in J]
        m = 0
        M = len(X)
        all_por = 0
        while len(X) > 1:
            current_point = X_in[J[m]]
            if current_point in X:
                P.append(current_point)
                X.remove(current_point)
                M -= 1
            dominated_points = []
            for p in X:
                all_por += 2
                if is_point1_dominating_point2(
                    point1=current_point, point2=p, directions=directions
                ):
                    dominated_points.append(p)
            for dp in dominated_points:
                X.remove(dp)
                M -= 1
            m += 1

        try:
            P.append(X[0])
        except:
            pass

        unikalne_P = []
        [unikalne_P.append(p) for p in P if p not in unikalne_P]
        print(f"Ilość porównań: {all_por}")
        return unikalne_P, dominated_points, all_por  # Zwróć unikalne punkty jako listę


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

    P = punkt_idealny(X_in=X, directions=["min", "min"])
    print("Punkty niezdominowane (punkt idealny):", P)
