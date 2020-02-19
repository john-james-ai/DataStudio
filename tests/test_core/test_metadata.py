#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : test_metadata.py                                                  #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Friday, February 14th 2020, 11:21:34 pm                     #
# Last Modified : Friday, February 14th 2020, 11:21:34 pm                     #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Unit test for metadata classes."""
import numpy as np
import pandas as pd
import pytest
from pytest import mark
import time

from datastudio.core.metadata import Metadata, DataSetMetadataBuilder
from datastudio.core.metadata import MetadataDirector
from datastudio.core.metadata import MetadataAdmin, MetadataDesc, MetadataSystem
from datastudio.core.metadata import MetadataProcess
class MetaDataTests:
  

    @mark.metadata
    def test_dataset_metadata_build(self):

        print("\n\nDataset Metadata Object")
        print("="*40)
        director = MetadataDirector()
        builder = DataSetMetadataBuilder(self, name='test_object')
        director.builder = builder
        director.build()
        metadata = builder.metadata
        metadata.print_types()

        print("\n\nDataset Metadata Administrative")
        print("-"*40)
        admin = metadata.get('admin')    
        admin.print()
        assert isinstance(admin, MetadataAdmin), "MetadataAdmin not built."
        
        print("\n\nDataset Metadata Descriptive")
        print("-"*40)
        desc = metadata.get('desc')                
        desc.print()
        assert isinstance(desc, MetadataDesc), "MetadataDesc not built."

        print("\n\nDataset Metadata System")
        print("-"*40)
        system = metadata.get('system')                
        system.print()
        assert isinstance(system, MetadataSystem), "MetadataSystem not built."

        print("\n\Dataset nMetadata Process")
        print("-"*40)
        process = metadata.get('process')                
        process.print()
        assert isinstance(process, MetadataProcess), "MetadataProcess not built."

        with pytest.raises(KeyError):
            metadata.get('xxx')

    @mark.metadata
    def test_metadata_admin(self, get_metadata):
        print("\n\n DataSet Metadata Administrative Test")
        print("-"*40)        
        metadata = get_metadata
        admin = metadata.get('admin')
        admin.update()
        assert admin.get('updates') == 1, "Admin updates not correct."
        admin.add(key='artist', value='BOC')
        assert admin.get('artist') == 'BOC', "Admin get error."
        with pytest.raises(ValueError):        
            admin.add(key='artist', value='dunno')
        with pytest.raises(KeyError):        
            admin.change(key='cook', value='BOC')
        admin.change(key='artist', value='air')
        assert admin.get('artist') == 'air', "Admin change error."
        admin.remove(key='artist')
        with pytest.raises(KeyError):        
            assert admin.get('artist') == 'air', "Admin remove failed to raise Keyerror."
        assert isinstance(admin.get(), dict), "Get error, failed to return all admin metadata"
        
    @mark.metadata
    def test_metadata_desc(self, get_metadata):
        print("\n DataSet Metadata Descriptive Test")
        print("-"*40)        
        metadata = get_metadata
        desc = metadata.get('desc')
        desc.update()
        assert desc.get('updates') == 1, "Admin updates not correct."
        desc.add(key='artist', value='BOC')
        assert desc.get('artist') == 'BOC', "Admin get error."
        with pytest.raises(ValueError):        
            desc.add(key='artist', value='dunno')
        with pytest.raises(KeyError):        
            desc.change(key='cook', value='BOC')
        desc.change(key='artist', value='air')
        assert desc.get('artist') == 'air', "Admin change error."
        desc.remove(key='artist')
        with pytest.raises(KeyError):        
            assert desc.get('artist') == 'air', "Admin remove failed to raise Keyerror."
        assert isinstance(desc.get(), dict), "Get error, failed to return all desc metadata"

    @mark.metadata
    def test_metadata_system(self, get_metadata):
        print("\n DataSet Metadata System Test")
        print("-"*40)        
        metadata = get_metadata
        system = metadata.get('system')
        system.update()
        assert system.get('updates') == 1, "Admin updates not correct."
        system.add(key='artist', value='BOC')
        assert system.get('artist') == 'BOC', "Admin get error."
        with pytest.raises(ValueError):        
            system.add(key='artist', value='dunno')
        with pytest.raises(KeyError):        
            system.change(key='cook', value='BOC')
        system.change(key='artist', value='air')
        assert system.get('artist') == 'air', "Admin change error."
        system.remove(key='artist')
        with pytest.raises(KeyError):        
            assert system.get('artist') == 'air', "Admin remove failed to raise Keyerror."
        assert isinstance(system.get(), dict), "Get error, failed to return all system metadata"

        
               
        
