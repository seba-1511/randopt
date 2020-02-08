#!/usr/bin/env python3

import os
import unittest
import randopt as ro


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dict_to_list(self):
        dictionary = dict(asdf=23, yxcv='vcxy', qwer=1)
        ref = ['asdf23', 'qwer1', 'yxcvvcxy']
        res = ro.dict_to_list(dictionary)
        self.assertEqual(ref, res)

    def test_dict_to_constants(self):
        dictionary = dict(asdf=23, yxcv='vcxy', qwer=1)
        res = ro.dict_to_constants(dictionary)
        self.assertTrue(isinstance(res, dict))
        for key, value in res.items():
            self.assertTrue(isinstance(key, str))
            self.assertTrue(isinstance(value, ro.Constant))

    def test_dict_to_path(self):
        dictionary = dict(asdf=23, yxcv='vcxy', qwer=1)
        res = ro.dict_to_path(dictionary)
        subs = res.split('/')
        for sub in subs:
            self.assertTrue(len(sub) < 255)
        ref = ro.dict_to_list(dictionary)
        self.assertEqual(subs, ref)

    def test_dict_to_(self):
        dictionary = dict(asdf=23, yxcv='vcxy', qwer=1)
        res = ro.dict_to_string(dictionary)
        subs = res.split('-')
        ref = ro.dict_to_list(dictionary)
        self.assertEqual(subs, ref)



if __name__ == '__main__':
    unittest.main()
