import numpy as np
from typing import List


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


def algorytm_z_filtracja(X_new, directions: List[str]):
    X = X_new.copy()

    all_por = 0
    if not len(directions) == len(X[0]):
        print("Liczba kierunków optymalizacji nie zgadza się z liczbą parametrów")
    else:
        P = []
        zdominowane = []
        i = 0
        while len(X):
            left = X.copy()
            print(f"\n=== Iteracja {i + 1} ===")
            aktywna_lista = X.copy()
            Y = aktywna_lista[0]
            j = 1
            nieprownywalne = []
            n = len(aktywna_lista)
            if len(X) != 1:
                while j < n:
                    por_num = 0
                    aktywna_lista = [elem for elem in X if elem not in nieprownywalne]
                    kolejny_elem = aktywna_lista[1].copy()
                    print(f"\n--- Iteracja {i + 1}, {j} ---")
                    print(f"Element aktywny: {Y}")
                    print(f"Kolejny element: {kolejny_elem}")

                    try:
                        left.remove(Y)
                    except:
                        pass

                    try:
                        left.remove(kolejny_elem)
                    except:
                        pass

                    if is_point1_dominating_point2(
                            point1=Y, point2=kolejny_elem, directions=directions
                    ):
                        # Y dominuje X(j), usuwamy X(j)
                        zdominowane.append(kolejny_elem)
                        X.remove(kolejny_elem)
                        # print(f"Usunięto element: {kolejny_elem}")
                    elif is_point1_dominating_point2(
                            point1=kolejny_elem, point2=Y, directions=directions
                    ):

                        zdominowane.append(Y)
                        aktywna_lista.remove(Y), X.remove(Y)
                        Y = kolejny_elem
                    else:
                        # print(f"Element nieporównywalny: {kolejny_elem}")
                        nieprownywalne.append(kolejny_elem)

                    j += 1
                    por_num += 2
                    all_por += 2
                    print(f"Liczba porównań: {por_num}")
                    print("Elementy usunięte:", zdominowane)
                    print("Punkty nieporównywalne:", nieprownywalne)
                    print("Pozostałe do sprawdzenia: ", left)
                    print("Punkty niezdominowane: ", P)
                print("dddddddddddddddddddd", all_por)
            # Dodajemy Y do listy punktów niezdominowanych
            P += [Y]

            print(f"X:{X}")
            print(f"AL:{aktywna_lista}")
            print(f"Left:{left}")
            print(f"Left:{nieprownywalne}")
            # X = [x for x in X if not all(x1 >= x2 for x1, x2 in zip(x, Y))]
            new = []

            aktywna_lista.remove(Y), X.remove(Y)
            print(f"AL:{aktywna_lista}")
            print(f"\n{i+1}F iteracja\n")
            if not (len(nieprownywalne) == 1 and kolejny_elem in nieprownywalne):
                for x in nieprownywalne:
                    all_por += 2
                    print(x)
                    for x1, x2 in zip(x, Y):
                        print(x1,x2)
                        if not x1 >= x2:
                            new += [x]
                print(new)
                print("num:", all_por)
                X = new

            print(f"Pozostałe elementy X: {X}")

            # Jeśli pozostał jeden element, dodajemy go do listy P
            if len(X) == 1:
                P.append(X[0])
                print(f"Dodano ostatni element do P: {X[0]}")
                break
            i += 1

    print(f"Zdominowane: {zdominowane}")

    unikalne_P = []
    [unikalne_P.append(p) for p in P if p not in unikalne_P]
    print("Wszystkie porównania: ", all_por)
    print(f"Niezdominowane: {unikalne_P}")
    return unikalne_P  # Zwróć unikalne punkty jako listę


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

    P = algorytm_z_filtracja(X, directions=["min", "min"])
    print("Punkty niezdominowane (z filtracją):", P)
