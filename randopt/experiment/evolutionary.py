#!/usr/bin/env python3


from random import sample
from .experiment import Experiment, leq


class Evolutionary(Experiment):

    """
    Selects the best `elite_size` results according to `fitness()` from
    the current experiment. Uniformly samples one of them as a parent, and
    perturbs it using the experiment's samplers.

    Note that in order to change parent, you should call experiment sample_parent()

    Parameters:

    * experiment - (Experiment) experiment to wrap.
    * elite_size - (int) number of results to consider as parents.
    * fitness - (function) function to determine fitness of result.

    Return type: n/a

    Example:

        experiment = Experiment('name', params={'lr': Gaussian()})
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
        '''
        Sets and returns a parent from currently available results.

        Parameters: n/a

        Return type: JSONSummary, the parent result.

        Example:

            evo.sample_parent()
        '''
        assert self.experiment.count() >= 1, 'Evolutionary can only be used with existing results.'
        elite = self.top(self.elite_size, fn=self.fitness)
        if len(elite) > 0:
            self.parent = sample(elite, 1)[0]
            return self.parent
        for p in self.params:
            self.set(p, 0.0)

    def sample(self, key):
        '''
        Generates a randomly sampled value for given parameter, which is
        a sampled perturbation plus the value of the current parent.

        Parameters:

        * key - name of randomly sampled parameter

        Return type: (float) Value of randomly generated value for specified sampler

        Example:

            e.sample('iterations')

        '''
        if self.parent is None:
            self.sample_parent()
        perturbation = self.params[key].sample()
        value = self.parent[key] + perturbation
        self.set(key, value)
        self.experiment.set(key, value)
        return value

    def sample_all_params(self):
        """
        Similar to Experiment.sample_all_params() but the parent is
        re-sampled first.
        """
        self.sample_parent()
        return super(Evolutionary, self).sample_all_params()
