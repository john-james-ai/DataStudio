#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : test_association_tests.py                                         #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 22nd 2020, 6:07:01 am                    #
# Last Modified : Saturday, February 22nd 2020, 6:07:01 am                    #
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

from datastudio.understanding.stat_tests.multivariate.association import *

class MultivariateAssociationTests:
  
    @mark.multivariate
    @mark.association
    def test_cov(self, get_arrays):
        print("\n\nCovariaance Tests")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = Covariance()
        test.fit(a1, a2)
        cov = test.get_result()
        test.print()                 

    @mark.multivariate
    @mark.association
    def test_cca(self, get_X_y):
        print("\n\nCanonical Correlation Test")
        print("-"*40)
        x,y = get_X_y        
        test = Covariance()
        test.fit(x,y)
        cca = test.get_result()
        test.print()                         