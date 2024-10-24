
def algorytm_z_filtracja(X):
    P = []
    zdominowane = []
    all_por = 0
    i = 0
    while len(X):
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
                if all(x1 <= x2 for x1, x2 in zip(Y, kolejny_elem)):
                    # Y dominuje X(j), usuwamy X(j)
                    zdominowane.append(kolejny_elem)
                    X.remove(kolejny_elem)
                    print(f"Usunięto element: {kolejny_elem}")
                elif all(x1 >= x2 for x1, x2 in zip(Y, kolejny_elem)):
                    # X(j) dominuje Y, aktualizujemy Y
                    print(f"Usunięto element: {Y}")
                    zdominowane.append(Y)
                    aktywna_lista.remove(Y), X.remove(Y)
                    Y = kolejny_elem
                else:
                    print(f"Element nieporównywalny: {kolejny_elem}")
                    nieprownywalne.append(kolejny_elem)

                    # X = np.delete(X, np.where(X == X[j, :])[0][0], axis=0)
                    # print(X)
                j += 1
                por_num += 2
                all_por += por_num
                print(f"Liczba porównań: {por_num}")

        # Dodajemy Y do listy punktów niezdominowanych
        P += [Y]

        aktywna_lista.remove(Y), X.remove(Y)

        print(f"X:{X}")
        print(f"AL:{aktywna_lista}")
        # X = [x for x in X if not all(x1 >= x2 for x1, x2 in zip(x, Y))]
        new = []
        u = 0

        Xn = X.copy()

        for x in Xn:
            u += 2
            all_por += u
            for x1, x2 in zip(x, Y):
                if not x1 >= x2:
                    new += [x]

        print(f"Porównania F: {u}")
        X = new


        print(f"Pozostałe elementy X: {X}")

        # Jeśli pozostał jeden element, dodajemy go do listy P
        if len(X) == 1:
            P.append(X[0])
            print(f"Dodano ostatni element do P: {X[0]}")
            break

        print(X)
        i += 1
    print(f"Porównania F: {all_por}")
    print(f"Zdominowane: {zdominowane}")
    unikalne_P = []
    [unikalne_P.append(p) for p in P if p not in unikalne_P]
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

    P = algorytm_z_filtracja(X)
    print("Punkty niezdominowane (z filtracją):", P)
