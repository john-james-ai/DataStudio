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
class MetaData:
    """MetaData master class. 
    
    Class provides behaviors to capture and manage administrative, 
    descriptive, and technical metadata.

    Parameters
    ----------
    entity : Object for which the metadata is being created

    """
    
    def __init__(self, entity):        
        self._metadata = {}
        self._create_metadata(entity)

    def _create_metadata(self):
        """Factory method that creates metadata objects."""
        self._metadata['admin'] = MetaDataAdmin(self)
        self._metadata['desc'] = MetaDataDesc(self)
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

    def add_admin(self, key, value):
        """Adds administrative metadata."""



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
        old = self._metadata['desc'].name
        self._metadata['desc'].name = value
        msg = "Changed object version from '" + old + "' to '" + value + "'"
        self._logger.info(msg)        
        return self

    @property
    def description(self):
        return self._metadata['desc'].description

    @description.setter
    def description(self, value):
        old = self._metadata['desc'].description
        self._metadata['desc'].description = value
        msg = "Changed object version from '" + old + "' to '" + value + "'"
        self._logger.info(msg)                
        return self

    @property
    def version(self):
        return self._metadata['desc'].version

    @version.setter
    def version(self, value):
        old = self._metadata['desc'].version
        self._metadata['desc'].version = value
        msg = "Changed object version from '" + old + "' to '" + value + "'"
        self._logger.info(msg)                
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

