import numpy as np
from typing import List


def is_point1_dominating_point2(
    point1: List[float], point2: List[float], directions: List[str]
):
    result: List[bool] = []
    for i in range(len(directions)):
        if directions[i] == "Min":
            result.append(point1[i] <= point2[i])
        elif directions[i] == "Max":
            result.append(point1[i] >= point2[i])

    if all(result):
        # print(f'Punkt {point1} dominuje punkt {point2}')
        return True
    else:
        return False


def algorytm_z_filtracja(X_new, directions: List[str], flag: bool = False):
    X = X_new.copy()
    zdominowane = []

    all_por = 0
    if not len(directions) == len(X[0]):
        print("Liczba kierunków optymalizacji nie zgadza się z liczbą parametrów")
    else:
        k = len(directions)
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
                    if flag:
                        return None, None, None
                    por_num = 0
                    aktywna_lista = [elem for elem in X if elem not in nieprownywalne]
                    if len(aktywna_lista) > 1:
                        kolejny_elem = aktywna_lista[1].copy()
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
                    por_num += k
                    all_por += k
            # Dodajemy Y do listy punktów niezdominowanych
            P += [Y]

            new = []

            aktywna_lista.remove(Y), X.remove(Y)
            if not (len(nieprownywalne) == 1 and kolejny_elem in nieprownywalne):
                for x in nieprownywalne:
                    all_por += k
                    # print(x)
                    if not is_point1_dominating_point2(point1=Y, point2=x, directions=directions):
                        new += [x]
                    else:
                        zdominowane += [x]
                X = new


            # Jeśli pozostał jeden element, dodajemy go do listy P
            if len(X) == 1:
                P.append(X[0])
                break
            i += 1


    unikalne_P = []
    [unikalne_P.append(p) for p in P if p not in unikalne_P]
    return unikalne_P, zdominowane, all_por  # Zwróć unikalne punkty jako listę


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

    P, zd, i = algorytm_z_filtracja(X, directions=["Min", "Min"])
    print("Punkty niezdominowane (z filtracją):", P)
