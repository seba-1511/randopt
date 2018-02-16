#!/usr/bin/env python3

from .experiment import Experiment


class GridSearch(Experiment):

    """
    Performs a grid-search on the parameters of a given experiment.

    Only accepts `Choice` as parameter sampler.
    """

    def __init__(self, experiment):
        # TODO: Assert that all params are Choice
        # TODO: Build index of what experiments have been ran
        self.__dict__.update(experiment)

    def refresh_index(self):
        pass

    def sample(self, key):
        # Given current params, choose the experiment that will fill the index
        pass

    def sample_all_params(self):
        # Do the first experiment that has been done less than all others
        # This function can not use sample, else we might end up trapped
        pass
