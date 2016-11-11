#!/usr/bin/env python

import randopt as ro

def loss(x):
    return x**2

if __name__ == '__main__':

    e = ro.Experiment('myexp', {
            # 'alpha': ro.Normal(low=-1.0, high=1.0, dtype='float'),
            #'alpha': ro.Gaussian(mean=0.0, std=1.0, dtype='float'),
            # 'alpha': ro.Choice([0.01, 0.05, 0.1, 0.5, 0.7, 0.9], sampler=ro.Uniform()),
            #'alpha' : ro.Choice([0, 1, 2, 3, 4], sampler=ro.Uniform()),
            #'alpha' : ro.Lognormal(mean=0.0, std=1.0, dtype='float'),
            'alpha' : ro.Poisson(lam=1.0, max_k=10.0, dtype='float'),

        })

    # Seeding will make all of your searches reproducible. (Usually not wanted)
    # e.seed(1234)

    # Randomly sampling parameters
    for i in xrange(100):
        alpha = e.sample('alpha')
        res = loss(e.alpha)
        print 'Result: ', res
        e.add_result(res)

    # Manually setting parameters
    e.alpha = 0.00001
    res = loss(e.alpha)
    e.add_result(res)

    # Search over all experiments results, including ones from previous runs
    opt = e.minimum()
    print 'Best result: ', opt.value, ' with params: ', opt.params
