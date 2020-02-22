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
from scipy.stats import fisher_exact, pearsonr, spearmanr
from sklearn.cross_decomposition import CCA
from tabulate import tabulate

from datastudio.understanding.stat_tests.interface import AbstractStatisticalTest

# =========================================================================== #
#                           Association Tests                                 #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                            Fisher Exact Test                                #
# --------------------------------------------------------------------------- #
class FisherExact(AbstractStatisticalTest):
    """Performs the Fisher Exact Test.

    Fisher's exact test is a statistical test used to determine if 
    there are nonrandom associations between two categorical variables.    
    """

    def __init__(self):
        super(FisherExact, self).__init__()

    def fit(self, X, alternative='two-sided'):
        """ Performs Fisher's exact test.

        Parameters
        ----------        
        X : array_like of ints
            A 2x2 contingency table. Elements should be non-negative integers.
        alternative : {‘two-sided’, ‘less’, ‘greater’}, optional
            Defines the alternative hypothesis. The following options 
            are available (default is ‘two-sided’):
                - ‘two-sided’
                - ‘less’: one-sided
                ‘greater’: one-sided        
        """
        self._statistic, self._p = fisher_exact(X, alternative=alternative)

    def get_result(self):
        """ Returns results of statistical test.

        Returns
        -------
        oddsratio : float
            This is prior odds ratio and not a posterior estimate.
        p_value : float
            P-value, the probability of obtaining a distribution at least 
            as extreme as the one that was actually observed, assuming that 
            the null hypothesis is true.

        """
        return super(FisherExact, self).get_result()

    def print(self):
        result = {'Odds-Ratio': [self._statistic], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))        



# --------------------------------------------------------------------------- #
#                         Pearson's Correlation Test                          #
# --------------------------------------------------------------------------- #
class PearsonR(AbstractStatisticalTest):
    """Performs the Pearsons Correlation Test."""

    def __init__(self):
        self._r = 0
        self._p = 0        

    def fit(self,X, Y):        
         self._r, self._p = pearsonr(X, Y)

    def get_result(self):
        return (self._r, self._p)

    @property
    def pearsonr(self):
        return self._r

    @property
    def p_value(self):
        return self._p

    def print(self):
        result = {'R-Statistic': [self._r], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))             

# --------------------------------------------------------------------------- #
#                         Spearman's Correlation Test                         #
# --------------------------------------------------------------------------- #
class SpearmanR(AbstractStatisticalTest):
    """Performs the Spearmans Rank Order Correlation Test."""

    def __init__(self):
        self._r = 0
        self._p = 0        

    def fit(self,X, Y, axis=0, nan_policy='propagate'):        
         self._r, self._p = spearmanr(X, Y, axis=axis, nan_policy=nan_policy)

    def get_result(self):
        return (self._r, self._p)

    @property
    def spearmanr(self):
        return self._r

    @property
    def p_value(self):
        return self._p

    def print(self):
        result = {'R-Statistic': [self._r], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))              

                  

    