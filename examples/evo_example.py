#!/usr/bin/env python

import randopt as ro

def loss(x):
    return x**2

if __name__ == '__main__':

    e = ro.Experiment('evo_example', {
            'alpha': ro.Gaussian(mean=0.0, std=1.5, dtype='float'),
        })

    # Populate with first result
    e.sample('alpha')
    res = loss(e.alpha)
    e.add_result(res)

    # Evolutionary search
    e = ro.Experiment('evo_example', {
            # Evolutionary will use alpha.sample() as perturbation
            'alpha': ro.Gaussian(mean=0.0, std=0.5, dtype='float'),
        })
    evo = ro.Evolutionary(e)
    for i in range(100):
        evo.sample_parent()
        evo.sample_all_params()
        res = loss(evo.alpha)
        print('Result: ', res)
        evo.add_result(res)


    # Search over all experiments results, including ones from previous runs
    opt = e.minimum()
    print('Best result: ', opt.result, ' with params: ', opt.params)

