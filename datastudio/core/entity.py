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
# Created       : Saturday, February 22nd 2020, 7:01:31 pm                    #
# Last Modified : Saturday, February 22nd 2020, 7:01:31 pm                    #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Module containing entity related interfaces."""
from abc import ABC, abstractmethod
from datastudio.core.metadata import MetadataEntityFactory 
# --------------------------------------------------------------------------- #
#                               Entity                                        #
# --------------------------------------------------------------------------- #
class Entity(ABC):
    """Abstract base class for all entity classes.

    Contains a limited set of behaviors that allow objects to be described
    in terms of their metadata attributes. Some methods are exposed to allow
    updates to descriptive metadata.

    Parameters
    ----------
    name : str
        The snake case name assigned to the object. All subclasses must have 
        names.

    kwargs : dictionary
        Other parameters required by subclasses.

    """

    def __init__(self, name, **kwargs):
        self._name        
        self.metadata = self._build_metadata()

    def _build_metadata(self):
        factory = MetadataEntityFactory(self, self._name)
        factory.create_admin() 
        factory.create_desc() 
        factory.create_tech() 
        factory.create_process() 
        return factory.metadata        

    @property
    def name(self):
        """Returns the name of the DataSet."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        admin = next( v for k,v in self._metadata.items() if k.startswith('admin'))
        admin.change('name', value)
