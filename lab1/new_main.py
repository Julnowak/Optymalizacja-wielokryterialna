# def all():
#     sorted = False
#     pass


def bez_filtracji(X):
    P = []  # Lista punktów niezdominowanych
    n = len(X)

    # Pętla po każdym punkcie X
    for i in range(n):
        Y = X[i]
        fl = 0  # Flaga do kontrolowania, czy Y zostało usunięte

        # Pętla po pozostałych punktach X
        for j in range(i + 1, n):
            if Y <= X[j]:
                # Jeśli Y jest mniejsze lub równe X[j], to X[j] jest usuwane
                continue  # Kontynuuj bez usuwania Y, tylko ignorujemy X[j]
            elif X[j] <= Y:
                # Jeśli X[j] jest mniejsze lub równe Y, to usuwamy Y
                fl = 1
                Y = X[j]  # Zmieniamy Y na X[j]
                break  # Przerywamy pętlę, ponieważ Y zostało zmienione
            else:
                print("Niezdominowany")

        if fl == 0:
            # Jeśli Y nie zostało zmienione, dodajemy je do listy P
            P.append(Y)
        # Jeśli Y zostało zmienione, nie dodajemy go do listy P

    return P




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

    P = bez_filtracji(X)
    print("Punkty niezdominowane (bez filtracji):", P)
