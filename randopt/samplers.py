#!/usr/bin/env python

import random

"""
Here we implement the sampling strategies.

TODO: 
    * Add support for sampling over lists of values. 
      Eg: ro.Uniform([1, 2, 4, 8]) uniformly samples over the list.
    * Add support for more sampling schemes. (Loguniform, Poisson, etc...)
"""

class Sampler(object):

    def __init__(self):
        self.rng = random.Random()

    def sample(self):
        raise('Class not instantiable')

    def seed(self, seed_val):
        self.rng.seed(seed_val)


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


class Normal(Uniform):
    pass


class Gaussian(Sampler):

    def __init__(self, mean=0.0, std=1.0, dtype='float'):
        pass

