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
from datastudio.core.metadata import MetaDataTech, MetaDataPersist

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
        self._create_metadata(name)
        logging.info('Class instantiation.')


    def _create_metadata(self, name):
        """Factory method that creates metadata objects."""
        self._metadata_admin = MetaDataAdmin(self)
        self._metadata_desc = MetaDataDesc(self, name)
        self._metadata_tech = MetaDataTech(self)
        self._metadata_persist = MetaDataPersist(self)
        
    # Administrative metadata management
    def get_metadata_admin(self):
        """ Obtain administrative metadata."""
        return self._metadata_admin.get_metadata()

    def update_metadata_admin(self):
        """ Update administrative metadata."""
        return self._metadata_admin.update_metadata()

    def print_metadata_admin(self):
        """ Prints administrative metadata."""
        self._metadata_admin.print()        
        return self

    # Descriptive metadata management
    def get_metadata_desc(self):
        """ Obtain descriptive metadata."""
        return self._metadata_desc.get_metadata()

    def update_metadata_desc(self):
        """ Update descriptive metadata."""
        return self._metadata_desc.update_metadata()

    def print_metadata_desc(self):
        """ Prints descriptive metadata."""
        self._metadata_desc.print()        
        return self    

    @property
    def name(self):
        """Returns the name of the object."""
        return self._metadata_desc.name

    @name.setter
    def name(self, value):
        self._metadata_desc.name = value
        return self

    @property
    def description(self):
        return self._metadata_desc.description

    @description.setter
    def description(self, value):
        self._metadata_desc.description = value
        return self

    @property
    def version(self):
        return self._metadata_desc.version

    @version.setter
    def version(self, value):
        self._metadata_desc.version = value
        return self

    @property
    def keywords(self):
        return self._metadata_desc.keywords
    
    def add_keyword(self, value):
        self._metadata_desc.keywords.append(value)
        return self

    def remove_keyword(self, value):
        self._metadata_desc.keywords.remove(value)
        return self

    # Technical metadata management
    def get_metadata_admin(self):
        """ Obtain technical metadata."""
        return self._metadata_tech.get_metadata()

    def update_metadata_tech(self):
        """ Update technical metadata."""
        return self._metadata_tech.update_metadata()

    def print_metadata_tech(self):
        """ Prints technical metadata."""
        self._metadata_tech.print()        
        return self        

    # Technical metadata management
    def get_metadata_persist(self):
        """ Obtain technical metadata."""
        return self._metadata_persist.get_metadata()

    def update_metadata_persist(self):
        """ Update technical metadata."""
        return self._metadata_persist.update_metadata()

    def print_metadata_persist(self):
        """ Prints technical metadata."""
        self._metadata_persist.print()        
        return self          