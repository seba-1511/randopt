# rand_opt
Random search optimization and experiment logging. Support async, fancy visualization, distributed execution.

## Example
Here's a short example on how to use `randopt`.

```python
#!/usr/bin/env python

import randopt as ro

def loss(x):
    return x**2

if __name__ == '__main__':

    e = ro.Experiment('myexp', {
            # 'alpha': ro.Normal(low=-1.0, high=1.0, dtype='float'),
            'alpha': ro.Gaussian(mean=0.0, std=1.0, dtype='float'),
            # 'alpha': ro.Choice([0.01, 0.05, 0.1, 0.5, 0.7, 0.9], sampler=ro.Uniform()),
        })

    # Seeding will make all of your searches reproducible. (Usually not wanted)
    # e.seed(1234)

    # Randomly sampling parameters
    for i in xrange(100):
        alpha = e.sample_alpha()
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
`randopt` also supports basic HTML visualization. After running an experiment, and using the `add_result` function, the following code can create a table containing the results. The `roviz.py` script will automatically launch the webpage. However, if you wish to view the HTML file for whatever reason, it's saved as `randopt_results/expName/viz.html`.

`python randopt/roviz.py -e expName`

By default, the visualizer sorts in order of ascending result. If you wish to visualize the data in a descending order, use the following command line argument.

`python randopt/roviz.py -e expName -s max`

## TODO

Check each python file or grep `TODO:` for a complete list of todos. Here's an overview.

* Unit Tests
* Documentation
* Implement more samplers
* Bayesian optimizaiton on previously ran experiments ?
