#!/usr/bin/env python

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

"""
This file implements the Experiment class.
"""

ATTACHMENT_DIR = '_attachments'
ATTACHMENT_EXT = '.pk'

leq = lambda x, y: x <= y
geq = lambda x, y: x >= y

OptResult = namedtuple('OptResult', ['value', 'params'])


class JSONSummary(object):

    def __init__(self, path):
        assert(path[-5:] == '.json')
        with open(path, 'r') as f:
            result = json.load(f)
        self.__summary = result
        self.__attachment = None
        self.__path = path
        self.__dir = os.path.dirname(path)
        self.__name = os.path.basename(path)[:-5]

    def __getattr__(self, attr):
        if attr in self.__summary.keys():
            return self.__summary[attr]
        elif attr == 'attachment':
            self._load_attachment()
            return self.__attachment
        elif attr == 'value':
            print('WARNING: .value is deprecated in favor of .result')
            return self.result
        elif attr == 'params':
            return self.__summary
        else:
            msg = 'Attribute ' + attr + ' is not implement in JSONSummary.'
            raise(NotImplementedError(msg))

    def __str__(self):
        return 'JSONSummary ' + str(self.__name) + ' with value ' + str(self.result)

    def _load_attachment(self):
        if self.__attachment is None:
            att_path = os.path.join(self.__dir, ATTACHMENT_DIR)
            att_path = os.path.join(att_path, self.__name + ATTACHMENT_EXT)
            with open(att_path, 'rb') as f:
                self.__attachment = pk.load(f)


class Experiment(object):

    '''
    Main class to create, manage, and search experimental results.

    Parameters:

    * name - (string) name of experiment.
    * params - (dict) dicitionary of parameter names to their random sampling functions.
    * directory - (string) directory in which the experiment will be saved. Default: randopt_results

    Return type: n/a

    Example:

        e = ro.Experiment('exp_name', {
            'batch_size' : ro.Uniform(low=5.0, high=150.0, dtype='int'),
            'iterations': ro.Normal(mean=1000.0, std=150.0, dtype='int'),
            'learning_rate' : ro.Uniform(low=0.0001, high=0.01, dtype='float'),
        })
    '''

    def __init__(self, name, params={}, directory='randopt_results'):
        self.name = name
        self.params = params
        for key in params:
            if key is not 'result':
                setattr(self, key, None)
            else:
                raise ValueError('Param cannot be named \'result\'')
        cwd = os.getcwd()
        randopt_folder = os.path.join(cwd, directory)
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
        result = None
        for fname in os.listdir(self.experiment_path):
            base, ext = os.path.splitext(fname)
            if 'json' in ext:
                fpath = os.path.join(self.experiment_path, fname)
                candidate = JSONSummary(fpath)
                if result is None or fn(candidate.result, result.result):
                    result = candidate
        return result

    def top(self, count, fn=leq):
        '''
        Returns the top count best results. By default, minimum.

        Parameters:

        * count - (int) number of results to return.
        * fn - (function) comparison function. Default: leq

        Return type: dict of parameters

        Example:

            e.top(3)
        '''
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

                    # TODO: refactor this insert function to be cleaner
                    if len(top_n_experiments) < count:
                        inserted = False
                        for i in range(len(top_n_experiments)):
                            if fn(result_value, top_n_experiments[i][0]):
                                #place the experiment in place
                                top_n_experiments.insert(i, (result_value, res))
                                inserted = True
                                break
                        if not inserted:
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
        '''
        Returns the maximum result from saved results.

        Parameters: n/a

        Return type: float

        Example:

            e.maximum()
        '''
        return self._search(geq)

    def minimum(self):
        '''
        Returns the minimum result from saved results.

        Parameters: n/a

        Return type: float

        Example:

            e.minimum()
        '''
        return self._search(leq)

    def all(self):
        '''
        Alias for Experiment.all_results()

        Example:

            e.all_results()
        '''
        for r in self.all_results():
            yield r

    def count(self):
        '''
        Returns the number of JSON summaries.

        Parameters: n/a

        Return type: int

        Example:

            e.count()
        '''
        return len(list(self.all()))


    def seed(self, seed):
        '''
        Manually set a seed value.

        Parameters:

        * seed - (int) random seed.

        Return type: n/a

        Example:

            e.seed(1234)
        '''
        for key in self.params:
            self.params[key].seed(seed)

    def set(self, key, value):
        setattr(self, key, value)
        return value

    def sample(self, key):
        '''
        Generates, sets, and returns a randomly sampled value for given parameter.

        Parameters:

        * key - (string) name of randomly sampled parameter

        Return type: float/int

        Example:

            e.sample('iterations')

        '''
        value = self.params[key].sample()
        setattr(self, key, value)
        return value

    def sample_all_params(self):
        '''
        Generates a randomly sampled value for all specified parameters.

        Parameters: n/a

        Return type: dict of parameters and values.

        Example:

            e.sample_all_params()
        '''
        for key in self.params:
            self.sample(key)
        return self.current

    def add_result(self, result, data=None, attachment=None):
        '''
        Generates a randomly sampled value for all specified parameters

        Parameters:

        * result - (float) value for the current set of hyperparameters.
        * data - (dict) additional logging data.
        * attachment - (dict) attachment data excluded from JSON summary.

        Return type: n/a

        Example:

            e.add_result(loss)
        '''
        res = {'result': result}
        for key in self.params:
            res[key] = getattr(self, key)
        if data is not None:
            for key in data:
                res[key] = data[key]
        fname = str(time()) + '_' + str(random.random())
        fpath = os.path.join(self.experiment_path, fname) + '.json'
        with open(fpath, 'w') as f:
            json.dump(res, f)
        if attachment is not None:
            assert(isinstance(attachment, dict))
            att_path = os.path.join(self.experiment_path, ATTACHMENT_DIR)
            if not os.path.exists(att_path):
                os.mkdir(att_path)
            att_file = os.path.join(att_path, fname + ATTACHMENT_EXT)
            with open(att_file, 'wb') as f:
                pk.dump(attachment, f)

    def all_results(self):
        '''
        Iterates through all previous results in no specific order

        Parameters: n/a

        Return type: iterator

        Example:

            for res in e.all_results():
                print res.value
        '''
        value, params = None, None
        for fname in os.listdir(self.experiment_path):
            base, ext = os.path.splitext(fname)
            if 'json' in ext:
                fpath = os.path.join(self.experiment_path, fname)
                with open(fpath, 'r') as f:
                    try:
                        res = json.load(f)
                        value = float(res['result'])
                        params = res
                        yield OptResult(value, params)
                    except ValueError:
                        print('Error reading file: ' + fpath + ' - skipped.')

    def save_state(self, path):
        '''
        Saves the state of the random variables into a file.

        Parameters:

        * path - (string) target filepath

        Return type: n/a

        Example:

            e.save_state(states/curr_state.pk)
        '''
        states = dict()
        for key in self.params:
            states[key] = self.params[key].get_state()
        with open(path, 'wb') as f:
            pk.dump(states, f, protocol=-1)

    def set_state(self, path):
        '''
        Sets the state of random variables from a file

        Parameters:

        * path - (string) target filepath

        Return type: n/a

        Example:

            e.set_state(states/curr_state.pk)
        '''
        with open(path, 'rb') as f:
            states = pk.load(f)
            for key in self.params:
                if key in states:
                    self.params[key].set_state(states[key])
