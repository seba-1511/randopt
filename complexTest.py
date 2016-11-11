#!/usr/bin/env python

import randopt as ro

def loss(w, x, y, z):
    return w**2 + x**2 + y**2 + z**2

if __name__ == '__main__':

    e = ro.Experiment('complexTest', {
            'normal'  : ro.Normal(mean=0.0, std=1.0, dtype='float'),
            'uniform' : ro.Uniform(low=-1.0, high=1.0, dtype='float'),
            'gaussian': ro.Gaussian(mean=0.0, std=1.0, dtype='float'),
            'choice'  : ro.Choice([0.01, 0.05, 0.1, 0.5, 0.7, 0.9], sampler=ro.Uniform()),
        })

    # Seeding will make all of your searches reproducible. (Usually not wanted)
    # e.seed(1234)

    # Randomly sampling parameters
    for i in xrange(1000):
        g = e.sample('gaussian')
        c = e.sample('choice')
        n = e.sample('normal')
        u = e.sample('uniform')
        res = loss(e.gaussian, e.choice, e.uniform, e.normal)
        print 'Result: ', res
        e.add_result(res)

    # Search over all experiments results, including ones from previous runs
    opt = e.minimum()
    print 'Best result: ', opt.value, ' with params: ', opt.params
