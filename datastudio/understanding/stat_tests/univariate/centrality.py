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
    """Calculates the T-test for the mean of ONE group of scores.
    
    Attributes
    ----------

    """

    def __init__(self):
        self._t = 0
        self._p = 0        

    def fit(self, a, popmean, axis=0):        
        """Calculates the T-test for the mean of ONE group of scores.
        
        Parameters
        ----------
        a : array_like
            sample observation
        popmean : float or array_like
            expected value in null hypothesis, if array_like than 
            it must have the same shape as a excluding the axis dimension
        axis : int or None, optional
            Axis along which to compute test. If None, compute over the whole array a.
        
        """
        self._t, self._p = ttest_1samp(a, popmean, axis)

    def print(self):
        result = {'t-statistic': [self._t], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))

# --------------------------------------------------------------------------- #
#                            One Sample Median Test                           #
# --------------------------------------------------------------------------- #
class MedianTest(AbstractStatisticalTest):
    """Perform a Mood’s median test.

    Test that two or more samples come from populations with the same median.

    Let n = len(args) be the number of samples. The “grand median” of all the 
    data is computed, and a contingency table is formed by classifying the 
    values in each sample as being above or below the grand median. The 
    contingency table, along with correction and lambda_, are passed to 
    scipy.stats.chi2_contingency to compute the test statistic and p-value.

    Attributes
    ----------
    statistic : float
        The test statistic. The statistic that is returned is determined by 
        lambda_. The default is Pearson’s chi-squared statistic.
    p_value : float
        The p-value of the test.
    grand_median : float
        The grand median.
    contingency_table : ndarray
        The contingency table. The shape of the table is (2, n), where 
        n is the number of samples. The first row holds the counts of 
        the values above the grand median, and the second row holds the 
        counts of the values below the grand median. The table allows 
        further analysis with, for example, scipy.stats.chi2_contingency, 
        or with scipy.stats.fisher_exact if there are two samples, without 
        having to recompute the table. If nan_policy is “propagate” and there 
        are nans in the input, the return value for table is None.
    """

    def __init__(self):
        super(MedianTest, self).__init__()   
        self._m = 0
        self._ctable = 0

    def fit(self,*args, **kwargs):   
        """Perform a Mood’s median test.

        Parameters
        ----------
        sample1, sample2, … : array_like
            The set of samples. There must be at least two samples. Each 
            sample must be a one-dimensional sequence containing at least 
            one value. The samples are not required to have the same length.
        ties : str, optional
            Determines how values equal to the grand median are classified 
            in the contingency table. The string must be one of:
            "below":
                Values equal to the grand median are counted as "below".
            "above":
                Values equal to the grand median are counted as "above".
            "ignore":
                Values equal to the grand median are not counted.
            The default is “below”.
        correction : bool, optional
            If True, and there are just two samples, apply Yates’ correction for 
            continuity when computing the test statistic associated with the 
            contingency table. Default is True.
        lambda_ : float or str, optional
            By default, the statistic computed in this test is Pearson’s 
            chi-squared statistic. lambda_ allows a statistic from the 
            Cressie-Read power divergence family to be used instead. 
            See power_divergence for details. Default is 1 
            (Pearson’s chi-squared statistic).
        nan_policy : {‘propagate’, ‘raise’, ‘omit’}, optional
            Defines how to handle when input contains nan. ‘propagate’ returns 
            nan, ‘raise’ throws an error, ‘omit’ performs the calculations ignoring 
            nan values. Default is ‘propagate’.        
        """             
        self._statistic, self._p, self._m, self._ctable = median_test(*args, **kwargs)

    def get_result(self):
        """Returns results of a Mood’s median test.

        Returns
        ----------
        stat : float
            The test statistic. The statistic that is returned is determined by 
            lambda_. The default is Pearson’s chi-squared statistic.
        p : float
            The p-value of the test.
        m : float
            The grand median.
        table : ndarray
            The contingency table. The shape of the table is (2, n), where 
            n is the number of samples. The first row holds the counts of 
            the values above the grand median, and the second row holds the 
            counts of the values below the grand median. The table allows 
            further analysis with, for example, scipy.stats.chi2_contingency, 
            or with scipy.stats.fisher_exact if there are two samples, without 
            having to recompute the table. If nan_policy is “propagate” and there 
            are nans in the input, the return value for table is None.
        """            
        return self._statistic, self._p, self._m, self._ctable

    @property
    def grand_median(self):
        return self._m

    @property
    def contingency_table(self):
        return self._ctable        

    def print(self):
        result = {'Test Statistic': [self._statistic], 'p-value': [self._p],
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

