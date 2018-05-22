#!/usr/bin/env python

import random

# Fork Python's RNG and seed with a truly random number
if 'RANDOP_INIT' not in globals():
    RANDOPT_RNG = random.Random()
    sys_seed = random.SystemRandom().randint(0, 1e10)
    RANDOPT_RNG.seed(sys_seed)
    RANDOPT_INIT = True

from .experiment import Experiment, HyperBand, Evolutionary, GridSearch, SummaryList
from .samplers import *
from .command import cli, experiment, parse
