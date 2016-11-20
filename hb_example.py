#!/usr/bin/env python

import randopt as ro

def loss(x):
    return x**2

def dloss(x):
    return 2.0*x

def run_exp():
    param = 10.0
    num_epochs = 10

    e = ro.HyperBand('hb_example', {
            'alpha': ro.Uniform(low=0.0, high=0.01)
        }, num_iter=num_epochs)
    e.sample_all_params()

    for epoch in range(num_epochs):
        param = param - e.alpha * dloss(param)
        if e.stop(loss(param)):
            return e
    e.add_result(loss(param))
    return e


if __name__ == '__main__':
    num_runs = 100

    for run in range(num_runs):
        e = run_exp()

    print 'optimal value: ', e.minimum()
