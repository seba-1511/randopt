#!/usr/bin/env python

import randopt as ro

def loss(x):
    return x**2

if __name__ == '__main__':

    e = ro.Experiment('myexp', {
            'alpha': ro.Uniform(low=-1.0, high=1.0, dtype='float'),
        })

    for i in xrange(100):
        alpha = e.sample_alpha()
        res = loss(e.alpha)
        print 'Result: ', res
        e.add_result(res)

    opt = e.minimum()
    print 'Best result: ', opt.value, ' with params: ', opt.params
