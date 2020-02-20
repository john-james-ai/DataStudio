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
from scipy.stats import chisquare, fisher_exact, f_oneway, kruskal, pearsonr
from scipy.stats import spearmanr, ttest_1samp, median_test, binom_test
from scipy.stats import ttest_ind, mannwhitneyu, ttest_rel, wilcoxon
from scipy.stats import friedmanchisquare
from sklearn.cross_decomposition import CCA
from sklearn.decomposition import FactorAnalysis
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import discriminant_analysis
from tabulate import tabulate

# --------------------------------------------------------------------------- #
#                        AbstractStatisticalTests                             #
# --------------------------------------------------------------------------- #
class AbstractStatisticalTests(ABC):

    @abstractmethod
    def fit(self, X):
        pass

    @abstractmethod
    def get_result(self):
        pass

    @abstractmethod
    def print(self):
        pass


# =========================================================================== #
#                           Association Tests                                 #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                            Chi-Square Test                                  #
# --------------------------------------------------------------------------- #
class ChiSquare(AbstractStatisticalTests):
    """Performs the Chi-Squared Goodness of fit test.
    
    The chi-square test tests the null hypothesis that the categorical 
    data has the given frequencies.

    """

    def __init__(self):
        self._chisq = 0
        self._p = 0        

    def fit(self, X, exp=None, ddof=0, axis=0):        
         self._chisq, self._p = chisquare(X,f_exp=exp, ddof=ddof, axis=axis)

    def get_result(self):
        return (self._chisq, self._p)

    @property
    def chisquare(self):
        return self._chisq

    @property
    def p_value(self):
        return self._p

    def print(self):
        result = {'Chi-Square': [self._chisq], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))

# --------------------------------------------------------------------------- #
#                            Fisher Exact Test                                #
# --------------------------------------------------------------------------- #
class FisherExact(AbstractStatisticalTests):
    """Performs the Fisher Exact Test."""

    def __init__(self):
        self._odds = 0
        self._p = 0        

    def fit(self, X, alternative='two-sided'):        
         self._odds, self._p = fisher_exact(X, alternative=alternative)

    def get_result(self):
        return (self._odds, self._p)

    @property
    def fisher(self):
        return self._odds

    @property
    def p_value(self):
        return self._p

    def print(self):
        result = {'Odds-Ratio': [self._odds], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))        

# --------------------------------------------------------------------------- #
#                         One-Way Anova                                       #
# --------------------------------------------------------------------------- #
class AnovaOne(AbstractStatisticalTests):
    """Performs the ANOVA One-Way Test."""

    def __init__(self):
        self._statistic = 0
        self._p = 0        

    def fit(self, X, Y, alternative='two-sided'):        
         self._statistic, self._p = f_oneway(X,Y)

    def get_result(self):
        return (self._statistic, self._p)

    @property
    def anovaone(self):
        return self._statistic

    @property
    def p_value(self):
        return self._p

    def print(self):
        result = {'F-Statistic': [self._statistic], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))                

# --------------------------------------------------------------------------- #
#                         Kruskal-Wallis Test                                 #
# --------------------------------------------------------------------------- #
class Kruskal(AbstractStatisticalTests):
    """Performs the Kruskal-Wallis Test."""

    def __init__(self):
        self._statistic = 0
        self._p = 0        

    def fit(self,*args, **kwargs):        
         self._statistic, self._p = kruskal(*args, **kwargs)

    def get_result(self):
        return (self._statistic, self._p)

    @property
    def kruskal(self):
        return self._statistic

    @property
    def p_value(self):
        return self._p

    def print(self):
        result = {'H-Statistic': [self._statistic], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))          

# --------------------------------------------------------------------------- #
#                         Pearson's Correlation Test                          #
# --------------------------------------------------------------------------- #
class PearsonR(AbstractStatisticalTests):
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
class SpearmanR(AbstractStatisticalTests):
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

# --------------------------------------------------------------------------- #
#                            Covariance                                       #
# --------------------------------------------------------------------------- #
class Covariance(AbstractStatisticalTests):
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

# --------------------------------------------------------------------------- #
#                     Canonical Correlation Analysis                          #
# --------------------------------------------------------------------------- #
class CCA(AbstractStatisticalTests):
    """Performs a canonical correlation analysis."""

    def __init__(self, n_components=2, scale=True, max_iter=500, 
            tol=1e-06, copy=True):
        self._X_scores = 0
        self._Y_scores = 0
        self._cca = CCA(n_components, scale, max_iter, tol,copy)

    def fit(X, y):         
        self._cca.fit(X, y)        
        self._X_scores, self._Y_scores = self._cca.transform(X,y)

    def get_result(self):
        return self._X_scores, self._Y_scores

    @property
    def cca(self):
        return self._X_scores, self._Y_scores

    def print(self):        
        print(tabulate(self._X_scores, self._Y_scores))          