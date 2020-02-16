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
# Last Modified : Sunday, February 16th 2020, 7:04:22 am                      #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
""" Management of administrative, descriptive and technical metadata.

This module encapsulates the creation, management, and reporting of 
administrative, descriptive, and technical metadata. Metadata is being 
maintained for three categories of classes:

    * Data : Classes that contain the data being analyzed and modeled.
    * Analysis : Classes that encapsulate various types of analyses.
    * Model : Machine learning models

Though each of these types of classes have distinct metadata requirements,
most can be characterized as:

    * Administrative metadata - Management information
    * Descriptive metadata - Discovery and identification
    * Technical metadata - Systems and environment
    * Process metadata - Log of tasks and operations performed

As such, the following enumerates the classes in this module.

    Factory Classes
    ------------------------
    AbstractMetadataFactory : Abstract base class and interface for factory classes.
    MetadataFactoryData : Concrete metadata factory for Data objects.
    MetadataFactoryAnalysis : Concrete metadata factory for Analysis objects.
    MetadataFactoryModel : Concrete metadata factory for Model objects.
    MetadataFactoryExperiment : Concrete metadata factory for Experiment objects.

    Metadata Interface Classes
    --------------------------
    AbstractMetadataAdmin : Abstract base class for all administrative Metadata classes.
    AbstractMetadataDesc : Abstract base class for all descriptive Metadata classes.
    AbstractMetadataTech : Abstract base class for all technical Metadata classes.

    Metadata Container Classes
    --------------------------
    Metadata : Encapsulates all metadata for a Data object 
    MetadataAnalysis : Encapsulates all metadata for an Analysis object
    MetadataModel : Encapsulates all metadata for a Model object

    Metadata Classes for Data Objects
    ----------------------------------
    MetadataAdminData : Administrative Metadata class for Data objects 
    MetadataDescData : Descriptive Metadata class for Data objects
    MetadataTechData : Technical Metadata class for Data objects

    Metadata Classes for Analysis Objects
    -------------------------------------
    MetadataAdminAnalysis : Administrative Metadata class for Analysis objects 
    MetadataDescAnalysis : Descriptive Metadata class for Analysis objects
    MetadataTechAnalysis : Technical Metadata class for Analysis objects

    Metadata  Classes for Model Objects
    -----------------------------------
    MetadataAdminModel : Administrative Metadata class for Model objects 
    MetadataDescModel : Descriptive Metadata class for Model objects
    MetadataTechModel : Technical Metadata class for Model objects    

"""
from abc import ABC, abstractmethod
import os
from datetime import datetime
import platform
from pprint import pprint
import psutil
import sys
import time
import uuid

from ..utils.format import scale_number
# =========================================================================== #
#                          METADATA FACTORY CLASSES                           #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                         AbstractMetadataFactory                             #
# --------------------------------------------------------------------------- #
class AbstractMetadataFactory(ABC):
    """ Behaviors required to create Metadata objects of various types.
    
    The Abstract Factory interface declares a set of methods that return
    different Metadata objects. These objects are called a family and are
    related by the type of object the metadata will represent. 
    """
    @abstractmethod
    def create_admin_metadata(self):
        pass

    @abstractmethod
    def create_desc_metadata(self):
        pass

    @abstractmethod
    def create_tech_metadata(self):
        pass

# --------------------------------------------------------------------------- #
#                         MetadataFactoryData                                 #
# --------------------------------------------------------------------------- #
class MetaDataFactoryData(AbstractMetadataFactory):
    """Creates Metadata objects for Data objects.

    This concrete factory produces administrative, descriptive and technical
    Metadata objects for Data objects.  
    """

    def create_admin_metadata(self):
        return MetadataAdminData()

    def create_desc_metadata(self):
        return MetadataDescData()

    def create_tech_metadata(self):
        return MetadataTechData()

# --------------------------------------------------------------------------- #
#                       MetadataFactoryAnalysis                               #
# --------------------------------------------------------------------------- #
class MetadataFactoryAnalysis(AbstractMetadataFactory):
    """Creates Metadata objects for Analysis objects.

    This concrete factory produces administrative, descriptive and technical
    Metadata objects for Analysis objects.  
    """

    def create_admin_metadata(self):
        return MetadataAdminAnalysis()

    def create_desc_metadata(self):
        return MetadataDescAnalysis()

    def create_tech_metadata(self):
        return MetadataTechAnalysis()


# --------------------------------------------------------------------------- #
#                       MetadataFactoryModel                                  #
# --------------------------------------------------------------------------- #
class MetadataFactoryModel(AbstractMetadataFactory):
    """Creates Metadata objects for Model objects.

    This concrete factory produces administrative, descriptive and technical
    Metadata objects for Model objects.  
    """

    def create_admin_metadata(self):
        return MetadataAdminModel()

    def create_desc_metadata(self):
        return MetadataDescModel()

    def create_tech_metadata(self):
        return MetadataTechModel()


