import numpy as np
from scipy.optimize import minimize
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# Definiujemy funkcje kryterialne F1 i F2
def F(u):
    x, y = u
    F1 = x**2 + y**2
    F2 = (x - 1)**2 + y**2
    return np.array([F1, F2])


# Definiujemy skalaryzację liniową S1
def scalarization_S1(u, lambdas):
    F_values = F(u)
    return np.dot(lambdas, F_values)


# Definiujemy skalaryzację przez odległość S3
def scalarization_S3(u, x_dom, lambdas, p):
    F_values = F(u)
    diff = lambdas * (F_values - x_dom)
    if p == np.inf:
        return np.max(np.abs(diff))
    else:
        return np.linalg.norm(diff, ord=p)


if __name__ == '__main__':
    # Definiujemy obszar dopuszczalny U: kwadrat [-1, 1] x [-1, 1]
    bounds = [(-1, 1), (-1, 1)]

    # Krok rho do zmiany parametrów skalaryzacji
    rho = 0.05
    lambda_values = np.arange(0, 1 + rho, rho)
    lambda_values = np.clip(lambda_values, 0, 1)  # Upewniamy się, że wartości są w przedziale [0,1]
    solutions_S1 = []
    solutions_S2 = []
    solutions_S3 = []

    # Skalaryzacja liniowa S1
    for lambda1 in lambda_values:
        lambda2 = 1 - lambda1
        if lambda1 == 0 and lambda2 == 0:
            continue
        lambdas = np.array([lambda1, lambda2])
        # Punkt startowy optymalizacji
        x0 = np.array([0, 0])
        res = minimize(scalarization_S1, x0, args=(lambdas,), bounds=bounds)
        if res.success:
            u_opt = res.x
            F_opt = F(u_opt)
            solutions_S1.append(F_opt)

    # Skalaryzacja przez odległość S3
    # Definiujemy punkt dominujący x_dom
    x_dom = np.array([3, 3])
    p = 2  # Norma Euklidesowa
    for lambda1 in lambda_values:
        lambda2 = 1 - lambda1
        if lambda1 == 0 and lambda2 == 0:
            continue
        lambdas = np.array([lambda1, lambda2])
        x0 = np.array([0, 0])
        res = minimize(scalarization_S3, x0, args=(x_dom, lambdas, p), bounds=bounds)
        if res.success:
            u_opt = res.x
            F_opt = F(u_opt)
            solutions_S3.append(F_opt)

    # Skalaryzacja za pomocą metody ograniczeń S2
    # Minimalizujemy F1(u) z ograniczeniem F2(u) ≤ a2
    a2_values = np.arange(0, 5 + rho, rho)
    for a2 in a2_values:
        # Definiujemy ograniczenie F2(u) ≤ a2
        def constraint(u):
            return a2 - F(u)[1]  # Ograniczenie nierównościowe: a2 - F2(u) ≥ 0

        cons = {'type': 'ineq', 'fun': constraint}
        x0 = np.array([0, 0])
        res = minimize(lambda u: F(u)[0], x0, bounds=bounds, constraints=cons)
        if res.success:
            u_opt = res.x
            F_opt = F(u_opt)
            solutions_S2.append(F_opt)

    # Dodatkowo, minimalizujemy F2(u) z ograniczeniem F1(u) ≤ a1
    a1_values = np.arange(0, 2 + rho, rho)
    for a1 in a1_values:
        # Definiujemy ograniczenie F1(u) ≤ a1
        def constraint(u):
            return a1 - F(u)[0]  # Ograniczenie nierównościowe: a1 - F1(u) ≥ 0

        cons = {'type': 'ineq', 'fun': constraint}
        x0 = np.array([0, 0])
        res = minimize(lambda u: F(u)[1], x0, bounds=bounds, constraints=cons)
        if res.success:
            u_opt = res.x
            F_opt = F(u_opt)
            solutions_S2.append(F_opt)

    # Konwersja list na tablice numpy i usunięcie duplikatów
    solutions_S1 = np.array(solutions_S1)
    solutions_S2 = np.array(solutions_S2)
    solutions_S3 = np.array(solutions_S3)

    # Usunięcie duplikatów w rozwiązaniach S2
    solutions_S2 = np.unique(solutions_S2, axis=0)

    # Wizualizacja wyników
    plt.figure(figsize=(8, 6))
    plt.plot(solutions_S1[:, 0], solutions_S1[:, 1], 'o-', label='S1 Skalaryzacja liniowa')
    plt.plot(solutions_S2[:, 0], solutions_S2[:, 1], 'x-', label='S2 Metoda ograniczeń')
    plt.plot(solutions_S3[:, 0], solutions_S3[:, 1], 's-', label='S3 Skalaryzacja przez odległość')
    plt.xlabel('F1(u)')
    plt.ylabel('F2(u)')
    plt.title('Aproksymacja zbioru FP(U)')
    plt.legend()
    plt.grid(True)
    plt.show()
