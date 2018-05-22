#!/usr/bin/env python3

"""Utilities for custom command-line interfaces."""

import sys
import inspect
import numbers
import argparse
import collections

import randopt as ro

__ARGUMENTS = {}
__FUNCTIONS = {}
__DOCS = {}


def cli(fn=None):
    """Register decorator for command-line interface of general commands."""
    argspec = inspect.getargspec(fn)
    arg_names = argspec[0]
    arg_defaults = argspec[3]
    if not len(arg_names) == len(arg_defaults):
        print('randopt.cli: some arguments do not have default values.')
        sys.exit(-1)
    fn_name = fn.__name__
    global __FUNCTIONS
    if fn_name in __FUNCTIONS:
        print('randopt.cli: ', fn_name, 'already registered.')
        sys.exit(-1)
    __FUNCTIONS[fn_name] = fn
    global __DOCS
    __DOCS[fn_name] = fn.__doc__
    global __ARGUMENTS
    __ARGUMENTS[fn_name] = {name: default
                            for name, default in zip(arg_names, arg_defaults)}


def experiment(name, directory='randopt_results'):
    """
    Register decorator for commands whose return values experimental results.
    """
    def experiment_decorator(fn):
        # Parse and register function
        cli(fn)
        argspec = inspect.getargspec(fn)
        arg_names = argspec[0]
        arg_defaults = argspec[3]

        # Update registered function with experiment wrapper
        fn_name = fn.__name__

        def wrapper(*args, **kwargs):
            experiment = ro.Experiment(name=name, directory=directory, params={
                name: ro.Constant(default)
                for name, default in zip(arg_names, arg_defaults)
            })
            result = fn(*args, **kwargs)
            if isinstance(result, collections.Iterable):
                if len(result) == 2:
                    experiment.add_result(result[0], data=result[1])
                elif len(result) == 3:
                    experiment.add_result(result[0],
                                          data=result[1],
                                          attachment=result[2])
            else:
                experiment.add_result(result)
        __FUNCTIONS[fn_name] = wrapper

    return experiment_decorator


def parse():
    """
    Parse arguments and execute commands registered via the
    cli/experiment decorators.
    """
    arguments = sys.argv[1:]

    # Check if asking for help
    if arguments[0] == '--help':
        if len(arguments) < 2:
            print('randopt.cli: List of registered commands:')
            for fn in __FUNCTIONS:
                print('*', fn)
            sys.exit(0)
        else:
            global __DOCS
            name = arguments[1]
            if name in __DOCS:
                print(__DOCS[name])
                sys.exit(0)
            else:
                print('randopt.cli:', name, 'is not a registered command.')
                sys.exit(-1)

    # If not, try to call the function
    global __ARGUMENTS
    if arguments[0] not in __ARGUMENTS:
        sys.exit('randopt.cli:', arguments[0], 'is not a registered command.')

    func_def = __ARGUMENTS[arguments[0]]
    parser = argparse.ArgumentParser('Randopt\'s custom argument parser')
    for arg in func_def:
        if isinstance(func_def[arg], numbers.Number):
            arg_type = type(func_def[arg])
        else:
            arg_type = str
        parser.add_argument('--' + arg,
                            type=arg_type,
                            default=func_def[arg],
                            required=False)

    parsed = parser.parse_args(arguments[1:])
    function = __FUNCTIONS[arguments[0]]
    function(**vars(parsed))
