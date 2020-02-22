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

from datastudio.understanding.stat_tests.bivariate.association import *


class BivariateAssociationTests:
  
    @mark.bivariate
    @mark.association
    def test_fisher_exact(self, get_arrays):
        print("\n\nBivariate Association Tests")
        print("="*40)
        print("\n\nFisher Exact Tests")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = FisherExact()
        test.fit(a4)
        odds, p = test.get_result()
        test.print()        

    @mark.bivariate
    @mark.association
    def test_pearsonr(self, get_arrays):
        print("\n\nPearsonR Correlation Tests")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = PearsonR()
        test.fit(a1,a2)
        h, p = test.get_result()
        test.print()          

    @mark.bivariate
    @mark.association
    def test_spearmanr(self, get_arrays):
        print("\n\nSpearmanR Correlation Tests")
        print("-"*40)
        a1, a2, a3, a4, a5 = get_arrays        
        test = SpearmanR()
        test.fit(a1,a2)
        h, p = test.get_result()
        test.print()              
