<p align="center"><img src="./assets/images/logo.png" /></p>

--------------------------------------------------------------------------------

[![Build Status](https://travis-ci.org/seba-1511/randopt.svg?branch=master)](https://travis-ci.org/seba-1511/randopt)
[![PyPI version](https://badge.fury.io/py/randopt.svg)](https://badge.fury.io/py/randopt)

randopt is a Python package for machine learning experiment management, hyper-parameter optimization, and results visualization. Some of its features include:

* result logging and management,
* human-readable format,
* support for parallelism / distributed / asynchronous experiments,
* command-line and programmatic API,
* shareable, flexible Web visualization,
* automatic hyper-parameter search, and
* pure Python - no dependencies !


# Installation

```shell
pip install randopt
```

# Usage

```python
import randopt as ro

def loss(x):
    return x**2

e = ro.Experiment('myexp', {
        'alpha': ro.Gaussian(mean=0.0, std=1.0, dtype='float'),
    })

# Sampling parameters
for i in xrange(100):
    e.sample('alpha')
    res = loss(e.alpha)
    print('Result: ', res)
    e.add_result(res)

# Manually setting parameters
e.alpha = 0.00001
res = loss(e.alpha)
e.add_result(res)

# Search over all experiments results, including ones from previous runs
opt = e.minimum()
print('Best result: ', opt.result, ' with params: ', opt.params)
```

## Results Visualization

Once you obtained some results, run `roviz.py path/to/experiment/folder` to visualize them in your web browser.

For more info on visualization and `roviz.py`, refer to the [Visualizing Results]() tutorial.

## Hyper-Parameter Optimization

To generate results and search for good hyper-parameters you can either user `ropt.py` or write your own optimizaiton script using the [Evolutionary](https://github.com/seba-1511/randopt/wiki/evolutionary) and [GridSearch](https://github.com/seba-1511/randopt/wiki/grid_search) classes.

For more info on hyper-parameter optimization, refer to the [Optimizing Hyperparams]() tutorial.


# Documentation

For more examples, tutorials, and documentation refer to the [wiki](https://github.com/seba-1511/randopt/wiki).


# Contributing

To contribute to Randopt, it is recommended to follow the [contribution guidelines](CONTRIBUTING.md).

### Acknowledgements
Randopt is maintained by [Séb Arnold](http://seba1511.com), with numerous contributions from the following persons.

* Noel Trivedi
* Cyrus Jia
* Daler Asrorov

# License

Randopt is released under the Apache 2 License. For more information, refer to the [LICENSE file](LICENSE.txt).

I would love to hear how your use Randopt. Feel free to [drop me a line](http://seba1511.com) !
