#!/usr/bin/env python3


from random import sample
from .experiment import Experiment, leq


class Evolutionary(Experiment):

    """
    Description:
        Selects the best `elite_size` results according to `fitness()` from
        the current experiment. Uniformly samples one of them as a parent, and
        perturbs it using the experiment's samplers.

        Note that in order to change parent, you should call experiment.sample_parent()

    Parameters:
        experiment - experiment to wrap
        elite_size - number of results to consider as parents
        fitness - function to determine fitness of result

    Return type:
        n/a

    Example:
        evo = Evolutionary(experiment)
        evo.sample_parent()
        evo.sample_all_params()
        evo.add_result(loss(evo.params))
    """

    def __init__(self, experiment, elite_size=10, fitness=None):
        self.__dict__.update(experiment.__dict__)
        self.experiment = experiment
        self.elite_size = 10
        if fitness is None:
            fitness = leq
        self.fitness = fitness
        self.parent = None

    def sample_parent(self):
        elite = self.top(self.elite_size, fn=self.fitness)
        if len(elite) > 0:
            self.parent = sample(elite, 1)[0]
            return self.parent
        for p in self.params:
            self.set(p, 0.0)

    def sample(self, key):
        if self.parent is None:
            self.sample_parent()
        perturbation = self.params[key].sample()
        self.set(key, self.parent[key] + perturbation)
        self.experiment.set(key, self.parent[key] + perturbation)
