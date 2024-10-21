import numpy as np


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
        mask = np.any(
            X > Y, axis=1
        )  # Zachowujemy punkty, które nie są zdominowane przez Y
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
