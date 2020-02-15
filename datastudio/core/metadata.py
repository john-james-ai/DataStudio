#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : metadata.py                                                       #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Friday, February 14th 2020, 8:47:19 am                      #
# Last Modified : Friday, February 14th 2020, 8:47:29 am                      #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
""" Management of administrative, descriptive and technical metadata.

This module encapsulates the creation, management, and reporting of 
administrative, descriptive, and technical metadata common to all entity
related classes. The classes in this module are:

    - MetaDataBase : Abstract base class from which all metadata classes derive. 
    - MetaDataAdmin : Administrative metadata.    
    - MetaDataDesc : Descriptive metadata
    - MetaDataTech : Technical metadata
"""
from abc import ABC, abstractmethod
import os
from datetime import datetime
import psutil
import platform
import time
import uuid

from ..utils.format import scale_number
# --------------------------------------------------------------------------- #
#                              MetaDataBase                                   #
# --------------------------------------------------------------------------- #
class MetaDataBase(ABC):
    """Abstract base class from which all MetaData* classes are derived."""
    def __init__(self, entity):
        self._entity = entity
        self._metadata = {}
    
    def get_metadata(self):
        return self._metadata.copy()

    def update_metadata(self):
        pass

    @abstractmethod
    def print(self):
        pass

# --------------------------------------------------------------------------- #
#                              MetaDataAdmin                                  #
# --------------------------------------------------------------------------- #
class MetaDataAdmin(MetaDataBase):
    """ Storage and management of administrative metadata."""

    def __init__(self, entity):
        super(MetaDataAdmin, self).__init__(entity)

        self._metadata['id'] = uuid.uuid4()                
        self._metadata['creator'] = os.getlogin()
        self._metadata['created'] = time.strftime("%c")
        self._metadata['modifier'] = os.getlogin()
        self._metadata['modified'] = time.strftime("%c")

    def update_metadata(self):
        self._metadata['modifier'] = os.getlogin()
        self._metadata['modified'] = time.strftime("%c")

    # TODO: Create print method
    def print(self):
        pass
        

# --------------------------------------------------------------------------- #
#                              MetaDataDesc                                   #
# --------------------------------------------------------------------------- #
class MetaDataDesc(MetaDataBase):
    """ Storage and management of descriptive metadata."""

    def __init__(self, entity, name):
        super(MetaDataDesc, self).__init__(entity)

        self._metadata['name'] = name
        self._metadata['description'] = ""
        self._metadata['class'] = entity.__class__.__name__
        self._metadata['version'] = "0.1.0"
        
    #TODO: 
    def print(self):
        pass

    @property
    def name(self):
        return self._metadata['name']

    @name.setter
    def name(self, value):
        self._metadata['name'] = value
        return self

    @property
    def description(self):
        return self._metadata['description']

    @description.setter
    def description(self, value):
        self._metadata['description'] = value

    @property
    def version(self):
        return self._metadata['version']

    @version.setter
    def version(self, value):
        self._metadata['version'] = value



# --------------------------------------------------------------------------- #
#                              MetaDataTech                                   #
# --------------------------------------------------------------------------- #
class MetaDataTech(MetaDataBase):
    """ Storage and management of technical metadata."""

    def __init__(self, entity):
        super(MetaDataTech, self).__init__(entity)

        self.update_metadata()

    def update_metadata(self):
        """Updates technical metadata."""
        uname = platform.uname()
        svmem = psutil.virtual_memory()

        self._metadata['system'] = uname.system
        self._metadata['node'] = uname.node
        self._metadata['release'] = uname.release
        self._metadata['version'] = uname.version
        self._metadata['machine'] = uname.machine
        self._metadata['processor'] = uname.processor
        self._metadata['release'] = uname.release
        self._metadata['physical_cores'] = psutil.cpu_count(logical=False)
        self._metadata['total_cores'] = psutil.cpu_count(logical=True)
        self._metadata['total_memory'] = scale_number(svmem.total)
        self._metadata['available_memory'] = scale_number(svmem.available)
        self._metadata['used_memory'] = scale_number(svmem.used)
        self._metadata['pct_memory_used'] = svmem.percent        

    # TODO: Create print method
    def print(self):
        pass



