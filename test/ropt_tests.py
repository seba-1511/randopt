#!/usr/bin/env python3

import unittest
import os
import subprocess
import randopt as ro


class TestRopt(unittest.TestCase):

    def _clean_up(self):
        if 'ROPT_NSEARCH' in os.environ:
            del os.environ['ROPT_NSEARCH']
        if 'ROPT_TYPE' in os.environ:
            del os.environ['ROPT_TYPE']
        if 'ROPT_NAME' in os.environ:
            del os.environ['ROPT_NAME']
        if 'ROPT_NPROC' in os.environ:
            del os.environ['ROPT_NPROC']
        subprocess.call(['make', 'clean'])

    def setUp(self):
        self._clean_up()
        self.experiment = ro.Experiment('ropt_test')

    def tearDown(self):
        self._clean_up()
        # curr = os.path.abspath(os.path.curdir)
        # results_dir = os.path.join(curr, 'randopt_results')
        # os.remove(results_dir) TODO: Why not working ?

    def test_no_sampling(self):
        os.environ['ROPT_NSEARCH'] = '3'
        command = 'ropt.py python test/ropt_simple.py --asdf=1 --qwer=1 --abcd=1'.split(' ')
        subprocess.call(command, shell=False)
        self.assertEqual(self.experiment.count(), 3)
        result = list(self.experiment.all())[0]
        self.assertEqual(result.result, 3)
        self.assertEqual(result.asdf, 1)
        self.assertEqual(result.qwer, 1)
        self.assertEqual(result.abcd, 1)

    def test_grid_search(self):
        os.environ['ROPT_NSEARCH'] = '8'
        os.environ['ROPT_TYPE'] = 'GridSearch'
        os.environ['ROPT_NAME'] = 'ropt_test'
        command = 'ropt.py python test/ropt_simple.py --abcd=Choice([1,2]) --qwer=Choice([1,2]) --asdf=Choice([1,2])'.split(' ')
        subprocess.call(command, shell=False)
        self.assertEqual(self.experiment.count(), 8)
        self.assertEqual(self.experiment.minimum().result, 3)
        self.assertEqual(self.experiment.maximum().result, 12)
        for res in self.experiment.all_results():
            self.assertIn(res.abcd, [1, 2])
            self.assertIn(res.qwer, [1, 2])
            self.assertIn(res.asdf, [1, 2])

    def test_evolutionary(self):
        os.environ['ROPT_NSEARCH'] = '1'
        command = 'ropt.py python test/ropt_simple.py --asdf=1 --qwer=1 --abcd=1'.split(' ')
        subprocess.call(command, shell=False)
        os.environ['ROPT_NSEARCH'] = '20'
        os.environ['ROPT_TYPE'] = 'Evolutionary'
        os.environ['ROPT_NAME'] = 'ropt_test'
        command = 'ropt.py python test/ropt_simple.py --abcd=Normal(0.0,0.1) --qwer=Uniform(-0.1,0.1) --asdf=Normal(0.0,0.3)'.split(' ')
        subprocess.call(command, shell=False)
        self.assertEqual(self.experiment.count(), 21)
        self.assertLessEqual(self.experiment.minimum().result, 3)
