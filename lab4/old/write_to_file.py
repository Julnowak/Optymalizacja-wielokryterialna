#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Tuple
import pandas as pd


def write_results_to_file(points: List[List[float]], nondominated_points: List[List[float]], parameters: List[Tuple[str, str]]):
    data = {}

    print(points)
    print(nondominated_points)
    print(parameters)

    for par in parameters:
        data[par[0] + ' - ' + par[1]] = []

    data['dominated'] = []

    for point in points:
        for i, coordinate in enumerate(point):
            key = parameters[i][0] + ' - ' + parameters[i][1]
            data[key].append(coordinate)

        for p in nondominated_points:
            equal = True

            for i in range(len(point)):
                if p[i] != point[i]:
                    equal = False
                    break

            if equal:
                data['dominated'].append('no')
                break

        else:
            data['dominated'].append('yes')

    df = pd.DataFrame(data)
    df.to_excel('results.xlsx', index=False)

if __name__ == '__main__':
    points = [[5, 5], [3, 6], [4, 4], [5, 3], [3, 3], [1, 8], [3, 4], [4, 5], [3, 10], [6, 6], [4, 1], [3, 5]]
    n = [[3, 3], [1, 8], [4, 1]]
    par = [('Kryterium 1', 'min'), ('Kryterium 2', 'min')]
    write_results_to_file(points, n, par)