#!/usr/bin/env python

import randopt as ro

def loss(x):
    return x**2

if __name__ == '__main__':

    e = ro.Experiment('myexp', {
            # 'alpha': ro.Normal(low=-1.0, high=1.0, dtype='float'),
            'alpha': ro.Gaussian(mean=0.0, std=1.0, dtype='float'),
            # 'alpha': ro.Choice([0.01, 0.05, 0.1, 0.5, 0.7, 0.9], sampler=ro.Uniform()),
        })

    # e.seed(1234)

    for i in xrange(100):
        alpha = e.sample_alpha()
        res = loss(e.alpha)
        print 'Result: ', res
        e.add_result(res)

    opt = e.minimum()
    print 'Best result: ', opt.value, ' with params: ', opt.params
