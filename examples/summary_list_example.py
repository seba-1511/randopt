#!/usr/bin/env python3

import random
import randopt as ro


if __name__ == '__main__':
    random.seed(1234)
    # Create random JSON Summaries
    exp = ro.Experiment('summary_list')
    for i in range(15):
        exp.add_result(random.random(), data={
            'alpha': [random.random() for _ in range(100)],
            'beta': [random.random() for _ in range(1000)],
            'gamma': random.random(),
        })

    # Fetch some results
    results = exp.top(10)

    # Play with the API
    print(len(results))
    assert len(results) == results.count()
    print('slice mean', results[0:3].mean())
    print('mean of top half:',
          results.filter(lambda r: r.result > results.mean()).mean())

    # Special functions on scalars
    print('min(gamma):', results.min('gamma'))
    print('max(gamma):', results.max('gamma'))
    print('mean(gamma):', results.mean('gamma'))
    print('var(gamma):', results.variance('gamma'))
    print('std(gamma):', results.std('gamma'))
    print('median(gamma):', results.median('gamma'))

    # Special functions on lists
    print('sum(min(alpha)):', sum(results.min('alpha')))
    print('sum(max(alpha)):', sum(results.max('alpha')))
    print('sum(mean(alpha)):', sum(results.mean('alpha')))
    print('sum(var(alpha)):', sum(results.variance('alpha')))
    print('sum(std(alpha)):', sum(results.std('alpha')))
    print('sum(median(alpha)):', sum(results.median('alpha')))
