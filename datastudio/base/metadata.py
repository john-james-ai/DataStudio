#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : DataStudio                                                        #
# Version : 0.1.0                                                             #
# File    : metadata.py                                                       #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Saturday, January 18th 2020, 6:11:10 pm                     #
# Last Modified : Saturday, January 18th 2020, 6:11:10 pm                     #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""MetaData Factory and Classes and Decorators for Various Types of MetaData."""
from abc import ABC, abstractmethod
import time
import uuid

# --------------------------------------------------------------------------- #
#                              METADATA                                       #
# --------------------------------------------------------------------------- #
class MetaData(ABC):
    """Abstract base class for all MetaData classes."""

    def __init__(self, instance):
        self._id = uuid.uuid4()        
        self._creator = os.getlogin()
        self._created = time.ctime(os.path.getctime(__file__))
        self._modifier = os.getlogin()
        self._modified = time.ctime(os.path.getmtime(__file__))
        self._updates = 0
        self._instance = instance
        self._class = instance.__class__.__name__
                
        

    def __call__(self, *args, **kwargs):
        
    
        return self.func(*args, **kwargs)        