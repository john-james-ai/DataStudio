#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : test_datalayer.py                                                 #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Thursday, January 23rd 2020, 6:59:18 pm                     #
# Last Modified : Monday, February 3rd 2020, 6:09:02 pm                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Tests DataLayer classes."""
import pytest
from pytest import mark

from datastudio.datalayer import *


class DataTableTests:
    
    @mark.datalayer
    @mark.datatable
    def test_datatable_name(self):
        dt = DataTable(name='TestTable')
        name = dt.name
        assert name == 'TestTable', "Name property not working on DataTable"

    @mark.datalayer
    @mark.datatable
    def test_datatable_create(self, get_dfs):
        dfs = get_dfs
        dt = DataTable(name='TestTable')
        dt.create(dfs[0])



class DatabaseTests:

    @mark.datalayer
    @mark.database
    def test_database_name(self):
        db = Database(name='TestDB')
        name = db.name
        assert name == 'TestDB', "Name property not working on DataBase"  


    @mark.datalayer
    @mark.database
    def test_database_create(self):
        db = Database(name='TestDB')
        db.create()     

    @mark.datalayer
    @mark.database
    def test_database_delete(self):
        db = Database(name='TestDB')        
        db.delete()

