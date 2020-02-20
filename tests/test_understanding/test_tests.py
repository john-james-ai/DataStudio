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
"""Unit statistical tests."""
import numpy as np
import pandas as pd
import pytest
from pytest import mark
import time

from datastudio.understanding.tests import ChiSquare

class AssociationTests:
  
    @mark.stats
    def test_chisquare(self, get_arrays):
        print("\n\nAssociation Tests")
        print("-"*40)
        a1, a2, a3 = get_arrays        
        test = ChiSquare()
        test.fit(a1, axis=0)
        X2, p = test.get_result()
        test.print()
        assert isinstance(X2, float), "Chisquare result not right shape"
        assert isinstance(p, float), "p-value wacked."     
        test.fit(a2, axis=0)
        X2, p = test.get_result()
        test.print()
        test.fit(a3, axis=0)
        X2, p = test.get_result()
        test.print()        
        