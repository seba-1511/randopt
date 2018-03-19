import unittest
import randopt as ro

import os #for various directory functions
import shutil #for shutil.rmtree
import json #for json.load()
import time #for time.sleep

#TODO: Test Experiment.save_state, amd Experiment.set_state

class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.expName = 'test_experiment_unit_tests'
        self.exp = ro.Experiment(self.expName, {
            'param1'  : ro.Uniform(low=0.0, high=100.0, dtype='int'),
            'param2'  : ro.Normal(mean=100, std=10, dtype='int'),
        })

    def tearDown(self):
        # remove the experiment result folder
        cwd = os.getcwd()
        randopt_folder = os.path.join(cwd, 'randopt_results')
        experiment_path = os.path.join(randopt_folder, self.expName)
        shutil.rmtree(experiment_path)

    def test_folder_creation(self):
        cwd = os.getcwd()
        randopt_folder = os.path.join(cwd, 'randopt_results')
        experiment_path = os.path.join(randopt_folder, self.expName)

        self.assertTrue(os.path.exists(experiment_path))

    def test_seeding_experiment(self):
        self.exp.seed(100)
        sampledParam = self.exp.sample('param1')

        #if properly seeded, the sampling should return 14
        expectedResult = 14

        self.assertEquals(sampledParam, expectedResult)

    def test_setting_param(self):
        desiredParam = 100
        self.exp.set('param1', desiredParam)

        self.assertEquals(self.exp.param1, desiredParam)

    def test_current(self):
        expectedParam1 = 10
        expectedParam2 = 15
        self.exp.set('param1', expectedParam1)
        self.exp.set('param2', expectedParam2)

        currentExp = self.exp.current
        self.assertEquals(currentExp['param1'], expectedParam1)
        self.assertEquals(currentExp['param2'], expectedParam2)

    def test_sample_all_params(self):
        #if properly seeded, the sampling should return 14 and 106
        self.exp.seed(100)
        expectedParam1 = 14
        expectedParam2 = 106
        currentExp = self.exp.sample_all_params()

        self.assertEquals(currentExp['param1'], expectedParam1)
        self.assertEquals(currentExp['param2'], expectedParam2)

    def test_maximum(self):
        self.exp.seed(100)
        expectedMaximum = { 'param1' : 14, 'param2' : 106}

        #Create two results
        self.exp.sample_all_params()
        self.exp.add_result(1000)
        self.exp.sample_all_params()
        self.exp.add_result(1)

        maxResult = self.exp.maximum()
        self.assertEquals(maxResult.result, 1000)
        self.assertEquals(int(maxResult.params['param1']), int(expectedMaximum['param1']))
        self.assertEquals(int(maxResult.params['param2']), int(expectedMaximum['param2']))

    def test_minimum(self):
        self.exp.seed(100)
        expectedMinimum = { 'param1' : 14, 'param2' : 106}

        #Create two results
        self.exp.sample_all_params()
        self.exp.add_result(1)
        self.exp.sample_all_params()
        self.exp.add_result(1000)

        minResult = self.exp.minimum()
        self.assertEquals(minResult.result, 1)
        self.assertEquals(int(minResult.params['param1']), int(expectedMinimum['param1']))
        self.assertEquals(int(minResult.params['param2']), int(expectedMinimum['param2']))

    def test_top_not_enough_results(self):
        self.exp.seed(100)
        #Create 5 results, and ask for the top 10 results
        #Expect to get 5 results back

        #Create 5 results
        nResults = 5
        self.exp.set('param1', 1)
        self.exp.set('param2', 1)
        self.exp.add_result(1)
        self.exp.set('param1', 2)
        self.exp.set('param2', 2)
        self.exp.add_result(2)
        self.exp.set('param1', 3)
        self.exp.set('param2', 3)
        self.exp.add_result(3)
        self.exp.set('param1', 4)
        self.exp.set('param2', 4)
        self.exp.add_result(4)
        self.exp.set('param1', 5)
        self.exp.set('param2', 5)
        self.exp.add_result(5)

        topN = self.exp.top(10)
        self.assertEquals(len(topN), nResults)

    def test_top_n(self):
        self.exp.seed(100)
        #Create 5 results
        nResults = 5
        self.exp.set('param1', 1)
        self.exp.set('param2', 1)
        self.exp.add_result(1)
        self.exp.set('param1', 2)
        self.exp.set('param2', 2)
        self.exp.add_result(2)
        self.exp.set('param1', 3)
        self.exp.set('param2', 3)
        self.exp.add_result(3)
        self.exp.set('param1', 4)
        self.exp.set('param2', 4)
        self.exp.add_result(4)
        self.exp.set('param1', 5)
        self.exp.set('param2', 5)
        self.exp.add_result(5)

        nRequested= 3
        topN = self.exp.top(nRequested)
        self.assertEquals(len(topN), nRequested)
        #the following are the expected values with the given seed
        self.assertEquals(int(topN[0]['param1']), 1)
        self.assertEquals(int(topN[0]['param2']), 1)
        self.assertEquals(int(topN[1]['param1']), 2)
        self.assertEquals(int(topN[1]['param2']), 2)
        self.assertEquals(int(topN[2]['param1']), 3)
        self.assertEquals(int(topN[2]['param2']), 3)

    def test_raise_with_param_named_result(self):
        with self.assertRaises(ValueError):
            ro.Experiment('invalid experiment', {
                    'result' : ro.Uniform(low=0.0, high=100.0, dtype='int'),
                })

    def test_add_result(self):
        self.exp.set('param1', 10)
        self.exp.set('param2', 20)
        self.exp.add_result(50)

        #grab the file in the experiment path
        cwd = os.getcwd()
        randopt_folder = os.path.join(cwd, 'randopt_results')
        experiment_path = os.path.join(randopt_folder, self.expName)
        files = os.listdir(experiment_path)

        #confirm that only 1 file was written
        self.assertEquals(len(files), 1)

        #confirm that the file was written properly
        file_path = os.path.join(experiment_path, files[0])
        with open(file_path, 'r') as f:
            writtenData = json.load(f)
            self.assertEquals(int(writtenData['param1']), 10)
            self.assertEquals(int(writtenData['param2']), 20)
            self.assertEquals(int(writtenData['result']), 50)

    def test_iter_all_results(self):
        nResults = 5
        exp_seen = []
        for i in range(nResults):
            self.exp.set('param1', i)
            self.exp.set('param2', i)
            self.exp.add_result(i)
            exp_seen.append(0)
        count = 0
        for res in self.exp.all_results():
            count += 1
            exp_seen[int(res.result)] += 1
            self.assertEquals(res.params['param1'], res.result)
            self.assertEquals(exp_seen[int(res.result)], 1)
        self.assertEquals(count, nResults)
        self.assertEquals(sum(exp_seen), nResults)
