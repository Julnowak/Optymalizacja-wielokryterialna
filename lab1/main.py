# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np

def all():
    sorted = False
    pass


def bez_filtracji(X):
    X = np.array(X)
    P = []

    i = 0
    while i < X.shape[0]:
        Y = X[i, :]
        fl = 0
        j = i + 1
        while j < X.shape[0]:
            print(f'--- Iteracja {i+1},{j} ---')
            print(f"Element aktywny: {Y}")
            print(X[j, :])
            print(X)
            if np.all(Y <= X[j, :]):
                # Y dominuje X(j), usuwamy X(j)

                X = np.delete(X, j, axis=0)


            else:
                if np.all(Y >= X[j, :]):
                    # X(j) dominuje Y, aktualizujemy Y
                    print(f"Usunięto element: {Y}")
                    Y, X = X[j, :], np.delete(X, np.where(X==Y)[0][0], axis=0)

                    fl = 1  # Zmiana flaga na 1
                else:
                    print(f"Element nieporównywalny: {X[j, :]}")
                    # X = np.delete(X, np.where(X == X[j, :])[0][0], axis=0)
                    print(X)
                j += 1

        # Dodajemy Y do listy punktów niezdominowanych
        P += [Y]

        if fl == 0:
            # Jeśli flaga równa 0, usuwamy Y z X
            X = np.delete(X, np.where(X==Y)[0][0], axis=0)
        else:
            i += 1

    return np.unique(P, axis=0).tolist()  # Zwróć unikalne punkty jako listę


def algorytm_z_filtracja(X):
    # Wejście: X - macierz Nx2 z punktami [x, y]
    # Wyjście: P - lista punktów niezdominowanych

    X = np.array(X)  # Przekształcenie listy na macierz numpy
    P = []  # Lista punktów niezdominowanych
    n = X.shape[0]  # Liczba punktów

    i = 0
    while i < n:
        Y = X[i, :]  # Pobranie aktualnego punktu Y
        j = i + 1

        while j < n:
            if np.all(Y <= X[j, :]):
                # Y dominuje X(j), usuwamy X(j)
                X = np.delete(X, j, axis=0)
                n = X.shape[0]  # Zaktualizowana liczba punktów
            elif np.all(X[j, :] <= Y):
                # X(j) dominuje Y, aktualizujemy Y
                Y = X[j, :]
                X[i, :] = X[j, :]
                j += 1
            else:
                j += 1

        # Dodajemy Y do listy punktów niezdominowanych
        P.append(list(Y))

        # Filtracja - usunięcie punktów zdominowanych przez Y
        mask = np.any(X > Y, axis=1)  # Zachowujemy punkty, które nie są zdominowane przez Y
        X = X[mask, :]
        n = X.shape[0]

        if n == 1:
            # Jeśli pozostał tylko jeden punkt, dodaj go do P i zakończ
            P.append(list(X[0]))
            break

        # Usunięcie Y z listy X
        if i < n:
            X = np.delete(X, i, axis=0)
            n = X.shape[0]

    return np.unique(P, axis=0).tolist()  # Zwróć unikalne punkty jako listę


def algorytm_oparty_o_punkt_idealny(X):
    # Wejście: X - macierz Nxk z punktami [x1, x2, ..., xk]
    # Wyjście: P - lista punktów niezdominowanych (zwykła lista int)

    X = np.array(X)  # Przekształcenie listy na macierz numpy
    k = X.shape[1]  # Liczba współrzędnych w każdym punkcie
    n = X.shape[0]  # Liczba punktów

    # 1. Inicjalizacja pustej listy P
    P = []

    # 2-3. Obliczanie xmin (minimalne wartości dla każdej współrzędnej)
    xmin = np.min(X, axis=0)

    # 4. Obliczanie kwadratów odległości d(j) dla każdego punktu X(j) od xmin
    d = np.array([np.sum((xmin - X[j, :]) ** 2) for j in range(n)])

    # 5. Posortowanie d(j) rosnąco
    J = np.argsort(d)  # Indeksy punktów X posortowane według odległości
    D = d[J]  # Posortowane odległości

    # 7. Zmienna M
    M = len(J)  # Liczba punktów po sortowaniu
    m = 0  # Indeks startowy w posortowanych punktach

    # 8. Pętla while do przeglądania posortowanych punktów
    while m < M:
        # Punkt X(J[m]) o najmniejszej odległości
        current_point = X[J[m], :]

        # Usunięcie z X wszystkich punktów zdominowanych przez current_point
        non_dominated_mask = np.any(X > current_point, axis=1)
        X = X[non_dominated_mask]  # Zostają tylko punkty, które nie są zdominowane przez current_point

        # Dodajemy current_point do listy punktów niezdominowanych
        P.append(current_point.tolist())  # Konwersja na zwykłą listę

        # Aktualizacja listy J po usunięciu punktów zdominowanych
        J = J[non_dominated_mask]  # Zaktualizuj J, by odzwierciedlać nowe X
        D = D[non_dominated_mask]  # Zaktualizuj D po usunięciu zdominowanych

        # Aktualizacja M i m
        M = len(J)  # Nowa liczba punktów
        m += 1  # Przejdź do kolejnego punktu

    return P


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    X = [[5, 5], [3, 6], [4, 4], [5, 3], [3, 3], [1, 8], [3, 4], [4, 5], [3, 10], [6, 6], [4, 1], [3, 5]]

    P = bez_filtracji(X)
    print("Punkty niezdominowane (bez filtracji):", P)

    P = algorytm_z_filtracja(X)
    print("Punkty niezdominowane (z filtracją):", P)

    P = algorytm_oparty_o_punkt_idealny(X)
    print("Punkty niezdominowane (punkt idealny):", P)
