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
    """Calculates a Pearson correlation coefficient and the p-value 
    for testing non-correlation.

    The Pearson correlation coefficient measures the linear relationship 
    between two datasets. Strictly speaking, Pearson’s correlation requires 
    that each dataset be normally distributed. Like other correlation 
    coefficients, this one varies between -1 and +1 with 0 implying 
    no correlation. Correlations of -1 or +1 imply an exact linear 
    relationship. Positive correlations imply that as x increases, so does y. 
    Negative correlations imply that as x increases, y decreases.

    The p-value roughly indicates the probability of an uncorrelated 
    system producing datasets that have a Pearson correlation at least 
    as extreme as the one computed from these datasets. The p-values 
    are not entirely reliable but are probably reasonable for datasets 
    larger than 500 or so.
    
    Attributes
    ----------
    R : Pearsons correlation coefficient
    p : 2-tailed p-value
    
    """

    def __init__(self):
        super(PearsonR, self).__init__()      

    def fit(self,X, Y):    
        """Calculates a Pearson correlation coefficient and the p-value 
        for testing non-correlation.

        Parameters
        ----------
        x : (N,) array_like
            Input
        y : (N,) array_like
            Input
        """
    
        self._statistic, self._p = pearsonr(X, Y)

    def get_result(self):
        """Returns the Pearson's correlation coefficient and 2-tailed p-value.
        
        Returns
        -------
        R : Pearsons correlation coefficient
        p : 2-tailed p-value

        """
        return super(PearsonR, self).get_result()

    def print(self):
        result = {"Pearson's Correlation Coefficient": [self._r], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))             

# --------------------------------------------------------------------------- #
#                         Spearman's Correlation Test                         #
# --------------------------------------------------------------------------- #
class SpearmanR(AbstractStatisticalTest):
    """Calculate a Spearman correlation coefficient with associated p-value.

    The Spearman rank-order correlation coefficient is a nonparametric measure 
    of the monotonicity of the relationship between two datasets. Unlike 
    the Pearson correlation, the Spearman correlation does not assume 
    that both datasets are normally distributed. Like other correlation 
    coefficients, this one varies between -1 and +1 with 0 implying no 
    correlation. Correlations of -1 or +1 imply an exact monotonic 
    relationship. Positive correlations imply that as x increases, so 
    does y. Negative correlations imply that as x increases, y decreases.

    The p-value roughly indicates the probability of an uncorrelated system 
    producing datasets that have a Spearman correlation at least as extreme 
    as the one computed from these datasets. The p-values are not entirely 
    reliable but are probably reasonable for datasets larger than 500 or so.
    
    Attributes
    ----------
    correlation : float or ndarray (2-D square)
        Spearman correlation matrix or correlation coefficient 
        (if only 2 variables are given as parameters. Correlation matrix 
        is square with length equal to total number of variables 
        (columns or rows) in a and b combined.
    pvalue: float
        The two-sided p-value for a hypothesis test whose null hypothesis 
        is that two sets of data are uncorrelated, has same dimension as rho.

    """

    def __init__(self):
        super(SpearmanR, self).__init__()      

    def fit(self,X, Y):    
        """Calculates a Spearman correlation coefficient and the p-value.

        Parameters
        ----------
        a, b : 1D or 2D array_like, b is optional
            One or two 1-D or 2-D arrays containing multiple variables and 
            observations. When these are 1-D, each represents a vector of 
            observations of a single variable. For the behavior in the 2-D 
            case, see under axis, below. Both arrays need to have the same 
            length in the axis dimension.
        axis : int or None, optional
            If axis=0 (default), then each column represents a variable, with 
            observations in the rows. If axis=1, the relationship is 
            transposed: each row represents a variable, while the columns 
            contain observations. If axis=None, then both arrays will be raveled.

        nan_policy : {‘propagate’, ‘raise’, ‘omit’}, optional
            Defines how to handle when input contains nan. The following options 
            are available (default is ‘propagate’):
            - ‘propagate’: returns nan
            - ‘raise’: throws an error
            - ‘omit’: performs the calculations ignoring nan values
        """
    
        self._statistic, self._p = spearmanr(X, Y)

    def get_result(self):
        """Returns the Pearson's correlation coefficient and 2-tailed p-value.
        
        Returns
        -------
        correlation : float or ndarray (2-D square)
            Spearman correlation matrix or correlation coefficient 
            (if only 2 variables are given as parameters. Correlation matrix 
            is square with length equal to total number of variables 
            (columns or rows) in a and b combined.
        pvalue: float
            The two-sided p-value for a hypothesis test whose null hypothesis 
            is that two sets of data are uncorrelated, has same dimension as rho.

        """
        return super(SpearmanR, self).get_result()

    def print(self):
        result = {"Spearman's Correlation Coefficient": [self._r], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))             

                  

    