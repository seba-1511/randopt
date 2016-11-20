#!/usr/bin/env python

import randopt as ro

def loss(w, x, y, z):
    return w**2 + x**2 + y**2 + z**2

if __name__ == '__main__':

    e = ro.Experiment('multi_params_example', {
            'dog'  : ro.Normal(mean=0.0, std=1.0, dtype='float'),
            'cat' : ro.Uniform(low=-1.0, high=1.0, dtype='float'),
            'dolphin': ro.Gaussian(mean=0.0, std=1.0, dtype='float'),
            'any_name'  : ro.Choice([0.01, 0.05, 0.1, 0.5, 0.7, 0.9], sampler=ro.Uniform()),
        })

    # Seeding will make all of your searches reproducible. (Usually not wanted)
    e.seed(1234)

    # Randomly sampling parameters
    for i in xrange(100):
        e.sample_all_params()
        res = loss(e.dog, e.cat, e.dolphin, e.any_name)
        print 'Result: ', res
        e.add_result(res)

    # Save/load the state of the random number generators
    e.save_state('./multi_params_state.pk')
    e.set_state('./multi_params_state.pk')

    # Search over all experiments results, including ones from previous runs
    opt = e.minimum()
    print 'Best result: ', opt.value, ' with params: ', opt.params
    opt = e.maximum()
    print 'Worst result: ', opt.value, ' with params: ', opt.params

    # Grab the top N results
    best_runs = e.top(3)
    print 'Best 3 results: ', best_runs
