#!/usr/bin/env python

import os
import json as json
import random
import cPickle as pk

from time import time
from collections import namedtuple

"""
This file implements the Experiment class.

TODO:
    * Add option to check if experiment was already ran. (search through json)
    * Add option to run Bayesian opti, based on previous exp.
    * Unit tests
"""

leq = lambda x, y: x <= y
geq = lambda x, y: x >= y

OptResult = namedtuple('OptResult', ['value', 'params'])


class Experiment(object):

    def __init__(self, name, params):
        self.name = name
        self.params = params
        for key in params:
            setattr(self, key, None)
        cwd = os.getcwd()
        randopt_folder = os.path.join(cwd, 'randopt_results')
        if not os.path.exists(randopt_folder):
            os.mkdir(randopt_folder)
        self.experiment_path = os.path.join(randopt_folder, self.name)
        if not os.path.exists(self.experiment_path):
            os.mkdir(self.experiment_path)

    @property
    def current(self):
        res = {}
        for key in self.params:
            res[key] = getattr(self, key)
        return res

    def _search(self, fn=leq):
        value, params = None, None
        for fname in os.listdir(self.experiment_path):
            base, ext = os.path.splitext(fname)
            if 'json' in ext:
                fpath = os.path.join(self.experiment_path, fname)
                with open(fpath, 'r') as f:
                    res = json.load(f)
                    if value is None or fn(float(res['result']), value):
                        value = float(res['result'])
                        params = res
        return OptResult(value, params)

    def maximum(self):
        return self._search(geq)

    def minimum(self):
        return self._search(leq)

    def seed(self, seed):
        for key in self.params:
            self.params[key].seed(seed)

    def set(self, key, value):
        setattr(self, key, value)
        return value

    def sample(self, key):
        value = self.params[key].sample()
        setattr(self, key, value)
        return value

    def sample_all_params(self):
        for key in self.params:
            self.sample(key)
        return self.current

    def add_result(self, result, data=None):
        """Data is a dict containing additional data about the experiment"""
        res = {'result': str(result)}
        for key in self.params:
            res[key] = str(getattr(self, key))
        if data is not None:
            for key in data:
                res[key] = str(data[key])
        fname = str(time()) + '_' + str(random.random()) + '.json'
        fpath = os.path.join(self.experiment_path, fname)
        with open(fpath, 'w') as f:
            json.dump(res, f)

    def save_state(self, path):
        """Saves the random state of the variables into a file"""
        states = dict()
        for key in self.params:
            states[key] = self.params[key].get_state()
        with open(path, 'wb') as f:
            pk.dump(states, f, protocol=-1)

    def set_state(self, path):
        """Sets the random state of variables from a file"""
        with open(path, 'rb') as f:
            states = pk.load(f)
            for key in self.params:
                if key in states:
                    self.params[key].set_state(states[key])
