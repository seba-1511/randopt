#!/usr/bin/env python

import random
import math

"""
Here we implement the sampling strategies.

TODO:
    * Unit tests
"""


class Sampler(object):

    def __init__(self, *args, **kwargs):
        self.rng = random.Random()

    def sample(self):
        raise('Sampler should not be instantiated')

    def seed(self, seed_val):
        self.rng.seed(seed_val)

    def get_state(self):
        return self.rng.getstate()

    def set_state(self, state):
        self.rng.setstate(state)


class Constant(Sampler):

    def __init__(self, value):
        super(Constant, self).__init__()
        self.value = value

    def sample(self):
        return self.value


class Choice(Sampler):

    def __init__(self, items, sampler=None):
        """sampler is any of the available samplers,
           used to sample element's index from the list."""
        if sampler is None:
            sampler = Uniform()
        self.sampler = sampler
        self.items = items
        self.rng = self.sampler.rng

    def sample(self):
        i = self.sampler.sample() * len(self.items)
        i = int(math.floor(i))
        return self.items[i]


class Truncated(Sampler):
    """
    Given a sampler, truncates the distribution between low and high.
    If None, not truncated.
    """

    def __init__(self, sampler=None, low=None, high=None):
        if sampler is None:
            sampler = Uniform()
        self.sampler = sampler
        self.min = low
        self.max = high
        self.rng = self.sampler.rng

    def sample(self):
        val = self.sampler.sample()
        if self.min is not None and val < self.min:
            val = self.min
        if self.max is not None and val > self.max:
            val = self.max
        return val


class Uniform(Sampler):
    '''
    Description:
        Generates a randomly sampled value from low to high with equal probability.

    Parameters:
        low - minimum value
        high - maximum value
        dtype - data type (float by default)

    Return type:
        n/a

    Example:
        randopt.Uniform(low=-1.0, high=1.0, dtype='float')
    '''
    def __init__(self, low=0.0, high=1.0, dtype='float'):
        super(Uniform, self).__init__()
        self.low = low
        self.high = high
        self.dtype = dtype

    def sample(self):
        res = self.rng.uniform(self.low, self.high)
        if 'fl' in self.dtype:
            return res
        return int(res)


class Gaussian(Sampler):
    '''
    Description:
        Generates a randomly sampled value with specified mean and std based on a Gaussian distribution

    Parameters:
        mean - mean of Gaussian
        std - standard deviation of Gaussian
        dtype - data type (float by default)

    Return type:
        n/a

    Example:
        randopt.Gaussian(mean=0.0, std=1.0, dtype='float')
    '''
    def __init__(self, mean=0.0, std=1.0, dtype='float'):
        super(Gaussian, self).__init__()
        self.mean = mean
        self.std = std
        self.dtype = dtype

    def sample(self):
        res = self.rng.gauss(self.mean, self.std)
        if 'fl' in self.dtype:
            return res
        return int(res)


class Normal(Gaussian):
    pass


class LognormVariate(Sampler):
    '''
    Description:
        Generates a randomly sampled value with specified mean and std based on a Log normal distribution

    Parameters:
        mean - mean of Lognormal
        std - standard deviation of Lognormal
        dtype - data type (float by default)

    Return type:
        n/a

    Example:
        randopt.LognormVariate(mean=0.0, std=1.0, dtype='float')
    '''
    def __init__(self, mean=0.0, std=1.0, dtype='float'):
        super(LognormVariate, self).__init__()
        self.mean = mean
        self.std = std
        self.dtype = dtype

    def sample(self):
        res = self.rng.lognormvariate(self.mean, self.std)
        if 'fl' in self.dtype:
            return res
        return int(res)


class BetaVariate(Sampler):
    '''
    Description:
        Generates a randomly sampled value with specified mean and std based on a Beta distribution

    Parameters:
        alpha - alpha of beta distribution
        beta - beta of beta distribution
        dtype - data type (float by default)

    Return type:
        n/a

    Example:
        randopt.BetaVariate(alpha=1,beta=1,dtype='float')
    '''
    def __init__(self, alpha, beta, dtype='float'):
        super(BetaVariate, self).__init__()
        self.alpha = alpha
        self.beta = beta
        self.dtype = dtype

    def sample(self):
        res = self.rng.betavariate(self.alpha, self.beta)
        if 'fl' in self.dtype:
            return res
        return int(res)


class ExpoVariate(Sampler):
    '''
    Description:
        Generates a randomly sampled value with lambda based on an exponential distribution

    Parameters:
        lam - lambda of exponential distribution (one divided by desired mean)
        dtype - data type (float by default)

    Return type:
        n/a

    Example:
        randopt.ExpoVariate(lam=1, dtype='float')
    '''
    def __init__(self, lam, dtype='float'):
        super(ExpoVariate, self).__init__()
        self.lam = lam
        self.dtype = dtype

    def sample(self):
        res = self.rng.expovariate(self.lam)
        if 'fl' in self.dtype:
            return res
        return int(res)


class WeibullVariate(Sampler):
    '''
    Description:
        Generates a randomly sampled value with specified mean and std based on a Weibull distribution

    Parameters:
        alpha - alpha of Weibull distribution (scale parameter)
        beta - beta of Weibull distribution (shape parameter)
        dtype - data type (float by default)

    Return type:
        n/a

    Example:
        randopt.WeibullVariate(alpha=1,beta=1,dtype='float')
    '''
    def __init__(self, alpha, beta, dtype='float'):
        super(WeibullVariate, self).__init__()
        self.alpha = alpha
        self.beta = beta
        self.dtype = dtype

    def sample(self):
        res = self.rng.weibullvariate(self.alpha, self.beta)
        if 'fl' in self.dtype:
            return res
        return int(res)


class ParetoVariate(Sampler):
    '''
    Description:
        Generates a randomly sampled value with alpha based on the Pareto distribution

    Parameters:
        alpha - alpha of Pareto distribution (shape parameter)
        dtype - data type (float by default)

    Return type:
        n/a

    Example:
        randopt.ParetoVariate(alpha=1,dtype='float')
    '''
    def __init__(self, alpha, dtype='float'):
        super(ParetoVariate, self).__init__()
        self.alpha = alpha
        self.dtype = dtype

    def sample(self):
        res = self.rng.paretovariate(self.alpha)
        if 'fl' in self.dtype:
            return res
        return int(res)
