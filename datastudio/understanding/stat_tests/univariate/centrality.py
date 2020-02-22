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
from scipy.stats import ttest_1samp, median_test, zscore
from tabulate import tabulate

from datastudio.understanding.stat_tests.interface import AbstractStatisticalTest
# =========================================================================== #
#                           Centrality Tests                                  #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                            One Sample t-test                                #
# --------------------------------------------------------------------------- #
class TTestOne(AbstractStatisticalTest):
    """Performs the One Sample t-test."""

    def __init__(self):
        self._t = 0
        self._p = 0        

    def fit(self, a, popmean, axis=0):        
         self._t, self._p = ttest_1samp(a, popmean, axis)

    def get_result(self):
        return (self._t, self._p)

    @property
    def ttestone(self):
        return self._t

    @property
    def p_value(self):
        return self._p

    def print(self):
        result = {'t-statistic': [self._t], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))

# --------------------------------------------------------------------------- #
#                            One Sample Median Test                           #
# --------------------------------------------------------------------------- #
class MedianTest(AbstractStatisticalTest):
    """Performs the One Sample Median Test."""

    def __init__(self):
        self._X2 = 0
        self._p = 0        
        self._m = 0
        self._ctable = 0

    def fit(self,*args, **kwargs):        
         self._X2, self._p, self._m, self._ctable = median_test(*args, **kwargs)

    def get_result(self):
        return (self._X2, self._p)

    @property
    def median_test(self):
        return self._X2

    @property
    def p_value(self):
        return self._p

    @property
    def grand_mean(self):
        return self._m

    @property
    def contingency_table(self):
        return self._ctable        

    def print(self):
        result = {'X^2 statistic': [self._X2], 'p-value': [self._p],
                  'Grand Median': [self._m], 'Contingency Table': self._ctable}
        print(tabulate(result, headers='keys'))

# --------------------------------------------------------------------------- #
#                                  Z Score                                    #
# --------------------------------------------------------------------------- #
class ZScore(AbstractStatisticalTest):
    """Compute the z score.
    
    Compute the z score of each value in the sample, relative to the sample 
    mean and standard deviation.

    Parameters
    ----------
    a : array_like
        An array like object containing the sample data.

    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over 
        the whole array a.

    ddof ; int, optional
        Degrees of freedom correction in the calculation of the standard deviation. 
        Default is 0.

    nan_policy : {‘propagate’, ‘raise’, ‘omit’}, optional
        Defines how to handle when input contains nan. ‘propagate’ returns nan,
        ‘raise’ throws an error, ‘omit’ performs the calculations ignoring nan 
        values. Default is ‘propagate’.

    Returns
    -------
    zscore : array_like
        The z-scores, standardized by mean and standard deviation of input array a.

    """

    def __init__(self):
        self._z = 0

    def fit(self,a, axis=0, ddof=0, nan_policy='propagate'):        
         self._z = zscore(a, axis=axis, ddof=ddof)

    def get_result(self):
        return self._z

    def print(self):
        result = {'Z Score': [self._z]}
        print(tabulate(result, headers='keys'))

