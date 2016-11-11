#!/usr/bin/env python

import random
import math

"""
Here we implement the sampling strategies.

TODO:
    * Add support for more sampling schemes. (Loguniform, Poisson, etc...)
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
        self.rng.getstate()

    def set_state(self, state):
        self.rng.setstate(state)


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

class Poisson(Sampler):
    '''
    lambda = event rate / average number of events per interval
    k = 0,1,2,3... (events in interval)

    '''
    def __init__(self, lam=1.0, max_k=4, dtype='float'):
        super(Poisson, self).__init__()
        self.lam = lam
        self.max_k = max_k
        self.dtype = dtype

    def sample(self):
        k = self.rng.randint(0.0, self.max_k)
        res = (self.lam**k)*math.exp(-self.lam)/math.factorial(k)
        if 'fl' in self.dtype:
            return res
        return int(res)


class BetaVariate(Sampler):

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

    def __init__(self, alpha, dtype='float'):
        super(ParetoVariate, self).__init__()
        self.alpha = alpha
        self.dtype = dtype

    def sample(self):
        res = self.rng.paretovariate(self.alpha)
        if 'fl' in self.dtype:
            return res
        return int(res)
