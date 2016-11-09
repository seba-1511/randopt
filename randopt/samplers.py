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

class Lognormal(Sampler):

    def __init__(self, mean=0.0, std=1.0, dtype='float'):
        super(Lognormal, self).__init__()
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
    def __init__(self, lam=1.0, k=1.0, dtype='float'):
        super(Poisson, self).__init__()
        self.lam = lam
        self.k = k
        self.dtype = dtype

    def sample(self):
        res = (self.lam**self.k)*math.exp(-self.lam)/math.factorial(self.k)
        if 'fl' in self.dtype:
            return res
        return int(res)
