from typing import List, Tuple
import numpy as np
from math import sqrt
from numpy._typing import NDArray


def is_point_dominating_point(point1: List[float], point2: List[float], min_max: List[bool]) -> bool:
    """
    Sprawdza, czy punkt `point1` dominuje punkt `point2` w przestrzeni kryteriów.
    """
    return all(
        (x1 <= x2 if m else x1 >= x2)
        for x1, x2, m in zip(point1, point2, min_max)
    )


def distance(point1: List[float], point2: List[float]) -> float:
    """
    Oblicza odległość euklidesową między dwoma punktami w przestrzeni wielowymiarowej.
    """
    return sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))


def classify_alternatives(decision_points: NDArray[float], classes: NDArray[float]) -> List[int]:
    """
    Przypisuje alternatywy do zdefiniowanych klas na podstawie ich współrzędnych.
    """
    classifications = []
    for point in decision_points:
        distances = [distance(point, cls) for cls in classes]
        classifications.append(np.argmin(distances) + 1)
    return classifications


def rsm(
        reference_points: NDArray[float],
        decision_points: NDArray[float],
        min_max: List[bool],
        bounds: List[Tuple[float, float]] = None,
        num_samples: int = 0,
        classes: NDArray[float] = None
) -> Tuple[List[Tuple[List[float], float]], List[int]]:
    """
    Implementacja RSM obsługująca tryb ciągły i dyskretny oraz przypisanie do klas.
    """
    if bounds and num_samples > 0:
        # Generowanie próbek w przestrzeni ciągłej
        samples = [np.linspace(b[0], b[1], num_samples) for b in bounds]
        decision_points = np.array(np.meshgrid(*samples)).T.reshape(-1, len(bounds))

    # Podział punktów referencyjnych na dominowane i nie-dominowane
    lst_nzd, lst_zd = [], []
    for i, ref in enumerate(reference_points):
        dominated = any(
            is_point_dominating_point(other, ref, min_max) for j, other in enumerate(reference_points) if i != j)
        if dominated:
            lst_zd.append(ref)
        else:
            lst_nzd.append(ref)

    # Obliczanie odległości od punktów referencyjnych
    scores = []
    for point in decision_points:
        d_plus = min(distance(point, r_plus) for r_plus in lst_nzd)
        d_minus = min(distance(point, r_minus) for r_minus in lst_zd)
        scores.append((point.tolist(), d_minus - d_plus))

    # Sortowanie punktów według wyniku
    scores.sort(key=lambda x: x[1], reverse=True)

    # Klasyfikacja punktów
    classifications = classify_alternatives(decision_points, classes) if classes is not None else []

    return scores, classifications


# Przykład użycia
if __name__ == "__main__":
    # Punkty referencyjne (dyskretny przypadek)
    reference_points = np.array([
        [0.3, 7.6, 2.9],
        [0.7, 8.0, 7.0],
        [0.1, 6.5, 3.5],
    ])

    # Punkty decyzyjne
    decision_points = np.array([
        [0.4, 7.7, 3.0],
        [0.6, 8.1, 6.9],
        [0.2, 6.7, 3.3],
    ])

    # Definicja klas
    classes = np.array([
        [0.3, 7.6, 2.9],  # Klasa 1
        [0.7, 8.0, 7.0],  # Klasa 2
    ])

    # Przypadek dyskretny
    scores, classifications = rsm(reference_points, decision_points, [True, True, True], classes=classes)
    print("Dyskretny:")
    for point, score in scores:
        print(f"Point: {point}, Score: {score:.4f}")
    print("Classifications:", classifications)

    # Przypadek ciągły
    bounds = [(0.0, 1.0), (6.0, 9.0), (2.0, 8.0)]
    scores, classifications = rsm(reference_points, None, [True, True, True], bounds=bounds, num_samples=5,
                                  classes=classes)
    print("\nCiągły:")
    for point, score in scores[:5]:  # Wyświetl pierwsze 5 wyników
        print(f"Point: {point}, Score: {score:.4f}")
    print("Classifications:", classifications)
