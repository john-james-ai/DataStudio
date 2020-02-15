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

from datastudio.core.metadata import MetaDataAdmin, MetaDataDesc
from datastudio.core.metadata import MetaDataTech
class MetaDataTests:

    @mark.metadata
    def test_metadata_admin(self):
        print("\n\nMetaData Admin Testing ")
        print("="*40)
        metadata = MetaDataAdmin(self)
        metadata1 = metadata.get_metadata()
        print("\nAdministrative metadata before update")
        print(metadata1)
        assert isinstance(metadata1, dict), "Metadata admin didn't return a dict"

        time.sleep(2)

        metadata.update_metadata()
        metadata2 = metadata.get_metadata()
        print("\nAdministrative metadata after update")
        print(metadata2)
        assert metadata1 != metadata2, "Metadata admin didn't update"

    @mark.metadata
    def test_metadata_desc(self):
        print("\n\nMetaData Desc Testing ")
        print("="*40)
        name = 'metadata_desc'
        metadata = MetaDataDesc(self, name)
        metadata1 = metadata.get_metadata()
        print("\nDescriptive metadata before update")
        print(metadata1)
        assert isinstance(metadata1, dict), "Metadata desc didn't return a dict"
        
        time.sleep(2)
        
        metadata.name = 'new name'
        metadata.description = 'new description'
        metadata2 = metadata.get_metadata()        
        print("\nDescriptive metadata after update")
        print(metadata2)
        assert metadata1 != metadata2, "Metadata desc didn't update"

    @mark.metadata
    def test_metadata_tech(self):
        print("\n\nMetaData Tech Testing ")
        print("="*40)
        metadata = MetaDataTech(self)
        metadata1 = metadata.get_metadata()
        print("\nTechnical metadata before update")
        print(metadata1)
        assert isinstance(metadata1, dict), "Metadata tech didn't return a dict"
        
        # Memory consumption function
        test_str = ' ' * 512000000
        
        metadata.update_metadata()
        metadata2 = metadata.get_metadata()
        print("\nTechnical metadata after update")
        print(metadata2)
        assert metadata1 != metadata2, "Metadata tech didn't update"
        



