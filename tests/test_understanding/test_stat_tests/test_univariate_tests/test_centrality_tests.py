#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : test_centrality_tests.py                                          #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 22nd 2020, 5:59:38 am                    #
# Last Modified : Saturday, February 22nd 2020, 5:59:38 am                    #
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

from datastudio.understanding.stat_tests.univariate.centrality import *
class UnivariateCentralityTests:
  
    @mark.univariate
    @mark.centrality
    def test_ttestone(self, get_arrays):
        print("\n\nUnivariate Centrality Tests")
        print("="*40)
        print("\n\nOne Sample t-Tests")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = TTestOne()
        test.fit(a1, popmean=10)
        t, p = test.get_result()
        test.print()
        
    @mark.univariate
    @mark.centrality
    def test_median_test(self, get_arrays):
        print("\n\nMedian Test")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = MedianTest()
        test.fit(a1,a2)
        t, p = test.get_result()
        test.print()    

    @mark.univariate
    @mark.centrality
    def test_zscore_test(self, get_arrays):
        print("\n\nZ Score Test")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = ZScore()
        test.fit(a1)
        z = test.get_result()
        test.print()       
       

  