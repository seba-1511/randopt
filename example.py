#!/usr/bin/env python

import randopt as ro

def loss(x):
    return x**2

if __name__ == '__main__':
    e = ro.Experiment('myexp', {
            'alpha': ro.uniform(low=-1.0, high=1.0, dtype='float'),
        })
    for i in xrange(1000):
        res = loss(e.alpha)
        e.add_result(res)
    print 'Best result: ', e.opt_value, ' with params: ', e.opt_params
