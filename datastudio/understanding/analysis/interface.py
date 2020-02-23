#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : interface.py                                                      #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 22nd 2020, 6:01:51 pm                    #
# Last Modified : Saturday, February 22nd 2020, 6:01:59 pm                    #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Module contains the interface for all Analysis classes."""

from abc import ABC, abstractmethod

# --------------------------------------------------------------------------- #
#                        AbstractStatisticalTest                              #
# --------------------------------------------------------------------------- #
class AbstractAnalysis(ABC):

    @abstractmethod
    def __init__(self):
        self._statistical_tests = {}
        self._visual_analyses = {}      
        self._quantitative_analyses = {}    

    @abstractmethod
    def fit(self, *args, **kwargs):
        pass

    def list_components(self, category=None):
        """Lists statistical test, quantitative and visual components of the analysis.
        
        Parameters
        ----------
        category : str, Default = None
            The category of components to list. Values are: 
            - 'stat' : The statistical test components
            - 'quant' : The quantitative analysis components
            - 'visual' : The visual analysis components
            None will list all components.

        Returns
        -------
        components : list
            List of components.
        """

    
    def get_result(self):
        """ Returns the statistic and p_value for the test."""
        return self._statistic, self._p

    @property
    def statistic(self):
        """ Returns the test statistic"""
        return self._statistic

    @property
    def p_value(self):
        """ Returns the p-value for the test statistic."""
        return self._p

    @abstractmethod
    def print(self):
        pass        

