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
# Created       : Saturday, February 22nd 2020, 6:00:45 am                    #
# Last Modified : Saturday, February 22nd 2020, 6:00:45 am                    #
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

from datastudio.understanding.stat_tests.bivariate.centrality import *
class BivariateCentralityTests:
  
    @mark.bivariate
    @mark.centrality
    def test_ttestind(self, get_arrays):
        print("\n\nBivariate Centrality Tests")
        print("-"*40)
        print("\n\nIndependent t-Tests")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = TTestInd()
        test.fit(a1, a5)
        t, p = test.get_result()
        test.print()      