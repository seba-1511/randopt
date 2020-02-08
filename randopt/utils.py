#!/usr/bin/env python3

"""Various utilities."""

import os
import randopt as ro


def dict_to_constants(dictionary):
    return {str(k): ro.Constant(dictionary[k]) for k in dictionary}


def dict_to_list(dictionary):
    return [str(key) + str(dictionary[key])
            for key in sorted(dictionary.keys())]


def dict_to_path(dictionary):
    return os.path.join(*dict_to_list(dictionary))


def dict_to_string(dictionary):
    return '-'.join(dict_to_list(dictionary))
