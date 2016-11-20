#!/usr/bin/env python

from setuptools import (
        setup as install,
        find_packages,
        )

VERSION = '0.1.0'

install(
        name='randopt',
        packages=['randopt'],
        version=VERSION,
        description='Random search optimization and experiment logging. Support async, fancy visualization, distributed execution.',
        long_description=open('README.md').read(),
        author='Seb Arnold',
        author_email='smr.arnold@gmail.com',
        url = 'https://github.com/seba-1511/randopt',
        download_url = 'https://github.com/seba-1511/randopt/archive/0.1.0.zip',
        license='License :: OSI Approved :: Apache Software License',
        classifiers=[],
        scripts=[
            'bin/roviz.py',
            ]
        )
