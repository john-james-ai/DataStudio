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
# Last Modified : Thursday, January 23rd 2020, 6:59:34 pm                     #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Tests DataLayer classes."""
import pytest
from pytest import mark

from datastudio.datalayer import *

class DatabaseTests:

    @mark.datalayer
    @mark.database
    def test_database_create(self):
        db = Database(name='TestDB')
        db.create()
        db.drop_db()
