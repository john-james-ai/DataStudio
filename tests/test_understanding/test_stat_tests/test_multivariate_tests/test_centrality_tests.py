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
# Created       : Saturday, February 22nd 2020, 6:06:02 am                    #
# Last Modified : Saturday, February 22nd 2020, 6:06:02 am                    #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Unit statistical tests."""
import numpy as np
import pandas as pd
import pytest
from pytest import mark
import time

from datastudio.understanding.stat_tests.multivariate.centrality import *

class MultiVariateCentralityTests:
  
    @mark.multivariate
    @mark.centrality
    def test_anova_one(self, get_arrays):
        print("\n\nMultivariate Centrality Tests")
        print("-"*40)
        print("\n\nOne-Way ANOVA Tests")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = AnovaOne()
        test.fit(a1,a2)
        f, p = test.get_result()
        test.print()                

    @mark.multivariate
    @mark.centrality
    def test_kruskal(self, get_arrays):
        print("\n\nKruskal Wallis Tests")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = Kruskal()
        test.fit(a1,a2)
        h, p = test.get_result()
        test.print()             

