#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : test_tests.py                                                     #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Thursday, February 20th 2020, 1:32:54 am                    #
# Last Modified : Thursday, February 20th 2020, 1:32:55 am                    #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Unit Centrality tests."""
import numpy as np
import pandas as pd
import pytest
from pytest import mark
import time

from datastudio.understanding.stat_tests.centrality import TTestOne, MedianTest

class CentralityTests:
  
    @mark.centrality
    def test_ttestone(self, get_arrays):
        print("\n\nCentrality Tests")
        print("="*40)
        print("\n\nOne Sample t-Tests")
        print("-"*40)
        a1, a2, a3, a4 = get_arrays        
        test = TTestOne()
        test.fit(a1, popmean=10)
        t, p = test.get_result()
        test.print()
        
    @mark.centrality
    def test_median_test(self, get_arrays):
        print("\n\nCentrality Tests")
        print("="*40)
        print("\n\nMedian Test")
        print("-"*40)
        a1, a2, a3, a4 = get_arrays        
        test = MedianTest()
        test.fit(a1,a2)
        t, p = test.get_result()
        test.print()        