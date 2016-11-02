#!/usr/bin/env python

import os
from distutils.core import setup
from setuptools import (
    setup as install,
    find_packages,
)

VERSION = '0.0.2'

install(
    name='randopt',
    version=VERSION,
    description="Random Search Optimization",
    long_description=open('README.md').read(),
    author='Cyrus Jia, Noel Trivedi, Seb Arnold',
    author_email='smr.arnold@gmail.com',
    license='License :: OSI Approved :: Apache Software License',
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        'Tools',
    ],
    scripts=[
        'bin/roviz.py'
      ]
)
