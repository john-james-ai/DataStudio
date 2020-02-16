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
""" Management of administrative, descriptive, technical and process metadata.

This module encapsulates the creation, management, and reporting of 
administrative, descriptive, technical and process metadata, hereinafter
called the metadata taxonomy. The classes include:

    * Metadata : Main class containing the metadata taxonomy objects.
    * MetadataBuilder : Class responsible for constructing the Metadata class.
    * AbstractMetadataBuilder : Interface for the MetadataBuilder class
    * AbstractMetadata : Interace for metadata taxonomy classes.
    * MetadataAdmin : Data and behaviors for administrative metadata
    * MetadataDesc : Data and behaviors for descriptive metadata
    * MetadataTech : Data and behaviors for technical metadata
    * MetadataProcess : Data and behaviors for process metadata


"""
from abc import ABC, abstractmethod, abstractproperty
import os
from datetime import datetime
import platform
from pprint import pprint
import psutil
import sys
import time
import uuid

from ..utils.format import scale_number
# --------------------------------------------------------------------------- #
#                                 Metadata                                    #
# --------------------------------------------------------------------------- #
class Metadata:
    """ Class containing administrative, descriptive, and technical metadata."""

    def __init__(self):
        self._metadata = {}

    def add(self, metadata):          
        """Adds metadata object.
        
        Parameters
        ----------
        metadata : A MetadataAdmin, MetadataDesc, or MetadataTech object        
        """      
        self._metadata[metadata.type] = metadata

    def get(self, metadata_type=None):
        """ Returns a metadata object.

        Returns the administrative, descriptive, or technical metadata object
        based upon a partial match of the metadata_type parameter.  

        Parameters
        ----------
        metadata_type : str
            String or partial string containing the type of metadata.
        """
        metadata = [value for key, value in self._metadata.items() \
            if metadata_type.lower() in key.lower()]
        
        if len(metadata) == 0:
            raise KeyError("No metadata type matching '{t}'. \
                Run the 'print_types' method for a list of supported \
                    metadata types.".format(t=metadata_type))
        elif len(metadata) > 1:
            raise KeyError("The metadata type entered '{t}'. \
                matches more than one type of metadata. Please refine \
                    your search with a more precise metadata type.\
                        ".format(t=metadata_type))            
        else:
            return metadata

    def print_types(self):
        for k in self._metadata.keys():
            print(k)

    def print(self):
        for v in self._metadata.values():
            v.print()



# --------------------------------------------------------------------------- #
#                          AbstractMetadataBuilder                            #
# --------------------------------------------------------------------------- #
class AbstractMetadataBuilder(ABC):
    """Abstract base class exposing methods for creating the Metadata objects."""

    @abstractproperty
    def metadata(self):
        pass

    @abstractmethod
    def build_admin(self):
        pass

    @abstractmethod
    def build_desc(self):
        pass

    @abstractmethod
    def build_tech(self):
        pass


# --------------------------------------------------------------------------- #
#                            MetadataBuilder                                  #
# --------------------------------------------------------------------------- #
class MetadataBuilder:
    """ Builds a Metadata object containing admin, descriptive and tech metadata.

    Implements the AbstractMetadataBuilder interface and provides specific
    implementation steps to build the Metadata object.
    
    """

    def __init__(self, entity, name):        
        """ Fresh builder object should contain an empty Metadata object."""
        self._entity = entity
        self._name = name
        self._reset()

    def _reset(self):
        self._metadata = Metadata()

    @property
    def metadata(self):
        """ Returns the metadata object once completed."""
        metadata = self._metadata
        self._reset()
        return metadata

    def build_admin(self):
        """Adds a administrative metadata subclass object."""
        admin = MetadataAdmin(self._entity, self._name)
        self._metadata.add(admin)

    def build_desc(self):
        """Adds a descriptive metadata subclass object."""
        desc = MetadataDesc(self._entity, self._name)
        self._metadata.add(desc)

    def build_tech(self):
        """Adds a technical metadata subclass object."""
        tech = MetadataTech(self._entity, self._name)
        self._metadata.add(tech)

# --------------------------------------------------------------------------- #
#                           AbstractMetadata                                  #
# --------------------------------------------------------------------------- #
class AbstractMetadata(ABC):
    """ Abstract base class for adminstrative, descriptive, & technical metadata.""" 

    def __init__(self, entity, name):
        self._entity = entity
        self._metadata = {}
        self._metadata['name'] = name    
        self._metadata['updates'] = 0

    def update(self, event=None):
        """Updates metadata attributes to reflect changes to object."""
        self._metadata['updates'] += 1

    def get(self, key=None):
        """Returns the value for a specific attribute."""
        if key:
            return self._metadata.get(key, None)
        else:
            return self._metadata.copy()

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

    def print(self):
        """Prints the metadata."""
        pprint(self._metadata)       

# --------------------------------------------------------------------------- #
#                            MetadataAdmin                                    #
# --------------------------------------------------------------------------- #
class MetadataAdmin(AbstractMetadata):
    """Concrete administrative metadata object."""

    def __init__(self, entity, name):
        super(MetadataAdmin, self).__init__(entity, name)
        self.metadata_type = 'Administrative'

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
        self._metadata['classname'] = classname        
        self._metadata['objectname'] = user + '_' + date_string + '_' + time + '_'\
            + classname + '_' + name

    def update(self, event=None):
        """Updates metadata attributes to reflect changes to object."""
        super(MetadataAdmin, self).update()
        self._metadata['modifier'] = os.getlogin()
        self._metadata['modified'] = time.strftime("%c")

# --------------------------------------------------------------------------- #
#                              MetadataDesc                                   #
# --------------------------------------------------------------------------- #
class MetadataDesc(AbstractMetadata):
    """ Storage and management of descriptive metadata."""

    def __init__(self, entity, name):
        super(MetadataDesc, self).__init__(entity, name)
        self.metadata_type = 'Descriptive'

        self._metadata['description'] = ""
        self._metadata['class'] = entity.__class__.__name__
        self._metadata['version'] = "0.1.0"
        
# --------------------------------------------------------------------------- #
#                              MetadataTech                                   #
# --------------------------------------------------------------------------- #
class MetadataTech(AbstractMetadata):
    """ Storage and management of technical metadata."""

    def __init__(self, entity, name):
        super(MetadataTech, self).__init__(entity, name)
        self.metadata_type = 'Technical'

        self.update_metadata()

    def update_metadata(self, event=None):
        """Updates technical metadata."""
        super(MetadataTech, self).update()
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

# --------------------------------------------------------------------------- #
#                              MetadataProcess                                #
# --------------------------------------------------------------------------- #
class MetadataProcess(AbstractMetadata):
    """ Storage and management of process metadata."""

    def __init__(self, entity, name):
        super(MetadataProcess, self).__init__(entity, name)
        self.metadata_type = 'Process'      

        self._metadata['log'] = []

        user = os.getlogin()
        date_formatted = time.strftime("%c")
        classname = entity.__class__.__name__        
        msg = classname + ' object named ' + name + ' was instantiated ' +\
            ' at ' + date_formatted + ' by ' + user
        self._metadata['log'].append(msg)

    def update(self, event=None):
        """Logs an activity update.""" 
        user = os.getlogin()
        date_formatted = time.strftime("%c")
        classname = self._entity.__class__.__name__        
        msg = 'Class : ' + classname + 'Name : ' + name +\
            'Date : ' + date_formatted + 'Event : ' + event
        if event:
            self._metadata['log'].append(msg)