#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : association.py                                                    #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 22nd 2020, 5:49:27 am                    #
# Last Modified : Saturday, February 22nd 2020, 5:49:27 am                    #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #

"""Module statistical tests of association between 2 variables. 

Association Tests
-----------------
The following tests of association are supported:

    * Chi-Squared Test
    * Fisher's Exact Test
    * One-way ANOVA Test
    * Kruskal Wallis Test
    * Pearsons Correlation
    * Spearmans R Correlation
    * Analysis of Covariance
    * Canonical Correlation

Centrality
----------

    * One-Sample t-test
    * One-Sample Median Test

Compare Groups
--------------

        * Paired t-test
        * 2 Independent t-tests
        * Wilcoxon-Mann Whitney Test
        * Wilcoxon Signed Rank Test
        * One-way Repeated ANOVA Tests
        * Friedman Test
        * Factorial Anova
        * Binomial Test
        * McNemar Test

Data Reduction
--------------

        * Factor Analysis

Predictive Analytics
--------------------

    * Simple Linear Regression
    * Multiple Linear Regression
    * Multiple Logistic Regression
    * Multivariate Multiple Linear Regression
    * Discriminant Analysis
    * Factorial Logistic Regression
    * Ordered Logistic Regression
    * Repeated Measures Logistic Regression

Note: This package makes liberal use of three statistical software packages.

    * SciPy : A Python-based ecosystem for mathematics, science and engineering.
    * Statsmodels : Statistical models, hypothesis tests and data exploration 
    * scikit-learn : A machine learning platform for Python.

Each of the classes above comply with an Abstract Base Class which defines
the interface for all test classes. 

"""

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import CCA
from tabulate import tabulate

from datastudio.understanding.stat_tests.interface import AbstractStatisticalTest

# =========================================================================== #
#                           Association Tests                                 #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                     Canonical Correlation Analysis                          #
# --------------------------------------------------------------------------- #
class CCA(AbstractStatisticalTest):
    """Performs a canonical correlation analysis."""

    def __init__(self, n_components=2, scale=True, max_iter=500, 
            tol=1e-06, copy=True):
        self._X_scores = 0
        self._Y_scores = 0
        self._cca = CCA(n_components, scale, max_iter, tol,copy)

    def fit(self, X, y):         
        self._cca.fit(X, y)        
        self._X_scores, self._Y_scores = self._cca.transform(X,y)

    def get_result(self):
        return self._X_scores, self._Y_scores

    @property
    def cca(self):
        return self._X_scores, self._Y_scores

    def print(self):        
        print(tabulate(self._X_scores, self._Y_scores))          

# --------------------------------------------------------------------------- #
#                            Covariance                                       #
# --------------------------------------------------------------------------- #
class Covariance(AbstractStatisticalTest):
    """Performs an estimate of a covariance matrix."""

    def __init__(self):
        self._cov = None           

    def fit(self, m, y=None, rowvar=True, bias=False, ddof=None, 
            fweights=None, aweights=None):        
         self._cov = np.cov(m, y=y, rowvar=rowvar, bias=bias, ddof=ddof, 
            fweights=fweights, aweights=aweights)

    def get_result(self):
        return self._cov

    @property
    def cov(self):
        return self._cov

    def print(self):        
        print(tabulate(self._cov))            