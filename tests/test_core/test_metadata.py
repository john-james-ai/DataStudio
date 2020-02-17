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

from datastudio.core.metadata import Metadata, MetadataBuilder, MetadataDirector
from datastudio.core.metadata import MetadataAdmin, MetadataDesc, MetadataTech
from datastudio.core.metadata import MetadataProcess
class MetaDataTests:
  

    @mark.metadata
    def test_metadata_build(self):

        print("\n\nMetadata Object")
        print("="*40)
        director = MetadataDirector()
        builder = MetadataBuilder(self, name='test_object')
        director.builder = builder
        director.build()
        metadata = builder.metadata
        metadata.print_types()

        print("\n\nMetadata Administrative")
        print("-"*40)
        admin = metadata.get('admin')    
        admin.print()
        assert isinstance(admin, MetadataAdmin), "MetadataAdmin not built."
        
        print("\n\nMetadata Descriptive")
        print("-"*40)
        desc = metadata.get('desc')                
        desc.print()
        assert isinstance(desc, MetadataDesc), "MetadataDesc not built."

        print("\n\nMetadata Technical")
        print("-"*40)
        tech = metadata.get('tech')                
        tech.print()
        assert isinstance(tech, MetadataTech), "MetadataTech not built."

        print("\n\nMetadata Process")
        print("-"*40)
        process = metadata.get('process')                
        process.print()
        assert isinstance(process, MetadataProcess), "MetadataProcess not built."

        with pytest.raises(KeyError):
            metadata.get('xxx')

    @mark.metadata
    def test_metadata_admin(self, get_metadata):
        print("\n\nMetadata Administrative Test")
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
        print("\nMetadata Descriptive Test")
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
    def test_metadata_tech(self, get_metadata):
        print("\nMetadata Technical Test")
        print("-"*40)        
        metadata = get_metadata
        tech = metadata.get('tech')
        tech.update()
        assert tech.get('updates') == 1, "Admin updates not correct."
        tech.add(key='artist', value='BOC')
        assert tech.get('artist') == 'BOC', "Admin get error."
        with pytest.raises(ValueError):        
            tech.add(key='artist', value='dunno')
        with pytest.raises(KeyError):        
            tech.change(key='cook', value='BOC')
        tech.change(key='artist', value='air')
        assert tech.get('artist') == 'air', "Admin change error."
        tech.remove(key='artist')
        with pytest.raises(KeyError):        
            assert tech.get('artist') == 'air', "Admin remove failed to raise Keyerror."
        assert isinstance(tech.get(), dict), "Get error, failed to return all tech metadata"

        
               
        
