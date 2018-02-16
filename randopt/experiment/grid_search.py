#!/usr/bin/env python3

from randopt.samplers import Choice
from .experiment import Experiment


class GridSearch(Experiment):

    """
    Performs a grid-search on the parameters of a given experiment.

    Only accepts `Choice` as parameter sampler.
    """

    def __init__(self, experiment):
        # Assert that all params are Choice
        for key in experiment.params:
            msg = 'Only Choice samplers accepted'
            assert isinstance(experiment.params[key], Choice), msg

        self.__dict__.update(experiment.__dict__)
        self.experiment = experiment
        # TODO: Build index of what experiments have been ran
        self.refresh_index()

    def refresh_index(self):
        """
        Description:
            Rebuilds the index of all executed experiments.

        Arguments:
            n/a

        Returns:
            n/a

        Example:
            gs.refresh_index()
        """
        index = {}
        # Build index
        for key in self.params:
            self._append_to_index(index, key)
        self._turn_to_count(index)

        # Count results
        for e in self.experiment.all_results():
            sub_index = index
            for p in self.params:
                sub_index = sub_index[e.params[p]]
            sub_index['count'] += 1
        self.index = index

    def _turn_to_count(self, index):
        for val in index:
            if len(index[val]) == 0:
                index[val]['count'] = 0
            else:
                self._turn_to_count(index[val])

    def _append_to_index(self, index, key):
        if len(index) == 0:
            for val in self.params[key].items:
                index[val] = {}
        else:
            for sub_key in index:
                self._append_to_index(index[sub_key], key)


    def sample(self, key):
        """
        Given current params, choose the experiment that will fill the index

        TODO: This function is O(3n), but could be O(n).
        """
        values = self.params[key].items
        counts = [0 for _ in values]
        current = self.current
        for i, val in enumerate(values):
            sub_index = self.index
            for p_key in self.params:
                if key == p_key:
                    sub_index = sub_index[val]
                else:
                    sub_index = sub_index[current[p_key]]
            counts[i] = sub_index['count']
        min_count = min(counts)
        min_idx = counts.index(min_count)
        self.set(key, values[min_idx])
        return values[min_idx]

    def sample_all_params(self):
        """
        Similar to Experiment.sample_all_params()

        Returnt the first configuration that has been executed less times than
        the others.
        """
        min_count = 0
        while True:
            for solution in self._possible_solutions(self.index):
                sub_index = self.index
                for val in solution:
                    sub_index = sub_index[val]
                if sub_index['count'] <= min_count:
                    for key, val in zip(self.params, solution):
                        self.set(key, val)
                    return self.current
            min_count += 1

    def _possible_solutions(self, index=None, partial=[]):
        if index is None:
            index = self.index
        if 'count' in index and len(index) == 1:
            yield partial
        else:
            for key in index:
                yield from self._possible_solutions(index[key], partial + [key, ])

    def add_result(self, *args, **kwargs):
        """
        Same as Experiment.add_result but also refreshes the index.
        """
        super(GridSearch, self).add_result(*args, **kwargs)
        self.refresh_index()
