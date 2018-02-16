#!/usr/bin/env python

import randopt as ro

def loss(x, y):
    return x**2 + y**2

if __name__ == '__main__':

    e = ro.Experiment('gs_example', {
            'alpha': ro.Choice([0.1, 0.2, 0.3]),
            'beta': ro.Choice([0.1, 0.2, 0.3]),
        })

    # Add a single result
    e.alpha = 0.1
    e.beta = 0.1
    #e.add_result(loss(0.1, 0.1))

    gs = ro.GridSearch(e)
    gs.sample('alpha')
    # Sampling parameters
    for i in range(9):
        gs.refresh_index()
        gs.sample_all_params()
        res = loss(gs.alpha, gs.beta)
        print('Result: ', res)
        gs.add_result(res)

    # Search over all experiments results, including ones from previous runs
    opt = gs.minimum()
    print('Best result: ', opt.value, ' with params: ', opt.params)
