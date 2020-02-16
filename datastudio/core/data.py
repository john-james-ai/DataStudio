#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : data.py                                                           #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 15th 2020, 9:48:56 pm                    #
# Last Modified : Saturday, February 15th 2020, 9:48:56 pm                    #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Module defines the data classes.

The data classes are the core Entity classes within DataStudio. Everything
starts with a data source indicated by the path parameter. The source is 
converted to dataframe and stored in a DataObject. 

Data classes contain the source DataObject as well as snapshots or
versions of the original source. Methods are exposed to verify, analyze, 
clean, transform, impute, and engineer the data.

As such, this module includes:

    * DataObject : Object representation of a single data source.
    * Data : Source (immutable) and mutable versions of the source DataObject.
    
"""
import pandas as pd
from datastudio.core.entity import Entity
# --------------------------------------------------------------------------- #
#                               DataObject                                    #
# --------------------------------------------------------------------------- #
class DataObject(Entity):

    def __init__(self, name, path):        
        super(DataObject, self).__init__(name)        
        self._df = pd.DataFrame()
        self._path = path
        self._locked = False

    
