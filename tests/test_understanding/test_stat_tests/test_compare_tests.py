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

from datastudio.understanding.stat_tests.compare import Binomial

class CompareTests:
  
    @mark.compare
    def test_binomial(self, get_arrays):
        print("\n\nCompare Group Tests")
        print("="*40)
        print("\n\nBinomial Test")
        print("-"*40)
        a1, a2, a3, a4 = get_arrays        
        test = Binomial()
        test.fit(3,5)
        p = test.get_result()
        test.print()
             