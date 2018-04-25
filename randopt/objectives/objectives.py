#!/usr/bin/env python3

"""
This module defines scalarization functions for multi-objective
optimization problems.
"""

try:  # Try native statistics module
    from statistics import mean, median, pvariance, pstdev
except ImportError:
    from randopt.statistics import mean, median, pvariance, pstdev

variance = pvariance
std = pstdev


def normalize(data):
    """
    Normalizes and iterable such that its elements sum to 1.

    Parameters:

    * data - (iterable) data to be normalized

    Example:

        data = [1, 2, 3]
        data = normalize(data)
        assert sum(data) == 1
    """
    total = sum(data)
    return [d / float(total) for d in data]


def mean_variance(data, w_mean=0.5, w_var=0.5):
    """
    Minimizes both mean and variance of a given multi-objective result.

    Returns w_mean * mean + w_var * var

    Parameters:

    * data - (iterable) multi-objective results
    * w_mean - (float) weight of the mean
    * w_var - (float) weight of the variance

    Example:

        exp = ro.Experiment('example')
        result = mean_variance([0.9, 0.5, 0.3, 0.2, 0.1], 0.1, 0.9)
        exp.add_result(results)
    """
    mu = mean(data)
    var = pvariance(data, mu=mu)
    return w_mean * mu + w_var * var


def mean_std(data, w_mean=0.5, w_std=0.5):
    """
    Minimizes both mean and standard deviation of a
    given multi-objective result.

    Returns w_mean * mean + w_std * std

    Parameters:

    * data - (iterable) multi-objective results
    * w_mean - (float) weight of the mean
    * w_std - (float) weight of the std

    Example:

        exp = ro.Experiment('example')
        result = mean_std([0.9, 0.5, 0.3, 0.2, 0.1], 0.3, 0.7)
        exp.add_result(results)
    """
    mu = mean(data)
    sigma = pstdev(data, mu=mu)
    return w_mean * mu + w_std * sigma


def median_variance(data, w_median=0.5, w_var=0.5):
    """
    Minimizes both median and variance of a given multi-objective result.

    Returns w_median * median + w_var * var

    Parameters:

    * data - (iterable) multi-objective results
    * w_median - (float) weight of the median
    * w_var - (float) weight of the variance

    Example:

        exp = ro.Experiment('example')
        result = median_variance([0.9, 0.5, 0.3, 0.2, 0.1], 0.1, 0.9)
        exp.add_result(results)
    """
    med = median(data)
    var = pvariance(data)
    return w_median * med + w_var * var


def median_std(data, w_median=0.5, w_std=0.5):
    """
    Minimizes both median and standard deviation of a
    given multi-objective result.

    Returns w_median * median + w_std * std

    Parameters:

    * data - (iterable) multi-objective results
    * w_mean - (float) weight of the median
    * w_std - (float) weight of the std

    Example:

        exp = ro.Experiment('example')
        result = median_std([0.9, 0.5, 0.3, 0.2, 0.1], 0.1, 0.9)
        exp.add_result(results)
    """
    med = median(data)
    sigma = pstdev(data)
    return w_median * med + w_std * sigma
