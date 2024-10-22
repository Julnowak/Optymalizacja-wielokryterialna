import numpy as np


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
        X = X[
            non_dominated_mask
        ]  # Zostają tylko punkty, które nie są zdominowane przez current_point

        # Dodajemy current_point do listy punktów niezdominowanych
        P.append(current_point.tolist())  # Konwersja na zwykłą listę

        # Aktualizacja listy J po usunięciu punktów zdominowanych
        J = J[non_dominated_mask]  # Zaktualizuj J, by odzwierciedlać nowe X
        D = D[non_dominated_mask]  # Zaktualizuj D po usunięciu zdominowanych

        # Aktualizacja M i m
        M = len(J)  # Nowa liczba punktów
        m += 1  # Przejdź do kolejnego punktu

    return P


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

    P = algorytm_oparty_o_punkt_idealny(X)
    print("Punkty niezdominowane (punkt idealny):", P)
