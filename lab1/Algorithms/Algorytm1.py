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
        return True
    else:
        return False


def bez_filtracji(X_in: List[List], directions: List[str], flag: bool = False):
    X = X_in.copy()

    all_por = 0
    if not len(directions) == len(X[0]):
        print("Liczba kierunków optymalizacji nie zgadza się z liczbą parametrów")
    else:
        P = []
        zdominowane = []
        k = len(directions)
        i = 0
        while len(X):
            aktywna_lista = X.copy()
            Y = aktywna_lista[0]
            fl = 0
            j = 1
            nieprownywalne = []
            n = len(aktywna_lista)
            if len(X) != 1:
                while j < n:
                    por_num = 0
                    aktywna_lista = [elem for elem in X if elem not in nieprownywalne]
                    if len(aktywna_lista) > 1:
                        kolejny_elem = aktywna_lista[1].copy()
                        if is_point1_dominating_point2(
                            point1=Y, point2=kolejny_elem, directions=directions
                        ):
                            # Y dominuje X(j), usuwamy X(j)
                            zdominowane.append(kolejny_elem)
                            X.remove(kolejny_elem)
                        elif is_point1_dominating_point2(
                            point1=kolejny_elem, point2=Y, directions=directions
                        ):
                            # X(j) dominuje Y, aktualizujemy Y
                            zdominowane.append(Y)
                            aktywna_lista.remove(Y), X.remove(Y)
                            Y = kolejny_elem
                            fl = 1  # Zmiana flaga na 1
                        else:
                            nieprownywalne.append(kolejny_elem)

                    j += 1
                    por_num += k
                    all_por += k

            # Dodajemy Y do listy punktów niezdominowanych
            P += [Y]

            if fl == 0:
                # Jeśli flaga równa 0, usuwamy Y z X
                X.remove(Y)

            i += 1

        unikalne_P = []
        [unikalne_P.append(p) for p in P if p not in unikalne_P]
        return unikalne_P, zdominowane, all_por  # Zwróć unikalne punkty jako listę


# Press the green button in the gutter to run the script.
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

    P,r,t = bez_filtracji(X_in=X, directions=["Min", "Min"])
    print("Punkty niezdominowane (bez filtracji):", P)
