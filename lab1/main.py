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


def bez_filtracji(X: List[List], directions: List[str]):
    if not len(directions) == len(X[0]):
        print("Liczba kierunków optymalizacji nie zgadza się z liczbą parametrów")
    else:
        P = []
        zdominowane = []
        i = 0
        while len(X):
            print(f"\n=== Iteracja {i + 1} ===")
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
                    kolejny_elem = aktywna_lista[1].copy()
                    print(f"\n--- Iteracja {i+1}, {j} ---")
                    print(f"Element aktywny: {Y}")
                    print(f"Kolejny element: {kolejny_elem}")
                    if is_point1_dominating_point2(
                        point1=Y, point2=kolejny_elem, directions=directions
                    ):
                        # Y dominuje X(j), usuwamy X(j)
                        zdominowane.append(kolejny_elem)
                        X.remove(kolejny_elem)
                        print(f"Usunięto element: {kolejny_elem}")
                    elif is_point1_dominating_point2(
                        point1=kolejny_elem, point2=Y, directions=directions
                    ):
                        # X(j) dominuje Y, aktualizujemy Y
                        print(f"Usunięto element: {Y}")
                        zdominowane.append(Y)
                        aktywna_lista.remove(Y), X.remove(Y)
                        Y = kolejny_elem
                        fl = 1  # Zmiana flaga na 1
                    else:
                        print(f"Element nieporównywalny: {kolejny_elem}")
                        nieprownywalne.append(kolejny_elem)

                    j += 1
                    por_num += 2
                    print(f"Liczba porównań: {por_num}")

            # Dodajemy Y do listy punktów niezdominowanych
            P += [Y]

            if fl == 0:
                # Jeśli flaga równa 0, usuwamy Y z X
                X.remove(Y)

            i += 1

        print(f"Zdominowane: {zdominowane}")
        unikalne_P = []
        [unikalne_P.append(p) for p in P if p not in unikalne_P]
        return unikalne_P  # Zwróć unikalne punkty jako listę


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

    P = bez_filtracji(X=X, directions=["min", "min"])
    print("Punkty niezdominowane (bez filtracji):", P)
