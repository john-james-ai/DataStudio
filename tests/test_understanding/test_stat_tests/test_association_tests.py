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

from datastudio.understanding.stat_tests.association import ChiSquare, FisherExact
from datastudio.understanding.stat_tests.association import AnovaOne, Kruskal
from datastudio.understanding.stat_tests.association import PearsonR, SpearmanR
from datastudio.understanding.stat_tests.association import Covariance, CCA

class AssociationTests:
  
    @mark.association
    def test_chisquare(self, get_arrays):
        print("\n\nAssociation Tests")
        print("="*40)
        print("\n\nChi-Square Tests")
        print("-"*40)
        a1, a2, a3, a4 = get_arrays        
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
        
    @mark.association
    def test_fisher_exact(self, get_arrays):
        print("\n\nFisher Exact Tests")
        print("-"*40)
        a1, a2, a3, a4 = get_arrays        
        test = FisherExact()
        test.fit(a4)
        odds, p = test.get_result()
        test.print()        

    @mark.association
    def test_anova_one(self, get_arrays):
        print("\n\nOne-Way ANOVA Tests")
        print("-"*40)
        a1, a2, a3, a4 = get_arrays        
        test = AnovaOne()
        test.fit(a1,a2)
        f, p = test.get_result()
        test.print()                

    @mark.association
    def test_kruskal(self, get_arrays):
        print("\n\nKruskal Wallis Tests")
        print("-"*40)
        a1, a2, a3, a4 = get_arrays        
        test = Kruskal()
        test.fit(a1,a2)
        h, p = test.get_result()
        test.print()             

    @mark.association
    def test_pearsonr(self, get_arrays):
        print("\n\nPearsonR Correlation Tests")
        print("-"*40)
        a1, a2, a3, a4 = get_arrays        
        test = PearsonR()
        test.fit(a1,a2)
        h, p = test.get_result()
        test.print()          

    @mark.association
    def test_spearmanr(self, get_arrays):
        print("\n\nSpearmanR Correlation Tests")
        print("-"*40)
        a1, a2, a3, a4 = get_arrays        
        test = SpearmanR()
        test.fit(a1,a2)
        h, p = test.get_result()
        test.print()              

    @mark.association
    def test_cov(self, get_arrays):
        print("\n\nCovariaance Tests")
        print("-"*40)
        a1, a2, a3, a4 = get_arrays        
        test = Covariance()
        test.fit(a1, a2)
        cov = test.get_result()
        test.print()                 

    @mark.association
    def test_cca(self, get_X_y):
        print("\n\nCanonical Correlation Test")
        print("-"*40)
        x,y = get_X_y        
        test = Covariance()
        test.fit(x,y)
        cca = test.get_result()
        test.print()                         