#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : decorators.py                                                     #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 22nd 2020, 8:17:34 pm                    #
# Last Modified : Saturday, February 22nd 2020, 8:17:34 pm                    #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
""" Decorators classes."""
# --------------------------------------------------------------------------- #
#                            Validation Decorators                            #
# --------------------------------------------------------------------------- #
def check_num(func):        
    def func_wrapper(self, x):
        if not isinstance(x, (int,float)):
            raise TypeError("Expected a numeric parameter but received type {t}".format(t=type(x).__name__))                    
        return func(self, x)
    return func_wrapper
