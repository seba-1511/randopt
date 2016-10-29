#!/usr/bin/env python

"""
This file implements the Experiment class.
"""

class Experiment(object):

    def __init__(self, name, params):
        self.name = name
        self.params = params
        for key in params:
            setattr(self, 'sample_' + key, self._sample(key))
            setattr(self, key, None)

    @property
    def opt_value(self):
        return 1.1

    @property
    def opt_params(self):
        return 0.0

    def _sample(self, key):
        def fn():
            value = self.params[key].sample()
            setattr(self, key, value)
            return value
        return fn

    def seed(self, seed):
        for key in self.params:
            self.params[key].seed(seed)

    def add_result(self, result, additional_data=None):
        pass

    def save_state(self, path):
        """Saves the random state of the variables into a file"""
        pass

    def set_state(self, path):
        """Sets the random state of variables from a file"""
        pass