# --------------------------------------------------------------------------- #
#                       MetadataFactoryExperiment                             #
# --------------------------------------------------------------------------- #
class MetadataFactoryExperiment(AbstractMetadataFactory):
    """Creates Metadata objects for Experiment objects.

    This concrete factory produces administrative, descriptive and technical
    Metadata objects for Experiment objects.  
    """

    def create_admin_metadata(self):
        return MetadataAdminExperiment()

    def create_desc_metadata(self):
        return MetadataDescExperiment()

    def create_tech_metadata(self):
        return MetadataTechExperiment()

# =========================================================================== #
#                             METADATA CLASSES                                #
# =========================================================================== #
# --------------------------------------------------------------------------- #
#                          AbstractMetadataAdmin                              #
# --------------------------------------------------------------------------- #
class AbstractMetadataAdmin(ABC):
    """ Abstract base class for all administrative metadata classes."""

    def __init__(self, entity, name):
        self._entity = entity
        self._metadata = {}        
        self._metadata['name'] = name


    @abstractmethod
    def get(self, key):
        """ Returns the administrative metadata."""
        pass 

    @abstractmethod
    def add(self, key, value):
        """ Adds administrative metadata element."""
        pass

    @abstractmethod
    def change(self, key, value):
        """Changes an administrative metadata key value pair."""
        pass

    @abstractmethod
    def remove(self, key):
        """Removes an administrative metadata key value pair."""
        pass

    @abstractmethod
    def update(self):
        """Updates the metadata affected by any changes to the object."""
        pass

    def print(self):
        pprint(self._metadata)
        
# --------------------------------------------------------------------------- #
#                          MetadataAdminData                                  #
# --------------------------------------------------------------------------- #
class MetadataAdminData(AbstractMetadataAdmin):
    """Concrete administrative metadata object for Data objects."""

    def __init__(self, entity, name):
        super(MetadataAdminData, self).__init__(entity, name)

        # Extract user datetime and object data once to avoid repeated calls.
        user = os.getlogin()
        date = datetime.now()
        date_string = date.year + '-' + date.month + '-' + \
            date.day + '_' + date.hour + '-' + date.minute + '-' \
                + date.second
        date_formatted = time.strftime("%c")
        classname = entity.__class__.__name__

        self._metadata['id'] = uuid.uuid4()                
        self._metadata['name'] = name
        self._metadata['creator'] = user
        self._metadata['created'] = date_formatted
        self._metadata['modifier'] = user
        self._metadata['modified'] = date_formatted
        self._metadata['updates'] = 0
        self._metadata['classname'] = classname        
        self._metadata['objectname'] = user + '_' + date_string + '_' + time + '_'\
            + classname + '_' + name

    def get(self, key):
        """Returns the value for a specific attribute."""
        return self._metadata.get(key, None)

    def add(self, key, value):
        """Adds metadata attribute."""
        if key not in self._metadata:
            self._metadata[key] = value
        else:
            raise ValueError("Key {key} already exists.".format(key=key))

    def change(self, key, value):
        """Change a key value pair."""
        try:
            self._metadata[key] = value
        except KeyError:
            print("Key {key} does not exist.".format(key=key))

    def remove(self, key):
        """Remove a key value pair based upon 'key'."""
        try:
            del self._metadata[key]
        except KeyError:
            print("Key {key} does not exist.".format(key=key))

    def update(self):
        """Updates metadata attributes to reflect changes to object."""
        self._metadata['modifier'] = os.getlogin()
        self._metadata['modified'] = time.strftime("%c")
        self._metadata['updates'] += 1
        






class MetadataBase(ABC):
    """Abstract base class from which all Metadata* classes are derived."""
    def __init__(self, entity):
        self._entity = entity
        self._metadata = {}
    
    def get_metadata(self):
        return self._metadata.copy()

    def update_metadata(self):
        pass

    def print(self):
        pprint(self._metadata)

# --------------------------------------------------------------------------- #
#                              MetadataAdmin                                  #
# --------------------------------------------------------------------------- #
class MetadataAdmin(MetadataBase):
    """ Storage and management of administrative metadata."""

    def __init__(self, entity):
        super(MetadataAdmin, self).__init__(entity)

        self._metadata['id'] = uuid.uuid4()                
        self._metadata['creator'] = os.getlogin()
        self._metadata['created'] = time.strftime("%c")
        self._metadata['modifier'] = os.getlogin()
        self._metadata['modified'] = time.strftime("%c")

    def update_metadata(self):
        self._metadata['modifier'] = os.getlogin()
        self._metadata['modified'] = time.strftime("%c")

# --------------------------------------------------------------------------- #
#                              MetadataDesc                                   #
# --------------------------------------------------------------------------- #
class MetadataDesc(MetadataBase):
    """ Storage and management of descriptive metadata."""

    def __init__(self, entity, name):
        super(MetadataDesc, self).__init__(entity)

        self._metadata['name'] = name
        self._metadata['description'] = ""
        self._metadata['class'] = entity.__class__.__name__
        self._metadata['version'] = "0.1.0"
        
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
#                              MetadataTech                                   #
# --------------------------------------------------------------------------- #
class MetadataTech(MetadataBase):
    """ Storage and management of technical metadata."""

    def __init__(self, entity):
        super(MetadataTech, self).__init__(entity)

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
        self._metadata['object_size'] = sys.getsizeof(self._entity)