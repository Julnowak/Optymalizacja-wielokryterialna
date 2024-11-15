import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Definicja parametrów
p1, p2 = 10, 10  # Parametry funkcji celu

# Funkcje celu
def objectives(u):
    x, y = u
    f1 = x**2 + y**2
    f2 = (x - p1)**2 + (y + p2)**2
    return np.array([f1, f2])

# Funkcja skalaryzacji przez sumę ważoną
def weighted_sum(u, lambdas):
    return np.dot(lambdas, objectives(u))

# Ograniczenie (obszar poszukiwań U)
def constraint(u):
    x, y = u
    return 1 - ((x - 3)**2 + (y - 3)**2)

# Optymalizacja dla danych lambdas
def scalarization_optimization(lambdas):
    cons = {'type': 'ineq', 'fun': constraint}
    bounds = [(2, 4), (2, 4)]  # Zakresy zmiennych (ponieważ okrąg jest w centrum (3,3) z promieniem 1)
    result = minimize(lambda u: weighted_sum(u, lambdas), x0=[3, 3], bounds=bounds, constraints=cons)
    if result.success:
        return objectives(result.x)
    else:
        return None

# Generowanie wartości lambda na jednostkowym sympleksie
angles = np.linspace(0, np.pi / 2, 20)
lambda_values = [(np.cos(angle), np.sin(angle)) for angle in angles]

pareto_points = []

for lambdas in lambda_values:
    F_values = scalarization_optimization(lambdas)
    if F_values is not None:
        pareto_points.append(F_values)

pareto_points = np.array(pareto_points)

# Wizualizacja
plt.figure(figsize=(10, 6))
plt.plot(pareto_points[:, 0], pareto_points[:, 1], marker='o', linestyle='-', label='Front Pareto')
plt.title('Skalaryzacja przez funkcję liniową')
plt.xlabel('F1')
plt.ylabel('F2')
plt.legend()
plt.grid(True)
plt.show()
