#!/usr/bin/env python

import os
try:
    import ujson as json
except ImportError:
    import json
import random
import cPickle as pk

from time import time
from math import log, ceil
from collections import namedtuple

from samplers import Uniform

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

    def top(self, count, fn=leq):
        top_n_experiments = []
        for fname in os.listdir(self.experiment_path):
            base, ext = os.path.splitext(fname)
            if 'json' in ext:
                fpath = os.path.join(self.experiment_path, fname)
                with open(fpath, 'r') as f:
                    res = json.load(f)

                    #save the result
                    result_value = float(res['result'])
                    #delete it from the dict
                    del res['result']

                    if len(top_n_experiments) < count:
                        top_n_experiments.append((result_value, res))
                    else:
                        #iterate over each item in the list
                        for i in range(count):
                            if fn(result_value, top_n_experiments[i][0]):
                                #place the experiment in place
                                top_n_experiments.insert(i, (result_value, res))
                                #remove the next worst element
                                top_n_experiments.pop()
                                break

        #sort the past experiments and then unzip to drop the result value
        results, dict_of_params = zip(*top_n_experiments)

        return dict_of_params

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


class HyperBand(Experiment):

    """
    HyperBand implementation, based on
    http://people.eecs.berkeley.edu/~kjamieson/hyperband.html
    """

    def __init__(self, name, params, num_iter, eta=None, comparator=None):
        super(HyperBand, self).__init__(name, params)
        if eta is None:
            eta = 2.718281828
        self.eta = eta
        if comparator is None:
            comparator = leq
        self.comparator = comparator
        self.num_iter = num_iter
        self.hyperband_path = os.path.join(self.experiment_path, 'hyperband')
        if not os.path.exists(self.hyperband_path):
            os.mkdir(self.hyperband_path)
        self.logeta = lambda x: log(x) / log(self.eta)
        self.s_max = int(self.logeta(self.num_iter))
        B = (self.s_max + 1) * self.num_iter
        self.s = self._get_s_value()
        self.n = int(ceil(B / self.num_iter / (self.s + 1) * (self.eta**self.s)))
        self.r = self.num_iter * (self.eta**(-self.s))
        self.curr_iter = 0
        self.i = 0
        self.curr_nconfig = int(self.n * self.eta**(self.i) / self.eta)
        self.next_update = int(self.r * self.eta**(self.i))
        fname = str(time()) + '_' + str(random.random()) + '.json'
        self.hb_file = os.path.join(self.hyperband_path, fname)

    def _find_run(self, s=None):
        res_list = []
        for fname in os.listdir(self.hyperband_path):
            base, ext = os.path.splitext(fname)
            if 'json' in ext:
                fname = os.path.join(self.hyperband_path, fname)
                with open(fname, 'r') as f:
                    res = json.load(f)
                    if res['s'] == s:
                        res_list.append(res)
        return res_list

    def _get_s_value(self):
        i = 1
        while True:
            for s in reversed(range(self.s_max + 1)):
                if len(self._find_run(s=s)) < (s + 1) * i:
                    return s
            i += 1

    def _update_hyperband_result(self, score):
        if not os.path.exists(self.hb_file):
            open(self.hb_file, 'a').close()
        with open(self.hb_file, 'r+') as f:
            if self.curr_iter == 1:
                res = {
                        's': self.s,
                        'n': self.n,
                        'r': self.r,
                        'num_iter': self.num_iter,
                        'i': self.i,
                        'results': [score, ],
                        }
                res.update(self.current)
            else:
                res = json.load(f)
                res['results'].append(score)
            f.seek(0)
            json.dump(res, f)

    def _continue(self, curr_iter, nb_config, score):
        num_seen = 0
        bound = None
        for fname in os.listdir(self.hyperband_path):
            base, ext = os.path.splitext(fname)
            if 'json' in ext:
                fname = os.path.join(self.hyperband_path, fname)
                with open(fname, 'r') as f:
                    res = json.load(f)
                    if len(res['results']) >= curr_iter and (
                            num_seen < nb_config or self.comparator(res['results'][curr_iter-1], bound)):
                        bound = res['results'][curr_iter-1]
                        num_seen += 1
        if num_seen < 1:
            return True
        if self.comparator(score, bound):
            return True
        return False
        

    def stop(self, validation_result):
        self.curr_iter += 1
        stop = False
        if self.curr_iter % self.next_update == 0:
            stop = not self._continue(self.curr_iter, self.curr_nconfig,
                                      validation_result)
            self.i += 1
            self.next_update = int(self.r * self.eta**(self.i))
            self.curr_nconfig = int(self.n * self.eta**(-self.i) / self.eta)
        self._update_hyperband_result(validation_result)
        return stop
