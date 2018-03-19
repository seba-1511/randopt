#!/usr/bin/env python3

import argparse
import randopt as ro


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--abcd', type=float)
    parser.add_argument('--qwer', type=float)
    parser.add_argument('--asdf', type=float)
    return parser.parse_args()


def loss(x, y, z):
    return x**2 + y**2 + z**2


if __name__ == '__main__':
    args = parse()
    exp = ro.Experiment('ropt_test', params={
        'abcd': ro.Constant(args.abcd),
        'qwer': ro.Constant(args.qwer),
        'asdf': ro.Constant(args.asdf),
    })
    exp.add_result(loss(args.abcd, args.asdf, args.qwer))
