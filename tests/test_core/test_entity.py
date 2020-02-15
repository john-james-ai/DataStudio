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
    def test_entity_metadata(self):
        entity = Entity('Entity Object')
        
        # Evaluate get_data
        metadata = entity.get_metadata()
        assert len(metadata) == 3, "Metadata not correct length."        
        admin = metadata['admin']
        print(admin)        
        assert isinstance(admin, dict), "Didn't return admin metadata dict"
        desc = metadata['desc']
        print(desc)
        assert isinstance(desc, dict), "Didn't return desc metadata dict"        
        tech = metadata['tech']
        print(tech)
        assert isinstance(tech, dict), "Didn't return tech metadata dict"  
        
        time.sleep(5)
        
        # Test update metadata
        entity.update_metadata()
        metadata = entity.get_metadata() 
        assert len(metadata) == 3, "Metadata not correct length."        
        admin2 = metadata['admin']        
        assert isinstance(admin2, dict), "Didn't return admin metadata dict"
        # assert admin != admin2, "Admin metadata update not working"        
        tech2 = metadata['tech']        
        assert isinstance(tech, dict), "Didn't return tech metadata dict"  
        assert tech != tech2, "Tech metadata update not working"        