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
related classes. The classes include:

    - MetaDataBase : Abstract base class from which all metadata classes derive. 
    - MetaData : Collection of administrative, technical and descriptive
        metadata subclasses for a specific Entity subclass.
    - MetaDataAdmin : Administrative metadata
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

# --------------------------------------------------------------------------- #
#                              MetaDataBase                                   #
# --------------------------------------------------------------------------- #
class MetaDataBase(ABC):
    """Abstract base class from which all MetaData* classes are derived.
    
    Defines the interface common among MetaData* classes. Operations include:
        - 

        - MetaData - Classes for the creation and management of administrative, 
            descriptive, and technical metadata.
        - Project - A Project object which specifies attributes common
            to all classes within a project.
        - Logger - Object for tracking access and update operations 
         
    Encapsulates and standardizes methods to create and manage five  
    categories of metadata:
        - Administrative - Date and time created, modified and by whom
        - Descriptive - Data used for the purposes of discovery and 
            identification       
        - Technical - Hardware, software environment, object size and format.
        - Persistence - Data serialization and filename information.
        - log - Access and update operations performed on the data. 

        """

    def __init__(self, name, project = None, version = '0.1.0', keywords = []):

        # Store project object
        self._project = project 

        # Administrative metadata
        self._admin = {}
        self._admin['id'] = uuid.uuid4()                
        self._admin['creator'] = os.getlogin()
        self._admin['created'] = time.ctime(os.path.getctime(__file__))
        self._admin['modifier'] = os.getlogin()
        self._admin['modified'] = time.mtime(os.path.getmtime(__file__))        

        # Descriptive metadata
        self._descriptive = {}
        self._descriptive['name'] = name
        self._descriptive['description'] = ""
        self._descriptive['class'] = self.__class__.__name__
        self._descriptive['version'] = version        
        self._descriptive['keywords'] = keywords

        # Technical metadata
        self._technical = {}
        uname = platform.uname()
        svmem = psutil.virtual_memory()

        self._technical['system'] = uname.system
        self._technical['node'] = uname.node
        self._technical['release'] = uname.release
        self._technical['version'] = uname.version
        self._technical['machine'] = uname.machine
        self._technical['processor'] = uname.processor
        self._technical['release'] = uname.release
        self._technical['physical_cores'] = psutil.cpu_count(logical=False)
        self._technical['total_cores'] = psutil.cpu_count(logical=True)
        self._technical['total_memory'] = scale_number(svmem.total)
        self._technical['available_memory'] = scale_number(svmem.available)
        self._technical['used_memory'] = scale_number(svmem.used)
        self._technical['pct_memory_used'] = svmem.percent

        # Persistence metadata
        if self._project:
            self._persistence['filename'] = self._project.name + \
                self._project.location + \
                self._project.member + self.__class__.__name__ + \
                self._descriptive['name'] + \
                    time.mtime(os.path.getmtime(__file__)) + '.P'
        else:
            self._persistence['filename'] = self.__class__.__name__ + \
                self._descriptive['name'] + \
                    time.mtime(os.path.getmtime(__file__)) + '.P'

        # Log  
        # TODO: Add logging to pandas dataframe.       
        self._log = pd.DataFrame() 

    

    def _update_metadata(self):
        """ Update metadata ."""

        # Update administrative metadata        
        self._admin['modifier'] = os.getlogin()
        self._admin['modified'] = time.mtime(os.path.getmtime(__file__))        

        # Update technical metadata
        self._technical = {}
        uname = platform.uname()
        svmem = psutil.virtual_memory()

        self._technical['system'] = uname.system
        self._technical['node'] = uname.node
        self._technical['release'] = uname.release
        self._technical['version'] = uname.version
        self._technical['machine'] = uname.machine
        self._technical['processor'] = uname.processor
        self._technical['release'] = uname.release
        self._technical['physical_cores'] = psutil.cpu_count(logical=False)
        self._technical['total_cores'] = psutil.cpu_count(logical=True)
        self._technical['total_memory'] = scale_number(svmem.total)
        self._technical['available_memory'] = scale_number(svmem.available)
        self._technical['used_memory'] = scale_number(svmem.used)
        self._technical['pct_memory_used'] = svmem.percent                

        # Persistence metadata
        if self._project:
            self._persistence['filename'] = self._project.name + \
                self._project.location + \
                self._project.member + self.__class__.__name__ + \
                self._descriptive['name'] + \
                    time.mtime(os.path.getmtime(__file__)) + '.P'
        else:
            self._persistence['filename'] = self.__class__.__name__ + \
                self._descriptive['name'] + \
                    time.mtime(os.path.getmtime(__file__)) + '.P'