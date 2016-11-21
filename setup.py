#!/usr/bin/env python

from setuptools import (
        setup as install,
        find_packages,
        )

VERSION = '0.1.1'

install(
        name='randopt',
        packages=['randopt'],
        version=VERSION,
        description='Random search optimization and experiment logging. Support async, fancy visualization, distributed execution.',
        author='Seb Arnold',
        author_email='smr.arnold@gmail.com',
        url = 'https://github.com/seba-1511/randopt',
        download_url = 'https://github.com/seba-1511/randopt/archive/0.1.1.zip',
        license='License :: OSI Approved :: Apache Software License',
        classifiers=[],
        scripts=[
            'bin/roviz.py',
            ]
        )
