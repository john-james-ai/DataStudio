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
from scipy.stats import chisquare, binom_test
from statsmodels.stats.diagnostic import lilliefors
from tabulate import tabulate

from datastudio.understanding.stat_tests.interface import AbstractStatisticalTest
# =========================================================================== #
#                           Distribution Tests                                #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                            Binomial Test                                    #
# --------------------------------------------------------------------------- #
class Binomial(AbstractStatisticalTest):
    """Performs the Binomial Test."""

    def __init__(self):        
        super(Binomial, self).__init__()        

    def fit(self, x, n=None, p=0.5):        
         self._p = binom_test(x,n,p)

    def get_result(self):
        return self._p
    @property
    def p_value(self):
        return self._p

    def print(self):
        result = {'p-value': [self._p]}
        print(tabulate(result, headers='keys'))

# --------------------------------------------------------------------------- #
#                    Chi-Square Goodness-of-Fit Test                          #
# --------------------------------------------------------------------------- #
class ChiSquareGoF(AbstractStatisticalTest):
    """Performs the Chi-Squared Goodness of fit test.
    
    The chi-square test tests the null hypothesis that the categorical 
    data has the given frequencies.

    Attributes
    ----------
    statistic : float or ndarray
        The chi-squared test statistic. The value is a float if axis is 
        None or f_obs and f_exp are 1-D.
    p_value : float or ndarray
        The p-value of the test. The value is a float if ddof and   
        the return value chisq are scalars.
    """

    def __init__(self):
        super(ChiSquareGoF, self).__init__()

    @property
    def statistic(self):
        return self._statistic

    @property
    def p_value(self):
        return self._p

    def fit(self, X, exp=None, ddof=0, axis=0):   
        """Performs the statistical test.

        Parameters
        ----------
        f_obs: array_like
            Observed frequencies in each category.
        f_exp: array_like, optional
            Expected frequencies in each category. By default the 
            categories are assumed to be equally likely.
        ddof : int, optional
            “Delta degrees of freedom”: adjustment to the degrees of freedom 
            for the p-value. The p-value is computed using a chi-squared distribution 
            with k - 1 - ddof degrees of freedom, where k is the number of observed 
            frequencies. The default value of ddof is 0.
        axis: int or None, optional
            The axis of the broadcast result of f_obs and f_exp along which 
            to apply the test. If axis is None, all values in f_obs are treated as a 
            single data set. Default is 0.

        """
         
        self._statistic, self._p = chisquare(X,f_exp=exp, ddof=ddof, axis=axis)


    def print(self):
        result = {'Chi-Square': [self._statistic], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))

# --------------------------------------------------------------------------- #
#                        Kolmogorov-Smirnov Test                              #
# --------------------------------------------------------------------------- #
class KolmogorovSmirnov(AbstractStatisticalTest):
    """Test assumed normal or exponential distribution using Lilliefors’ test.
    
    Lilliefors’ test is a Kolmogorov-Smirnov test with estimated parameters.

    Attributes
    ----------
    ksstat : float
        Kolmogorov-Smirnov test statistic with estimated mean and variance.

    pvalue : float
        If the pvalue is lower than some threshold, e.g. 0.05, then we can 
        reject the Null hypothesis that the sample comes from a 
        normal distribution.  

    """

    def __init__(self):
        super(KolmogorovSmirnov, self).__init__()

    @property
    def statistic(self):
        return self._statistic

    @property
    def p_value(self):
        return self._p        

    def fit(self, x, dist='norm', pvalmethod='table'):   
        """Performs the statistical test.

        Parameters
        ----------
        x : array_like, 1d
            Data to test.

        dist : {‘norm’, ‘exp’}, optional
            The assumed distribution.

        pvalmethod : {‘approx’, ‘table’}, optional
            The method used to compute the p-value of the test statistic. 
            In general, ‘table’ is preferred and makes use of a very large 
            simulation. ‘approx’ is only valid for normality. if dist = ‘exp’ 
            table is always used. ‘approx’ uses the approximation formula of 
            Dalal and Wilkinson, valid for pvalues < 0.1. If the pvalue is 
            larger than 0.1, then the result of table is returned.

        """
         
        self._statistic, self._p = lilliefors(x, dist=dist, pvalmethod=pvalmethod)


    def print(self):
        result = {'KS Statistic': [self._statistic], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))        