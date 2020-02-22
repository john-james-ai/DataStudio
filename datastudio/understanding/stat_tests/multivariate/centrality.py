#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : centrality.py                                                     #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 22nd 2020, 5:06:38 am                    #
# Last Modified : Saturday, February 22nd 2020, 5:06:38 am                    #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from scipy.stats import f_oneway, kruskal
from tabulate import tabulate

from datastudio.understanding.stat_tests.interface import AbstractStatisticalTest

# --------------------------------------------------------------------------- #
#                         Kruskal-Wallis Test                                 #
# --------------------------------------------------------------------------- #
class Kruskal(AbstractStatisticalTest):
    """Compute the Kruskal-Wallis H-test for independent samples.

    The Kruskal-Wallis H-test tests the null hypothesis that the population 
    median of all of the groups are equal. It is a non-parametric version of 
    ANOVA. The test works on 2 or more independent samples, which may have 
    different sizes. Note that rejecting the null hypothesis does not indicate 
    which of the groups differs. Post hoc comparisons between groups are 
    required to determine which groups are different.
    
    """

    def __init__(self):
        super(Kruskal, self).__init__()         

    def fit(self,*args, **kwargs):    
        """ Performs the Kruskal_Wallis H-test.

        Parameters
        ----------    
        sample1, sample2, … : array_like
            Two or more arrays with the sample measurements can be given 
            as arguments.
        nan_policy : {‘propagate’, ‘raise’, ‘omit’}, optional
            Defines how to handle when input contains nan. The following options 
            are available (default is ‘propagate’):
                 - ‘propagate’: returns nan
                 - ‘raise’: throws an error
                 - ‘omit’: performs the calculations ignoring nan values        
        """
        self._statistic, self._p = kruskal(*args, **kwargs)


    @property
    def p_value(self):
        return self._p

    def print(self):
        result = {'H-Statistic': [self._statistic], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))          

# --------------------------------------------------------------------------- #
#                         One-Way Anova                                       #
# --------------------------------------------------------------------------- #
class AnovaOne(AbstractStatisticalTest):
    """Performs the ANOVA One-Way Test.
    
    The one-way ANOVA tests the null hypothesis that two or more groups 
    have the same population mean. The test is applied to samples from 
    two or more groups, possibly with differing sizes.    
    """

    def __init__(self):
        super(AnovaOne, self).__init__()    

    def fit(self, *args):      
        """ Performs the one-way ANOVA test.

        Parameters
        ----------  
        sample1, sample2, … : array_like
            The sample measurements for each group.
        """
        self._statistic, self._p = f_oneway(*args)

    def get_result(self):
        """ Returns results of the most recent one-way ANOVA test.

        Returns
        -------
        statistic : float
            The computed F-value of the test.
        pvalue : float
            The associated p-value from the F-distribution.

        """
        return super(AnovaOne, self).get_result()

    def print(self):
        result = {'F-Statistic': [self._statistic], 'p-value': [self._p]}
        print(tabulate(result, headers='keys'))                
