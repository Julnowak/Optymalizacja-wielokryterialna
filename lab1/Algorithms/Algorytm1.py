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


def bez_filtracji(X_in: List[List], directions: List[str]):
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
                    elif is_point1_dominating_point2(
                        point1=kolejny_elem, point2=Y, directions=directions
                    ):
                        # X(j) dominuje Y, aktualizujemy Y
                        zdominowane.append(Y)
                        aktywna_lista.remove(Y), X.remove(Y)
                        Y = kolejny_elem
                        fl = 1  # Zmiana flaga na 1
                    else:
                        print(f"Element nieporównywalny: {kolejny_elem}")
                        nieprownywalne.append(kolejny_elem)

                    j += 1
                    por_num += k
                    all_por += k
                    print(f"Liczba porównań: {por_num}")
                    print("Elementy usunięte:", zdominowane)
                    print("Punkty nieporównywalne:", nieprownywalne)
                    print(
                        "Pozostałe do sprawdzenia: ",
                        [elem for elem in X if elem not in nieprownywalne][1:],
                    )
                    print("Punkty niezdominowane: ", P)

            # Dodajemy Y do listy punktów niezdominowanych
            P += [Y]

            if fl == 0:
                # Jeśli flaga równa 0, usuwamy Y z X
                X.remove(Y)

            i += 1

        print(f"Zdominowane: {zdominowane}")
        unikalne_P = []
        print(f"Liczba porównań: {all_por}")
        [unikalne_P.append(p) for p in P if p not in unikalne_P]
        return unikalne_P  # Zwróć unikalne punkty jako listę


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    X = [
        [2, 1],
        [6, 2],
        [1, 0],
        [4, 4],
        [4, 0],
        [5, 0],
        [4, 2],
        [1, 2],
        [2, 2],
        [2, 1]
    ]

    P = bez_filtracji(X_in=X, directions=["min", "max"])
    print("Punkty niezdominowane (bez filtracji):", P)
