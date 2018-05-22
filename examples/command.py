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


if __name__ == '__main__':
    ro.parse()
