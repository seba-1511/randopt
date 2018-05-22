#!/usr/bin/env python3

"""

Allows sampling and hyper-parameter search from outside of Python.

Note: ROPT_NPROC is currently unsupported, until I find a way to cleanly kill all
      sub-processes.

Example:
    ROPT_NSEARCH=16 ROPT_NPROC=4 ropt.py python example.py run --lr='Choice([0.1,0.2,0.3])' --wd='uniform(0,10)'

    Runs 16 searches with up to 4 processes in parallel (these are ropt.py parameters)
    of the command 'python example.py run --lr X --wd Y' where X is sampled from  the given 
    Choice distribution and Y is sampled from Uniform(0, 10).

Another example using Search wrappers is

    ROPT_TYPE=GridSearch ROPT_NAME=newton-2_experiment ropt.py CUDA_VISIBLE_DEVICES=0 python experiments.py main newton --lr="Choice([0.01,0.1])"

The convention is to always pass sampled arguments to ropt with an = sign, to wrap the sampler in quotes (required by most shells), and avoid spaces within these quotes. The choice of quotes and the casing for samplers is irrelevant.
"""

import os
import sys
import subprocess
import multiprocessing as mp
import randopt as ro

ROPT_TYPE = 'ROPT_TYPE'
ROPT_NAME = 'ROPT_NAME'
ROPT_DIR = 'ROPT_DIR'
ROPT_NSEARCH = 'ROPT_NSEARCH'
ROPT_NPROC = 'ROPT_NPROC'


class CommandGenerator(object):
    def __init__(self, command, parameters, samplers):
        self.command = command
        self.parameters = parameters
        self.samplers = samplers

    def __iter__(self):
        return self

    def __next__(self):
        values = [s.sample() for s in self.samplers]
        return self.command.format(*values)

    next = __next__


class ExperimentSampler(object):

    def __init__(self, command, parameters, experiment):
        self.experiment = experiment
        self.command = command
        self.parameters = parameters

    def __iter__(self):
        return self

    def __next__(self):
        self.experiment.sample_all_params()
        current = self.experiment.current
        values = [current[p] for p in self.parameters]
        return self.command.format(*values)

    next = __next__


def is_number(s):
    """
    Copy-pasted from:
    https://www.pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


def parse_sampler(param):
    values = param[param.index('(') + 1:param.index(')')]
    if '[' in values or '(' in values:
        values = values[1:-1].split(',')
        values = [float(v) if is_number(v) else v for v in values]
        values = [values, ]
    else:
        values = values.split(',')
        values = [float(v) if is_number(v) else v for v in values]
    sampler = param[:param.index('(')].lower()
    samplers = {
        'uniform': ro.Uniform,
        'gaussian': ro.Gaussian,
        'normal': ro.Normal,
        'choice': ro.Choice,
        'constant': ro.Constant,
        'lognormvariate': ro.LognormVariate,
        'betavariate': ro.BetaVariate,
        'expovariate': ro.ExpoVariate,
        'weibullvariate': ro.WeibullVariate,
        'paretovariate': ro.ParetoVariate,
    }
    if sampler not in samplers:
        msg = 'The requested distribution is not implemented, yet.'
        raise NotImplementedError(msg)
    return samplers[sampler](*values)


def parse_experiment(param):
    if 'evo' in param.lower():
        return ro.Evolutionary
    elif 'grid' in param.lower():
        return ro.GridSearch
    else:
        msg = 'Experiment class not implemented in ropt.py yet.'
        raise NotImplementedError(msg)


if __name__ == '__main__':
    experiment = None
    if ROPT_TYPE in os.environ:
        experiment = os.environ[ROPT_TYPE]
        experiment = parse_experiment(experiment)
    experiment_name = None
    if ROPT_NAME in os.environ:
        experiment_name = os.environ[ROPT_NAME]
    experiment_dir = 'randopt_results'
    if ROPT_DIR in os.environ:
        experiment_dir = os.environ[ROPT_DIR]
    n_searches = -1
    if ROPT_NSEARCH in os.environ:
        n_searches = int(os.environ[ROPT_NSEARCH]) 
    n_processes = 1
    if ROPT_NPROC in os.environ:
        experiment_name = int(os.environ[ROPT_NPROC]) 

    print('Working on', experiment_name, 'in', experiment_dir)

    arguments = sys.argv[1:]
    args_idx = 0

    command = ""
    parameters = []
    samplers = []
    for arg in arguments:
        if '=' in arg and '(' in arg and ')' in arg:
            # parse argument and sampler
            param, sampler = arg.split('=')
            command = command + ' ' + param + ' {' + str(len(samplers)) + ':.10f}'
            sampler = parse_sampler(sampler)
            param = param.replace('-', '')
            parameters.append(param)
            samplers.append(sampler)
        else:
            command = command + ' ' + arg

    # Generate the right number of commands
    if experiment is not None and experiment_name is not None:
        print('Using ', experiment.__name__)
        print('sys: ', sys.argv)
        params = {p: s for p, s in zip(parameters, samplers)}
        experiment = experiment(ro.Experiment(name=experiment_name,
                                              params=params,
                                              directory=experiment_dir))
        command_generator = ExperimentSampler(command, parameters, experiment)
    else:
        command_generator = CommandGenerator(command, parameters, samplers)

    if n_searches == -1:
        n_searches = float('inf')
        commands = command_generator
    else:
        commands = (next(command_generator) for _ in range(n_searches))

    # Run until search finishes
    for i, command in enumerate(commands):
        print(i, ':', command)
        subprocess.call(command, shell=True)
