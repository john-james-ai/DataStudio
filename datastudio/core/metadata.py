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
    - MetaData : Collection of administrative, technical and descriptive
        metadata subclasses for a specific Entity subclass.
    - MetaDataTech : Techistrative metadata
    - MetaDataDescriptive : Descriptive metadata
    - MetaDataTechnical : Technical metadata
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
        self.is_composite = False
    
    def get_metadata(self):
        return self._metadata

    def add_metadata(self, metadata):
        pass

    def update_metadata(self):
        pass

    @abstractmethod
    def remove_metadata(self, metadata):
        pass

    @abstractmethod
    def print(self):
        pass

# --------------------------------------------------------------------------- #
#                              MetaData                                       #
# --------------------------------------------------------------------------- #
class MetaData(MetaDataBase):
    """Composite class containing the metadata subclasses."""

    def __init__(self, entity):
        super(MetaData, self).__init__(entity)
        self.is_composite = True

    def get_metadata(self):
        return self._metadata

    def add_metadata(self, metadata):
        self._metadata[metadata.__class__.__name__] = metadata

    def update_metadata(self):
        for k, v in self._metadata.items():
            v.update_metadata()        

    def remove_metadata(self, metadata):
        del self._metadata[metadata.__class__.__name__] 

    def print(self):
        for k, v in self._metadata.items():
            v.print()

# --------------------------------------------------------------------------- #
#                              MetaDataTech                                  #
# --------------------------------------------------------------------------- #
class MetaDataTech(MetaDataBase):
    """ Storage and management of administrative metadata."""

    def __init__(self, entity):
        super(MetaDataTech, self).__init__(entity)

        self._metadata = {}

        self._metadata['id'] = uuid.uuid4()                
        self._metadata['creator'] = os.getlogin()
        self._metadata['created'] = time.ctime(os.path.getctime(__file__))
        self._metadata['modifier'] = os.getlogin()
        self._metadata['modified'] = time.mtime(os.path.getmtime(__file__))        

    def update_metadata(self):
        self._metadata['modifier'] = os.getlogin()
        self._metadata['modified'] = time.mtime(os.path.getmtime(__file__))                

    def remove_metadata(self):
        self._metadata = {}

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
        self.is_composite = False

        self._metadata['name'] = name
        self._metadata['description'] = ""
        self._metadata['class'] = entity.__class__.__name__
        self._metadata['version'] = "0.1.0"
        self._metadata['keywords'] = [name, entity.__class__.__name__]

    def update_metadata(self):
        pass

    def remove_metadata(self):
        self._metadata = {}

    #TODO: 
    def print(self):
        pass

    @property
    def name(self):
        return self._metadata['name']

    @name.setter
    def name(self, value):
        self._metadata['name'] = value

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

    @property
    def keywords(self):
        return self._metadata['keywords']
    
    def add_keyword(self, value):
        self._metadata['keyword'].append(value)

    def remove_keyword(self, value):
        self._metadata['keyword'].remove(value)


# --------------------------------------------------------------------------- #
#                              MetaDataTech                                   #
# --------------------------------------------------------------------------- #
class MetaDataTech(MetaDataBase):
    """ Storage and management of administrative metadata."""

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
        
    def remove_metadata(self):
        self._metadata = {}

    # TODO: Create print method
    def print(self):
        pass


# --------------------------------------------------------------------------- #
#                              MetaDataPersistence                            #
# --------------------------------------------------------------------------- #
class MetaDataPersistence(MetaDataBase):
    """ Storage and management of persistence metadata."""

    def __init__(self, entity):
        super(MetaDataPersistence, self).__init__(entity)

        self.update_metadata()

    def update_metadata(self):
        if self._entity.project:
            self._metadata['filename'] = self._entity.project.name + \
                self._entity.project.location + \
                self._entity.project.taskname + \
                self._entity.project.member + self._entity.__class__.__name__ + \
                self._entity.name  + \
                    time.mtime(os.path.getmtime(__file__)) + '.P'
        else:
            self._metadata['filename'] = self._entity.__class__.__name__ + \
                self._entity.name  + \
                    time.mtime(os.path.getmtime(__file__)) + '.P'

    def remove_metadata(self, metadata):
        self._metadata = {}

    # TODO: Create print method
    def print(self):
        pass

