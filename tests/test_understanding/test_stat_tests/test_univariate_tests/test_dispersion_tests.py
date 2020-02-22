#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : test_dispersion_tests.py                                          #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 22nd 2020, 5:59:54 am                    #
# Last Modified : Saturday, February 22nd 2020, 5:59:54 am                    #
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

from datastudio.understanding.stat_tests.univariate.dispersion import *
class UnivariateDispersionTests:
  
    @mark.univariate
    @mark.dispersion
    def test_skew_test(self, get_arrays):
        print("\n\nUnivariate Dispersion Tests")
        print("="*40)        
        print("\nSkew Test")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = Skew()
        test.fit(a3)
        skew = test.get_result()
        test.print()        

    @mark.univariate
    @mark.dispersion
    def test_kurtosis_test(self, get_arrays):
        print("\nKurtosis Test")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = Kurtosis()
        test.fit(a1)
        kurtosis, z, p = test.get_result()
        test.print()        
