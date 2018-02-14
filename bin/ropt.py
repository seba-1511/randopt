#!/usr/bin/env python3

"""
Docstring

Allows sampling from outside of Python.

Note: --nproc is currently unsupported, until I find a way to cleanly kill all
      sub-processes.

Example:
    ropt.py python example.py run --nproc 4 --nsearch 16 --lr 'Choice([0.1,0.2,0.3])' --wd='uniform(0,10)'

    Runs 16 searches with up to 4 processes in parallel (these are ropt.py parameters)
    of the command 'python example.py run --lr X --wd=Y' where X is sampled from a the given 
    Choice distribution and Y is sampled from Uniform(0, 10).

TODO:
    * Add support for different kinds of experiments (HyperBand, BayesOpt).
      This means: pass the name of experiment and name of class to be used for sampling.
"""

import os
import sys
import subprocess
import multiprocessing as mp
import randopt as ro


class CommandGenerator(object):
    def __init__(self, command, parameters, samplers):
        self.command = command
        self.parameters = parameters
        self.samplers = samplers

    def __iter__(self):
        return self

    def __next__(self):
        com = self.command
        for p, s in zip(self.parameters, self.samplers):
            com += ' ' + p + ' ' + str(s.sample()) 
        return com


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


def parse_equality_param(arg):
    param = ''
    if '=' in arg:
        cut = arg.index('=')
        param += arg[cut+1:]
    return param


def parse_param(args):
    if '=' in args[0]:
        return 0, parse_equality_param(args[0])
    if '--' in args[1]:
        return 0, args[0]
    return 1, args[1]

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


if __name__ == '__main__':
    n_searches = -1
    n_processes = 1
    arguments = sys.argv[1:]
    args_idx = 0

    command = ''
    # Parse main command
    if '-c' in arguments[0] or '--command' in arguments[0]:
        if '=' in arguments[0]:
            command += parse_equality_param(arguments[0])
            args_idx += 1

    while '--' not in arguments[args_idx]:
        command += ' ' + arguments[args_idx]
        args_idx += 1

    # Parse arguments
    parameters = []
    samplers = []

    while args_idx < len(arguments):
        arg = arguments[args_idx]
        if '--nproc' in arg:
            shift, param = parse_param(arguments[args_idx:])
            n_processes = int(param)
            args_idx += shift
        elif '--nsearch' in arg:
            shift, param = parse_param(arguments[args_idx:])
            n_searches = int(param)
            args_idx += shift
        elif '--' not in arg:
            parameters[-1] += ' ' + arg
        else:
            shift, param = parse_param(arguments[args_idx:])
            if '--' in param:
                parameters[-1] += ' ' + param
            else:
                sampler = parse_sampler(param)
                if '=' in arg:
                    arg = arg[:arg.index('=')]
                parameters.append(arg)
                samplers.append(sampler)
            args_idx += shift
        args_idx += 1

    # Generate the right number of commands
    command_generator = CommandGenerator(command, parameters, samplers)
    if n_searches == -1:
        n_searches = float('inf')
        commands = command_generator
    else:
        commands = (next(command_generator) for _ in range(n_searches))

    # Run until search finishes
    call = lambda x: subprocess.call(x, shell=True)
    for i, command in enumerate(commands):
        print(i, ':', command)
        call(command)
