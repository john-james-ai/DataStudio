#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : test_entity.py                                                    #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 15th 2020, 1:50:55 am                    #
# Last Modified : Saturday, February 15th 2020, 1:51:12 am                    #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Unit test for Entity class."""
import numpy as np
import pandas as pd
import pytest
from pytest import mark
import time

from datastudio.core.entity import Entity
from datastudio.core.metadata import MetaDataAdmin, MetaDataDesc
from datastudio.core.metadata import MetaDataTech
class EntityTests:

    @mark.entity
    def test_entity_metadata_admin(self):        
        entity = Entity('Entity Object')
        
        # Test admin metadata
        metadata1 = entity.get_metadata()
        print("\n\nMetaData Admin Testing ")
        print("="*40)
        print("\nAdministrative metadata before update")
        print(metadata1['admin'])
        assert isinstance(metadata1['admin'], dict), "Metadata admin didn't return a dict"

        time.sleep(2)

        entity.update_metadata()
        metadata2 = entity.get_metadata()
        print("\nAdministrative metadata after 1st update")
        print(metadata2['admin'])
        assert isinstance(metadata2['admin'], dict), "Metadata admin didn't return a dict"
        assert metadata1['admin'] != metadata2['admin'], "Metadata admin didn't update"        

        time.sleep(2)

        entity.update_metadata_admin()
        metadata3 = entity.get_metadata_admin()
        print("\nAdministrative metadata after 2nd update")
        print(metadata3)        
        assert isinstance(metadata3, dict), "Metadata admin - get.metadata.admin not dict"
        assert metadata2['admin'] != metadata3, "Metadata admin - update.metadata.admin not working"        

    @mark.entity
    def test_entity_metadata_desc(self):
        entity = Entity('Entity Object')
        
        # Test desc metadata
        metadata1 = entity.get_metadata()
        print("\n\nMetaData Descriptive Testing ")
        print("="*40)
        print("\nDescriptive metadata before update")
        print(metadata1['desc'])
        assert isinstance(metadata1['desc'], dict), "Metadata desc didn't return a dict"
        
        entity.name = 'newname'
        entity.description = 'some new description'
        entity.version = '99'

        metadata2 = entity.get_metadata_desc()
        print("\nDescriptive metadata after update")
        print(metadata2)
        assert isinstance(metadata2, dict), "Metadata desc didn't return a dict"
        assert metadata1['desc'] != metadata2, "Metadata desc property updates not working"        

    @mark.entity
    def test_entity_metadata_tech(self):
        entity = Entity('Entity Object')
        
        # Test tech metadata
        metadata1 = entity.get_metadata()
        print("\n\nMetaData Technical Testing ")
        print("="*40)
        print("\nTechnical metadata before update")
        print(metadata1['tech'])
        assert isinstance(metadata1['tech'], dict), "Metadata tech didn't return a dict"
        
        # Memory consumption function
        test_str = ' ' * 512000000

        entity.update_metadata_tech()
        metadata2 = entity.get_metadata_tech()
        print("\nTechnical metadata after update")
        print(metadata2)
        assert isinstance(metadata2, dict), "Metadata tech didn't return a dict"
        assert metadata1['tech'] != metadata2, "Metadata tech property updates not working"        

    @mark.entity
    def test_entity_metadata_print(self):
        entity = Entity('Entity Object')
        
        print("\n\nMetaData Print Testing ")
        print("="*40)
        print("\nPrinting admin metadata")
        entity.print_metadata_admin()
        print("\nPrinting desc metadata")
        entity.print_metadata_desc()
        print("\nPrinting tech metadata")
        entity.print_metadata_tech()
        print("\n\nPrinting all metadata")
        entity.print_metadata()
        
        
                