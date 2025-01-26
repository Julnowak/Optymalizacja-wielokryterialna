import random


class PathFinding:
    def __init__(self):
        self.directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),
            (1, 1), (-1, -1), (-1, 1), (1, -1)
        ]

    def crossover(self, parent1, parent2):
        # Wybór losowego miejsca krzyżowania
        crossover_point = random.randint(1, min(len(parent1), len(parent2)))-1

        # Utworzenie nowego dziecka
        child = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        # print(child)
        # print(child2)

        new_child = extend_path(child)
        new_child_2 = extend_path(child2)

        return new_child, new_child_2


def extend_path(child):
    extended_path = [child[0]]  # Zaczynamy od pierwszego punktu

    for i in range(1, len(child)):
        current_point = extended_path[-1]
        next_point = child[i]

        # Obliczamy różnice w współrzędnych
        delta_x = next_point[0] - current_point[0]
        delta_y = (next_point[1] - current_point[1])

        # Obliczamy liczbę kroków w poziomie i pionie
        steps = max(abs(delta_x), abs(delta_y))

        # Generujemy punkty pomiędzy
        while delta_x != 0 or delta_y != 0:
            if delta_x > 0 and delta_y > 0:
                new_x = current_point[0] + 1
                new_y = current_point[1] + 1
                delta_x -= 1
                delta_y -= 1
            if delta_x < 0 and delta_y < 0:
                new_x = current_point[0] - 1
                new_y = current_point[1] - 1
                delta_x += 1
                delta_y += 1
            elif delta_y < 0:
                new_x = current_point[0]
                new_y = current_point[1] - 1
                delta_y += 1
            elif delta_x < 0:
                new_x = current_point[0] - 1
                new_y = current_point[1]
                delta_x += 1
            elif delta_y > 0:
                new_x = current_point[0]
                new_y = current_point[1] + 1
                delta_y -= 1
            elif delta_x > 0:
                new_x = current_point[0] + 1
                new_y = current_point[1]
                delta_x -= 1
            else:
                break

            extended_path.append((new_x, new_y))
            current_point = extended_path[-1]

        if next_point not in extended_path:
            extended_path.append(next_point)
    return extended_path



# # Tworzymy instancję klasy
pathfinding = PathFinding()
#
# # Definiujemy dwóch rodziców
# parent1 = [(5, 10), (6, 11), (7, 11), (8, 11), (9, 11), (10, 12), (11, 13), (12, 14), (13, 14), (14, 14), (15, 15), (15, 16), (15, 17), (16, 18), (17, 18), (17, 19), (17, 20), (17, 21), (17, 22), (17, 23), (17, 24), (18, 24), (19, 25), (19, 26), (19, 27), (19, 28), (19, 29), (19, 30), (19, 31), (19, 32), (19, 33), (20, 33), (21, 34), (22, 35), (23, 35), (24, 35), (25, 35), (26, 35), (27, 35), (28, 35), (29, 35), (30, 35), (31, 35), (31, 36), (31, 37), (31, 38), (31, 39), (31, 40), (31, 41), (31, 42), (31, 43), (31, 44), (31, 45), (31, 46), (31, 47), (31, 48), (32, 49), (33, 50), (34, 50), (35, 50), (36, 50), (37, 50), (38, 50), (39, 50), (40, 50), (41, 50), (42, 50), (43, 50), (44, 50), (45, 50), (46, 50), (47, 50), (48, 50)]
# parent2 = [(2, 4), (3, 5), (4, 6), (5, 6)]
#
# # Wywołujemy crossover
# child = pathfinding.crossover(parent1, parent2)
#
# # Drukujemy wynik
# print("Dziecko:", child)
#
# # Można też dodać proste sprawdzenie, czy długość dziecka jest odpowiednia
# print("Długość dziecka:", len(child))