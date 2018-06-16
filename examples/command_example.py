#!/usr/bin/env python3

import randopt as ro


@ro.cli
def test1(arg1=20, arg2='name', arg3=1.23):
    print('test1')
    print('arg1', arg1)
    print('arg2', arg2)
    print('arg3', arg3)


@ro.cli
def test2(arg1=20, arg2='name', arg3=1.23):
    """
    The docstring serves as help when using the --help flag.

    Args:
        arg1: int
        arg2: str
        arg3: float
    """
    print('test2')
    print('arg1', arg1)
    print('arg2', arg2)
    print('arg3', arg3)


@ro.experiment('only_result')
def test_experiment1(x=2, y=3):
    return x**2 + y**2


@ro.experiment('result_params')
def test_experiment2(x=2, y=3):
    return x**2 + y**2, {'additional': 'info'}


@ro.experiment('result_params_attachments')
def test_experiment3(x=2, y=3):
    return x**2 + y**2, {'additional': 'info'}, {'attach': 'this sentence.'}

@ro.cli
def test_experiment4(x=2, y=4):
    exp = ro.Experiment('params_from_def', params=ro.dict_to_params(locals()))
    exp.add_result(x**2 + y**2, data={'additional': 'as usual.'})


if __name__ == '__main__':
    ro.parse()
