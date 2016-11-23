#!/usr/bin/env python

import randopt as ro


def loss(x):
    return x**2 + 2*x - 3


def dloss(x):
    return 2*x + 2


def grad_descent(f, df, init, num_epochs, lr):
    params = init
    convergence = []
    for epoch in range(num_epochs):
        params = params - (lr * df(params))
        convergence.append(f(params))
    # Return final result + convergence array
    return f(params), convergence

if __name__ == '__main__':
    init = 10.0
    num_runs = 100

    exp = ro.Experiment('grad_descent', {
        'learning_rate': ro.Gaussian(mean=0.01, std=0.01),
        'num_epochs': ro.Truncated(
            ro.Gaussian(mean=50, std=10, dtype='int'),
            low=10,
            high=100)
        })

    # Run the experiment a couple of time
    for _ in range(num_runs):
        exp.sample_all_params()
        result, convergence = grad_descent(loss, dloss, init, exp.num_epochs,
                                           exp.learning_rate)
        exp.add_result(result, data={
            'convergence': convergence
            })

        opt = exp.minimum()
    print 'Optimal result: ', opt.value, ', with convergence: ', opt.params['convergence']
