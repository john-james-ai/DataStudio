#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : test_distribution_tests.py                                        #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 22nd 2020, 5:59:25 am                    #
# Last Modified : Saturday, February 22nd 2020, 5:59:26 am                    #
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

from datastudio.understanding.stat_tests.univariate.distribution import *
class UnivariateDistributionTests:
  
    @mark.univariate
    @mark.distribution
    def test_binomial(self, get_arrays):
        print("\n\nUnivariate Distribution Tests")
        print("="*40)
        print("\n\nBinomial Test")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = Binomial()
        test.fit(3,5)
        p = test.get_result()
        test.print()
             

    @mark.univariate
    @mark.distribution
    def test_kolmogorov_smirnov_test(self, get_arrays):
        print("\n\nKolmogorov-Smirnov Test")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = KolmogorovSmirnov()
        test.fit(a1)
        ks, p = test.get_result()
        test.print()                      

    @mark.univariate
    @mark.distribution
    def test_shapiro_wilk_test(self, get_arrays):
        print("\n\nShapiro-Wilk Test")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = Shapiro()
        test.fit(a1)
        w, p = test.get_result()
        test.print()                       

    @mark.univariate
    @mark.distribution
    def test_anderson_darling_test(self, get_arrays):
        print("\n\nAnderson-Darling Test")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = Anderson()
        test.fit(a1)
        w, p = test.get_result()
        print(test.p_value)
        test.print()             