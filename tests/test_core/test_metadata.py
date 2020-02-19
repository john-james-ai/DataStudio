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

from datastudio.core.data import DataStoreFile

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

