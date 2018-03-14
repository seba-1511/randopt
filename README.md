<p align="center"><img src="./assets/images/logo.png" /></p>

--------------------------------------------------------------------------------

randopt is a package for machine learning experiment management, hyper-parameter optimization, and results visualization.

[![Build Status](https://travis-ci.org/seba-1511/randopt.svg?branch=master)](https://travis-ci.org/seba-1511/randopt)
[![PyPI version](https://badge.fury.io/py/randopt.svg)](https://badge.fury.io/py/randopt)

<p align="center"><img width="60%" src="assets/images/pipeline.png" /></p>

## Install

```shell
pip install randopt
```
or clone this repo and `python setup.py develop`.

## Example
Here's a short example on how to use `randopt`.

```python
#!/usr/bin/env python

import randopt as ro

def loss(x):
    return x**2

if __name__ == '__main__':

    e = ro.Experiment('myexp', {
            'alpha': ro.Gaussian(mean=0.0, std=1.0, dtype='float'),
        })

    # Sampling parameters
    for i in xrange(100):
        e.sample('alpha')
        res = loss(e.alpha)
        print 'Result: ', res
        e.add_result(res)

    # Manually setting parameters
    e.alpha = 0.00001
    res = loss(e.alpha)
    e.add_result(res)

    # Search over all experiments results, including ones from previous runs
    opt = e.minimum()
    print 'Best result: ', opt.value, ' with params: ', opt.params
```

## Visualization

Once your experiments are run, 

`roviz.py path/to/experiment/folder`

## More Info

For more examples, tutorials, and documentation refer to the [website](http://seba-1511.github.io/randopt).

