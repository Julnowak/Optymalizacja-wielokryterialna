#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np


def generate_points_gaussian(mean, std, number_of_points, number_of_parameters):
    return np.random.normal(mean, std, (number_of_points, number_of_parameters))


def generate_points_exponential(scale, number_of_points, number_of_parameters):
    return np.random.exponential(scale, (number_of_points, number_of_parameters))


def generate_points_beta(a, b, number_of_points, number_of_parameters):
    return np.random.beta(a, b, (number_of_points, number_of_parameters))


def generate_points_gamma(shape, scale, number_of_points, number_of_parameters):
    return np.random.gamma(shape, scale, (number_of_points, number_of_parameters))

def generate_points_uniform(low, high, number_of_points, number_of_parameters):
    return np.random.uniform(low, high, (number_of_points, number_of_parameters))

# def write_to_file(all_points, non_dominated_points, parameters_names, parameter_function):


if __name__ == '__main__':
    print(generate_points_gamma(1, 4, 5, 2))