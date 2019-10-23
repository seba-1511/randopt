#!/usr/bin/env python3

"""Various utilities."""

import randopt as ro


def dict_to_constants(dictionary):
    return {k: ro.Constant(dictionary[k]) for k in dictionary}


def dict_to_string(dictionary):
    result = ''
    for key in sorted(dictionary.keys()):
        result += key + str(dictionary[key]) + '-'
    return result[:-1]
