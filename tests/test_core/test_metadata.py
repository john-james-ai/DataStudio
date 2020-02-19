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

from datastudio.core.data import DataStoreFile, DataSourceFile
from datastudio.core.data import DataSet, DataCollection

class MetaDataTests:
  
    @mark.metadata
    def test_datastorefile_metadata_build(self):

        print("\n\nDataStoreFile Metadata Object")
        print("="*40)
        datastore_path = "./tests/test_data/test_file/san_francisco.csv"
        name = 'sf_listings'
        ds = DataStoreFile(name, path=datastore_path)        
        metadata = ds.metadata
        metadata.print()

        print("\nDataStoreFile Admin Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='admin')
        admin = metadata.get('admin')              
        assert len(admin.get()) == 17, "DataStoreFile: Admin metadata error"         
        

        print("\nDataStoreFile Descriptive Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='desc')
        admin = metadata.get('desc')      
        assert len(admin.get()) == 3, "DataStoreFile: Desc metadata error"

        print("\nDataStoreFile Technical Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='tech')
        admin = metadata.get('tech')      
        assert len(admin.get()) == 14, "DataStoreFile: Tech metadata error"

        print("\nDataStoreFile Process Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='proc')
        admin = metadata.get('proc')      
        assert len(admin.get()) == 1, "DataStoreFile: Process metadata error"

    @mark.metadata
    def test_datasourcefile_metadata_build(self):

        print("\n\nDataSourceFile Metadata Object")
        print("="*40)
        datastore_path = "./tests/test_data/test_file/san_francisco.csv"
        name = 'sf_listings'
        ds = DataSourceFile(name, path=datastore_path)        
        metadata = ds.metadata
        metadata.print()

        print("\nDataSourceFile Admin Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='admin')
        admin = metadata.get('admin')              
        assert len(admin.get()) == 17, "DataSourceFile: Admin metadata error"         
        

        print("\nDataSourceFile Descriptive Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='desc')
        admin = metadata.get('desc')      
        assert len(admin.get()) == 3, "DataSourceFile: Desc metadata error"

        print("\nDataSourceFile Technical Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='tech')
        admin = metadata.get('tech')      
        assert len(admin.get()) == 14, "DataSourceFile: Tech metadata error"

        print("\nDataSourceFile Process Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='proc')
        admin = metadata.get('proc')      
        assert len(admin.get()) == 1, "DataSourceFile: Process metadata error"        
    
    @mark.metadata
    def test_dataset_metadata_build(self):

        print("\n\nDataSet Metadata Object")
        print("="*40)
        source_path = "./tests/test_data/test_file/san_francisco.csv"
        store_path = "./tests/test_data/test_file/san_francisco.xlsx"
        name = 'sf_listings'
        source = DataSourceFile(name, path=source_path)        
        store = DataStoreFile(name, path=store_path)  
        ds = DataSet(name=name, datasource=source, datastore=store)      
        metadata = ds.metadata
        metadata.print()

        print("\nDataSet Admin Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='admin')
        admin = metadata.get('admin')              
        assert len(admin.get()) == 9, "DataSet: Admin metadata error"         
        

        print("\nDataSet Descriptive Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='desc')
        admin = metadata.get('desc')      
        assert len(admin.get()) == 3, "DataSet: Desc metadata error"

        print("\nDataSet Technical Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='tech')
        admin = metadata.get('tech')      
        assert len(admin.get()) == 13, "DataSet: Tech metadata error"

        print("\nDataSet Process Metadata Object")
        print("-"*40)
        metadata.print(metadata_type='proc')
        admin = metadata.get('proc')      
        assert len(admin.get()) == 1, "DataSet: Process metadata error"        

    @mark.metadata_datacollections
    def test_datacollection_metadata_build(self, get_datasets):

        print("\n\nDataCollection Metadata Object")
        print("="*40)
        ds1, ds2 = get_datasets
        name = 'sf_nashville'
        dc = DataCollection(name=name, entity=ds1)
        metadata = dc.metadata        
        dc.print_members()
        dc.add(ds2)
        dc.print_members()
        