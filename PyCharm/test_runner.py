#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import tests

prodTestSuite = unittest.TestSuite()
prodTestSuite.addTest(unittest.makeSuite(tests.IndTests))
runner = unittest.TextTestRunner(verbosity=2)
runner.run(prodTestSuite)
