import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.optimize import linprog


class UTABIS:

    def __init__(self, scales, monotonic, delta, categories):
        self.scales = scales
        self.monotonic = monotonic
        self.delta = delta
        self.categories = categories

    def _normalize(self, data):
        """
        Normalizuje dane do zakresu [0, 1].
        """
        min_vals = data.min(axis=0)
        max_vals = data.max(axis=0)
        return (data - min_vals) / (max_vals - min_vals), min_vals, max_vals

    def _create_constraints(self, norm_reference):
        """
        Tworzy ograniczenia dla problemu optymalizacji.
        """
        n_ref, n_crit = norm_reference.shape
        total_variables = sum(self.scales)

        A = []
        b = []
        Aeq = []
        beq = []

        # Ograniczenia monotoniczności
        offset = 0
        for crit_idx, (scale, is_increasing) in enumerate(zip(self.scales, self.monotonic)):
            for j in range(scale - 1):
                a = np.zeros(total_variables)
                if is_increasing:
                    a[offset + j] = -1
                    a[offset + j + 1] = 1
                else:
                    a[offset + j] = 1
                    a[offset + j + 1] = -1
                A.append(a)
                b.append(0)
            offset += scale

        # Ograniczenia kategorii
        for i in range(n_ref - 1):
            for j in range(i + 1, n_ref):
                if self.categories[i] < self.categories[j]:
                    a = np.zeros(total_variables)
                    offset = 0
                    for crit_idx, scale in enumerate(self.scales):
                        a[offset:offset + scale] = norm_reference[i, crit_idx] - norm_reference[j, crit_idx]
                        offset += scale
                    A.append(a)
                    b.append(-self.delta)

        # Suma wag = 1
        a_eq = np.zeros(total_variables)
        offset = 0
        for scale in self.scales:
            a_eq[offset + scale - 1] = 1
            offset += scale
        Aeq.append(a_eq)
        beq.append(1)

        bounds = [(0, None)] * total_variables
        c = np.zeros(total_variables)
        return np.array(A), np.array(b), np.array(Aeq), np.array(beq), bounds, c

    def fit(self, data, reference):
        """
        Dopasowuje model na podstawie danych referencyjnych.
        """
        # Normalizacja danych
        norm_data, self.min_vals, self.max_vals = self._normalize(data)
        norm_reference, _, _ = self._normalize(reference)

        # Tworzenie ograniczeń
        A, b, Aeq, beq, bounds, c = self._create_constraints(norm_reference)

        # Rozwiązanie problemu optymalizacji
        res = linprog(c, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=bounds, method='highs')
        if not res.success:
            raise ValueError("Problem optymalizacji nie został rozwiązany.")

        # Wyznaczenie wag
        self.weights = res.x

        # Obliczenie funkcji użyteczności
        utilities = []
        for row in norm_data:
            utility = 0
            offset = 0
            for crit_idx, scale in enumerate(self.scales):
                g = np.linspace(0, 1, scale)
                u_values = np.zeros(scale)
                u_values[0] = 0
                for k in range(1, scale):
                    u_values[k] = u_values[k - 1] + self.weights[offset + k - 1]
                offset += scale
                utility += np.interp(row[crit_idx], g, u_values)
            utilities.append(utility)

        self.utilities = np.array(utilities)
        return self.utilities

    def visualize(self, data, utilities, criterion1=0, criterion2=1, criterion3=2):
        """
        Wizualizuje punkty danych w przestrzeni trzech wybranych kryteriów.
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')  # Dodanie wykresu 3D

        # Wykres punktów
        sc = ax.scatter(
            data[:, criterion1],
            data[:, criterion2],
            data[:, criterion3],
            c=utilities,
            cmap='viridis',
            edgecolor='k',
            s=100
        )

        # Dodanie skali kolorów
        plt.colorbar(sc, label="Użyteczność")

        # Opis osi
        ax.set_xlabel(f"Kryterium {criterion1 + 1}")
        ax.set_ylabel(f"Kryterium {criterion2 + 1}")
        ax.set_zlabel(f"Kryterium {criterion3 + 1}")
        ax.set_title("Wizualizacja punktów danych w przestrzeni trzech kryteriów")

        plt.show()
# Dane testowe
data = np.array([
    [3, 10, 1],
    [4, 20, 2],
    [2, 20, 0],
    [6, 40, 0],
    [2, 20, 3],
    [1, 10, 1],
])

reference = np.array([
    [3, 10, 1],
    [4, 20, 2],
    [2, 20, 0],
    [6, 40, 0],
    [2, 20, 3],
    [1, 10, 1],
])

categories = [1, 2, 2, 4, 5, 1, 1]

# Parametry
scales = [2, 3, 3]
monotonic = [True, True, True]  # True: rosnące, False: malejące
delta = 0.05

# UTA BIS
model = UTABIS(scales, monotonic, delta, categories)
utilities = model.fit(data, reference)

# Wizualizacja
model.visualize(data, utilities)
