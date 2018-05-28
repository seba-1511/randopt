#!/usr/bin/env python

from setuptools import (
        setup,
        find_packages,
        )

VERSION = '0.2.0'

setup(
        name='randopt',
        packages=find_packages(),
        version=VERSION,
        description='Random search optimization and experiment logging. Support async, visualization, distributed execution.',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        author='Seb Arnold',
        author_email='smr.arnold@gmail.com',
        url = 'https://github.com/seba-1511/randopt',
        download_url = 'https://github.com/seba-1511/randopt/archive/' + str(VERSION) + '.zip',
        license='License :: OSI Approved :: Apache Software License',
        classifiers=[],
        scripts=[
            'bin/roviz.py',
            'bin/ropt.py',
            ]
        )
