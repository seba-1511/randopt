#!/usr/bin/env python3

import randopt as ro
from random import random

def loss(x, y):
    return [(x**2 + y**2 + random()) / i for i in range(1, 51)]

if __name__ == '__main__':
    exp = ro.Experiment('quadratic', params={
        'x': ro.Gaussian(),
        'y': ro.Uniform(-0.5, 0.5)
    })

    for _ in range(20):
        exp.sample_all_params()
        conv = loss(exp.x, exp.y)
        exp.add_result(conv[-1], data={
            'convergence': conv
        })
