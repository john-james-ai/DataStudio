#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : tests.py                                                          #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Thursday, February 20th 2020, 12:28:39 am                   #
# Last Modified : Thursday, February 20th 2020, 12:28:40 am                   #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Module defines the suite of statistical tests provided in DataStudio.

This package supports 32 statistical tests, organized around various facets of 
statistical inference. The classes fall broadly into five groups:

    1. Tests of Association
    2. Tests of Central Tendency  
    3. Tests of Dispersion
    4. Tests between Groups
    5. Tests of Assumptions  
    6. Predictive Analytics.

The classes are hereby listed below by category.

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
from scipy.stats import ttest_ind
from tabulate import tabulate

from datastudio.understanding.stat_tests.interface import AbstractStatisticalTest
# =========================================================================== #
#                           Compare Group Tests                               #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                         2 Independent T-Test                                #
# --------------------------------------------------------------------------- #
class TTestInd(AbstractStatisticalTest):
    """Calculate the T-test for the means of two independent samples of scores.

    This is a two-sided test for the null hypothesis that 2 independent samples 
    have identical average (expected) values. This test assumes that the populations 
    have identical variances by default.

    Attributes
    ----------
    statistic : float or array
        The calculated t-statistic.

    pvalue: float or array
        The two-tailed p-value.   
    
    """

    def __init__(self):        
        super(TTestInd, self).__init__()        

    def fit(self, a, b, axis=0, equal_var=True, nan_policy='propagate'):        
        """Calculate the T-test for the means of two independent samples of scores.

        Parameters
        ----------
        a, b : array_like
            The arrays must have the same shape, except in the dimension corresponding to axis (the first, by default).

        axis " int or None, optional
            Axis along which to compute test. If None, compute over the whole arrays, a, and b.

        equal_var : bool, optional
            If True (default), perform a standard independent 2 sample test that assumes equal population variances [1]. If False, perform Welch’s t-test, which does not assume equal population variance [2].

        nan_policy : {‘propagate’, ‘raise’, ‘omit’}, optional
            Defines how to handle when input contains nan. The following options are available (default is ‘propagate’):
            - ‘propagate’: returns nan
            - ‘raise’: throws an error
            - ‘omit’: performs the calculations ignoring nan values       
        
        """        
        self._statistic, self._p = ttest_ind(a,b, axis=axis, equal_var=equal_var)

    def get_result(self):
        return self._statistic, self._p

    @property
    def statistic(self):
        return self._statistic

    @property
    def p_value(self):
        return self._p

    def print(self):
        result = {'t-statistic': [self._statistic], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))

