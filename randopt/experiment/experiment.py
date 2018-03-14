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

TODO:
    * Add option to check if experiment was already ran. (search through json)
"""

leq = lambda x, y: x <= y
geq = lambda x, y: x >= y

OptResult = namedtuple('OptResult', ['value', 'params'])


class Experiment(object):

    '''
    Description:

        Initializes experiment

    Parameters:

        * name - name of experiment
        * params - dicitionary of parameter names to their random sampling functions

    Return type:

        n/a

    Example:

        e = ro.Experiment('neuralnet_ftp', {
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
        '''
        Description:

            Returns the top count best results. By default, minimum

        Parameters:

            * count - integer
            * fn=leq,geq - optional, set to geq for maximal values

        Return type:

            dictionary of parameters

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
        Description:

            Returns the maximum result after experimentation

        Parameters:

            n/a

        Return type:

            Maximum result

        Example:

            e.maximum()
        '''
        return self._search(geq)

    def minimum(self):
        '''
        Description:

            Returns the minimum result after experimentation

        Parameters:

            n/a

        Return type:

            Minimum result

        Example:

            e.minimum()
        '''
        return self._search(leq)

    def seed(self, seed):
        '''
        Description:

            Manually set a seed value

        Parameters:

            * seed : integer

        Return type:

            n/a

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
        Description:

            Generates a randomly sampled value for given parameter

        Parameters:

            * key - name of randomly sampled parameter

        Return type:

            Value of randomly generated value for specified sampler

        Example:

            e.sample('iterations')

        '''
        value = self.params[key].sample()
        setattr(self, key, value)
        return value

    def sample_all_params(self):
        '''
        Description:

            Generates a randomly sampled value for all specified parameters

        Parameters:

            n/a

        Return type:

            self.current

        Example:

            e.sample_all_params()
        '''
        for key in self.params:
            self.sample(key)
        return self.current

    def add_result(self, result, data=None):
        '''
        Description:

            Generates a randomly sampled value for all specified parameters

        Parameters:

            * result - resultant value
            * data - dict of {result_name: value}

        Return type:

            n/a

        Example:

            e.add_result(loss)
        '''
        res = {'result': result}
        for key in self.params:
            res[key] = getattr(self, key)
        if data is not None:
            for key in data:
                res[key] = data[key]
        fname = str(time()) + '_' + str(random.random()) + '.json'
        fpath = os.path.join(self.experiment_path, fname)
        with open(fpath, 'w') as f:
            json.dump(res, f)

    def all_results(self):
        '''
        Description:

            Iterates through all previous results in no specific order

        Parameters:

            n/a

        Return type:

            iterator

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
        Description:

            Saves the state of the random variables into a file

        Parameters:

            path - target filepath

        Return type:

            n/a

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
        Description:

            Sets the state of random variables from a file

        Parameters:

            * path - target filepath

        Return type:

            n/a

        Example:

            e.set_state(states/curr_state.pk)
        '''
        with open(path, 'rb') as f:
            states = pk.load(f)
            for key in self.params:
                if key in states:
                    self.params[key].set_state(states[key])
