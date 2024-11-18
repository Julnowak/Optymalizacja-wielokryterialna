#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def plot_results(all_points, rank_points):
    if not all_points:
        return None

    fig = plt.figure()

    if len(all_points[0]) == 3:
        x_all, y_all, z_all = zip(*all_points)
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x_all, y_all, z_all, marker ="*", label="Zbiór punktów")

        if len(rank_points) >= 1:
            rank1 = rank_points[0]
            ax.scatter([rank1[0]], [rank1[1]], [rank1[2]], c="red", marker ="o", label="Ranking 1")

        if len(rank_points) >= 2:
            rank2 = rank_points[1]
            ax.scatter([rank2[0]], [rank2[1]], [rank2[2]], c="green", marker ="o", label="Ranking 2")

        if len(rank_points) >= 3:
            rank3 = rank_points[2]
            ax.scatter([rank3[0]], [rank3[1]], [rank3[2]], c="black", marker ="o", label="Ranking 3")

        ax.set_zlabel('Kryterium 3')

    elif len(all_points[0]) == 2:
        x_all, y_all = zip(*all_points)
        ax = fig.add_subplot(111)
        ax.scatter(x_all, y_all, c="blue", marker ="*", label="Zbiór punktów")

        if len(rank_points) >= 1:
            rank1 = rank_points[0]
            ax.scatter([rank1[0]], [rank1[1]], c="red", marker ="o", label="Ranking 1")

        if len(rank_points) >= 2:
            rank2 = rank_points[1]
            ax.scatter([rank2[0]], [rank2[1]], c="green", marker ="o", label="Ranking 2")

        if len(rank_points) >= 3:
            rank3 = rank_points[2]
            ax.scatter([rank3[0]], [rank3[1]], c="black", marker ="o", label="Ranking 3")

    else:
        return None

    ax.set_xlabel('Kryterium 1')
    ax.set_ylabel('Kryterium 2')
    plt.legend()
    plt.title('Alternatywy wraz z rankingiem')
    plt.show()