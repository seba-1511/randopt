#!/usr/bin/env python3

from random import gauss
import randopt as ro
import randopt.objectives as obj

def converge(curve, mu, sigma):
    return [c + gauss(mu, sigma)**2 for c in curve]

if __name__ == '__main__':
    curve = [10 / x for x in range(1, 36)]

    loss = obj.median_variance

    exp = ro.Experiment('objectives_example', params={
        'mu': ro.Gaussian(3, 1),
        'sigma': ro.Gaussian(1, 1),
    })

    for _ in range(10):
        exp.sample_all_params()
        convergence = converge(curve, exp.mu, exp.sigma)
        exp.add_result(loss(convergence, 0.5, 0.5), data={
            'convergence': convergence,
            'normalized': obj.normalize(convergence),
            'curve': curve,
        })

    evo = ro.Evolutionary(exp, {
        'mu': ro.Gaussian(0.0, 0.1),
        'sigma': ro.Gaussian(0.0, 0.1),
    })
    for _ in range(100):
        evo.sample_all_params()
        convergence = converge(curve, evo.mu, evo.sigma)
        evo.add_result(loss(convergence, 0.5, 0.5), data={
            'convergence': convergence,
            'normalized': obj.normalize(convergence),
            'curve': curve,
        })

