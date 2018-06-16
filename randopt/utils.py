#!/usr/bin/env python3

"""Various utilities."""

import randopt as ro

def dict_to_params(dictionary):
    return {k: ro.Constant(dictionary[k]) for k in dictionary}
