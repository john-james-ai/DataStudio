#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : entity.py                                                         #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Friday, February 14th 2020, 8:22:33 am                      #
# Last Modified : Friday, February 14th 2020, 8:39:26 am                      #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
""" Module encapsulates data and behaviors for Entity classes."""
from abc import ABC, abstractmethod
import logging

from datastudio.core.metadata import MetaDataAdmin, MetaDataDesc
from datastudio.core.metadata import MetaDataTech

# --------------------------------------------------------------------------- #
#                              Entity                                         #
# --------------------------------------------------------------------------- #
class Entity(ABC):
    """Abstract base class for all Entity related classes.
    
    The Entity class is an abstract base class that defines the information
    and behavior for all classes with an entity stereotype. Examples of 
    Entity subclasses include:
        - DataObject : A wrapper for a dataset or dataframe.   
        - Project : Encapsulates all objects and behaviors for a project.
        - Task : Contains objects and behaviors to accomplish specific tasks.
    
    The Entity class encapsulates primarily administrative information and
    behaviors such as metadata creation and management and logging. 
    """

    def __init__(self, name):        
        self._metadata = {}
        self._create_metadata(name)
        logging.info('Class instantiation.')


    def _create_metadata(self, name):
        """Factory method that creates metadata objects."""
        self._metadata['admin'] = MetaDataAdmin(self)
        self._metadata['desc'] = MetaDataDesc(self, name)
        self._metadata['tech'] = MetaDataTech(self)


    def get_metadata(self):
        """Obtain all metadata and return a dictionary."""        
        metadata = {}
        for k, v in self._metadata.items():
            metadata[k] = v.get_metadata().copy()
        return metadata

    def update_metadata(self):
        """Update all metadata.""" 
        for k, v in self._metadata.items():
            v.update_metadata()  
        return self

    def print_metadata(self):
        """Print all metadata."""
        for _, v in self._metadata.items():            
            v.print()
            print("\n")
        return self

    # Administrative metadata management
    def get_metadata_admin(self):
        """ Obtain administrative metadata."""
        return self._metadata['admin'].get_metadata().copy()

    def update_metadata_admin(self):
        """ Update administrative metadata."""
        self._metadata['admin'].update_metadata()        
        return self

    def print_metadata_admin(self):
        """ Prints administrative metadata."""
        self._metadata['admin'].print()        
        return self

    # Descriptive metadata management
    def get_metadata_desc(self):
        """ Obtain descriptive metadata."""
        return self._metadata['desc'].get_metadata().copy()

    def update_metadata_desc(self):
        """ Update descriptive metadata."""
        return self._metadata['desc'].update_metadata()

    def print_metadata_desc(self):
        """ Prints descriptive metadata."""
        self._metadata['desc'].print()        
        return self    

    @property
    def name(self):
        """Returns the name of the object."""
        return self._metadata['desc'].name

    @name.setter
    def name(self, value):
        self._metadata['desc'].name = value
        return self

    @property
    def description(self):
        return self._metadata['desc'].description

    @description.setter
    def description(self, value):
        self._metadata['desc'].description = value
        return self

    @property
    def version(self):
        return self._metadata['desc'].version

    @version.setter
    def version(self, value):
        self._metadata['desc'].version = value
        return self

    # Technical metadata management
    def get_metadata_tech(self):
        """ Obtain technical metadata."""
        return self._metadata['tech'].get_metadata().copy()

    def update_metadata_tech(self):
        """ Update technical metadata."""
        self._metadata['tech'].update_metadata()
        return self

    def print_metadata_tech(self):
        """ Prints technical metadata."""
        self._metadata['tech'].print()        
        return self        
