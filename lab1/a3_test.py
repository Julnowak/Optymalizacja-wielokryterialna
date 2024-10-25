def ideal_point_algorithm(X):
    # Krok 1: Inicjalizuj listę pustą dla punktów niezdominowanych
    P = []

    # Krok 2: Oblicz xmin, czyli minimum dla każdej współrzędnej
    xmin = [min(coord) for coord in zip(*X)]

    # Krok 4: Oblicz kwadratowe odległości między xmin a każdym punktem w X
    d = [sum((x_i - xmin_i) ** 2 for x_i, xmin_i in zip(x, xmin)) for x in X]

    # Krok 5: Posortuj odległości rosnąco i zachowaj ich indeksy
    sorted_indices = sorted(range(len(d)), key=lambda i: d[i])
    D = [d[i] for i in sorted_indices]
    J = sorted_indices

    # Krok 7: Inicjalizuj M jako liczba punktów w X
    M = len(X)
    m = 0

    # Krok 8: Wybierz niezdominowane punkty
    while m < M:
        current_index = J[m]
        current_point = X[current_index]

        # Usuń wszystkie punkty z X, które są zdominowane przez X[J(m)]
        X = [x for i, x in enumerate(X) if
             not all(x_i <= cp_i for x_i, cp_i in zip(x, current_point)) or i == current_index]

        # Zaktualizuj M
        M = len(X)

        # Dodaj X[J(m)] do listy punktów niezdominowanych P
        P.append(current_point)

        # Przejdź do kolejnego punktu
        m += 1

    return P


# Przykład użycia
X = [[2, 3], [5, 4], [3, 1], [2, 2]]
P = ideal_point_algorithm(X)
print("Punkty niezdominowane:", P)