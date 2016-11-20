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

    import os
    import json
    max_lr = 0.0
    for fname in os.listdir(e.hyperband_path):
        base, ext = os.path.splitext(fname)
        if 'json' in ext:
            fname = os.path.join(e.hyperband_path, fname)
            with open(fname, 'r') as f:
                res = json.load(f)
                if res['alpha'] > max_lr:
                    max_lr = res['alpha']
    print 'Max LR tried: ', max_lr
