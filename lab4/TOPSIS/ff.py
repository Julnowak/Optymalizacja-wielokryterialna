import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def fuzzy_topsis(daneA, daneK, wektorWag):
    """
    Fuzzy TOPSIS dla danych w postaci liczb rozmytych trójkątnych.
    """
    # Określenie wielkości problemu
    liczbaAlternatyw, kolumny = daneA.shape
    iloscKryteriow = kolumny - 2  # Odejmujemy kolumny ID i nazwy alternatyw

    # Skalowanie danych (normalizacja rozmyta)
    macierz_skalowana = np.zeros((liczbaAlternatyw, iloscKryteriow, 3))  # Liczby rozmyte jako [dolna, środkowa, górna]
    for j in range(iloscKryteriow):
        dolne = np.array([daneA[i, 2 + j][0] for i in range(liczbaAlternatyw)])
        srodkowe = np.array([daneA[i, 2 + j][1] for i in range(liczbaAlternatyw)])
        gorne = np.array([daneA[i, 2 + j][2] for i in range(liczbaAlternatyw)])
        minVal = np.min(dolne)  # Dolne wartości
        maxVal = np.max(gorne)  # Górne wartości
        for i in range(liczbaAlternatyw):
            macierz_skalowana[i, j, 0] = (daneA[i, 2 + j][0] - minVal) / (maxVal - minVal)
            macierz_skalowana[i, j, 1] = (daneA[i, 2 + j][1] - minVal) / (maxVal - minVal)
            macierz_skalowana[i, j, 2] = (daneA[i, 2 + j][2] - minVal) / (maxVal - minVal)

    # Ważenie
    for j in range(iloscKryteriow):
        macierz_skalowana[:, j, :] *= wektorWag[j]

    # Wyznaczenie wektorów idealnych i antyidealnych
    wektorIdealny = np.zeros((iloscKryteriow, 3))  # Idealna liczba rozmyta
    wektorAntyIdealny = np.zeros((iloscKryteriow, 3))  # Antyidealna liczba rozmyta
    for j in range(iloscKryteriow):
        wektorIdealny[j, 0] = np.max(macierz_skalowana[:, j, 0])  # Dolny
        wektorIdealny[j, 1] = np.max(macierz_skalowana[:, j, 1])  # Środkowy
        wektorIdealny[j, 2] = np.max(macierz_skalowana[:, j, 2])  # Górny

        wektorAntyIdealny[j, 0] = np.min(macierz_skalowana[:, j, 0])  # Dolny
        wektorAntyIdealny[j, 1] = np.min(macierz_skalowana[:, j, 1])  # Środkowy
        wektorAntyIdealny[j, 2] = np.min(macierz_skalowana[:, j, 2])  # Górny

    # Obliczenie odległości do wektorów idealnych i antyidealnych
    odleglosciIdealny = np.zeros((liczbaAlternatyw, 3))
    odleglosciAntyIdealny = np.zeros((liczbaAlternatyw, 3))
    for i in range(liczbaAlternatyw):
        for j in range(iloscKryteriow):
            odleglosciIdealny[i, :] += (macierz_skalowana[i, j, :] - wektorIdealny[j, :]) ** 2
            odleglosciAntyIdealny[i, :] += (macierz_skalowana[i, j, :] - wektorAntyIdealny[j, :]) ** 2

    odleglosciIdealny = np.sqrt(odleglosciIdealny)
    odleglosciAntyIdealny = np.sqrt(odleglosciAntyIdealny)

    # Obliczenie wskaźnika bliskości
    ranking = np.zeros((liczbaAlternatyw, 2))
    for i in range(liczbaAlternatyw):
        bliskosc = odleglosciAntyIdealny[i, 1] / (odleglosciIdealny[i, 1] + odleglosciAntyIdealny[i, 1])
        ranking[i, :] = [i + 1, bliskosc]  # Indeks i wskaźnik bliskości

    # Posortowanie rankingu
    ranking = ranking[np.argsort(ranking[:, 1])[::-1]]  # Sortowanie malejące wg bliskości

    # Wyświetlenie wyników
    print("Macierz decyzyjna:")
    print(daneA[:, 2:])
    print("Macierz skalowana:")
    print(macierz_skalowana)
    print("Wektor idealny:")
    print(wektorIdealny)
    print("Wektor antyidealny:")
    print(wektorAntyIdealny)
    print("Ranking alternatyw:")
    print(ranking)


    # Wyświetlenie wyników
    print("Macierz decyzyjna:")
    print(daneA[:, 2:])
    print("Macierz skalowana:")
    print(macierz_skalowana)
    print("Wektor idealny:")
    print(wektorIdealny)
    print("Wektor antyidealny:")
    print(wektorAntyIdealny)
    print("Ranking alternatyw:")
    print(ranking)

        # Rysowanie wykresów
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(
        [alt[1] for alt in daneA[:, 2]],  # Środkowa wartość z 3. kolumny
        [alt[1] for alt in daneA[:, 3]],  # Środkowa wartość z 4. kolumny
        [alt[1] for alt in daneA[:, 4]],  # Środkowa wartość z 5. kolumny
        label='Alternatywy', c='b', marker='+'
    )

    ax.scatter(wektorIdealny[:, 1], wektorIdealny[:, 1], wektorIdealny[:, 1], label='Idealny', c='g', marker='o')
    ax.scatter(wektorAntyIdealny[:, 1], wektorAntyIdealny[:, 1], wektorAntyIdealny[:, 1], label='Antyidealny', c='r',
               marker='x')
    ax.legend()
    plt.show()
    return ranking, macierz_skalowana, wektorIdealny, wektorAntyIdealny


if __name__ == '__main__':
    # ciągłe
    daneA = np.array([
        [1, 'A1', [0.1, 0.3, 0.5], [0.2, 0.4, 0.6], [0.3, 0.5, 0.7], [0.4, 0.6, 0.8]],
        [2, 'A2', [0.2, 0.4, 0.6], [0.1, 0.3, 0.5], [0.3, 0.5, 0.7], [0.2, 0.4, 0.6]],
        [3, 'A3', [0.3, 0.5, 0.7], [0.4, 0.6, 0.8], [0.1, 0.3, 0.5], [0.5, 0.7, 0.9]],
        [4, 'A4', [0.2, 0.4, 0.6], [0.3, 0.5, 0.7], [0.2, 0.4, 0.6], [0.3, 0.5, 0.7]],
    ], dtype=object)

    wektorWag = np.array([0.4, 0.3, 0.2, 0.1])
    ranking, _, _, _ = fuzzy_topsis(daneA, None, wektorWag)

    # dyskretne
    daneA = np.array([
        [1, 'A1', [0.1, 0.3, 0.5], [0.2, 0.4, 0.6], [0.3, 0.5, 0.7]],
        [2, 'A2', [0.2, 0.4, 0.6], [0.3, 0.5, 0.7], [0.1, 0.3, 0.5]],
        [3, 'A3', [0.3, 0.5, 0.7], [0.1, 0.3, 0.5], [0.2, 0.4, 0.6]],
    ], dtype=object)

    wektorWag = np.array([0.5, 0.3, 0.2])
    ranking, _, _, _ = fuzzy_topsis(daneA, None, wektorWag)

