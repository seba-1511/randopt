#!/usr/bin/env python

import os
import json
import random

from time import time
from collections import namedtuple

"""
This file implements the Experiment class.
"""

leq = lambda x, y: x <= y
geq = lambda x, y: x >= y


class Experiment(object):

    def __init__(self, name, params):
        self.name = name
        self.params = params
        for key in params:
            setattr(self, 'sample_' + key, self._sample(key))
            setattr(self, 'set_' + key, self._set(key))
            setattr(self, key, None)
        cwd = os.getcwd()
        randopt_folder = os.path.join(cwd, 'randopt_results')
        if not os.path.exists(randopt_folder):
            os.mkdir(randopt_folder)
        self.experiment_path = os.path.join(randopt_folder, self.name)
        if not os.path.exists(self.experiment_path):
            os.mkdir(self.experiment_path)

    def _sample(self, key):
        def fn():
            value = self.params[key].sample()
            setattr(self, key, value)
            return value
        return fn

    def _set(self, key):
        def fn(value):
            setattr(self, key, value)
            return value
        return fn

    def _search(self, fn=leq):
        opt = namedtuple('OptResult', ['value', 'params'])
        opt.value = None
        opt.params = None

        for fname in os.listdir(self.experiment_path):
            base, ext = os.path.splitext(fname)
            if 'json' in ext:
                fpath = os.path.join(self.experiment_path, fname)
                with open(fpath, 'r') as f:
                    res = json.load(f)
                    if opt.value is None or fn(res['result'], opt.value):
                        opt.value = res['result']
                        opt.params = res
        return opt

    def maximum(self):
        return self._search(geq)

    def minimum(self):
        return self._search(leq)

    def seed(self, seed):
        for key in self.params:
            self.params[key].seed(seed)

    def add_result(self, result, data=None):
        """Data is a dict containing additional data about the experiment"""
        res = {'result': result}
        for key in self.params:
            res[key] = getattr(self, key)
        fname = str(time()) + '_' + str(random.random()) + '.json'
        fpath = os.path.join(self.experiment_path, fname)
        with open(fpath, 'w') as f:
            json.dump(res, f)

    def save_state(self, path):
        """Saves the random state of the variables into a file"""
        pass

    def set_state(self, path):
        """Sets the random state of variables from a file"""
        pass
