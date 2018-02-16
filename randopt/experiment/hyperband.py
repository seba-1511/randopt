#!/usr/bin/env python3

import os
import random
try:
    import ujson as json
except ImportError:
    import json
try:
    import cPickle as pk
except ImportError:
    import pickle as pk

from time import time
from math import log, ceil
from collections import namedtuple

from randopt.samplers import Uniform
from .experiment import Experiment, leq, geq


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
            # TOOD: Decide whether to use the following or .
            # for s in range(self.s_max + 1):
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
        # TODO: That is slow.
        # FIX: Load in memory, check update time of folder.
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
        """
        Current problem: The first few runs are compared against empty ones,
                         and so will have to run until the end.
                         Think of a good fix.
        """
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
