#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : conftest.py                                                       #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Monday, January 20th 2020, 9:26:05 pm                       #
# Last Modified : Monday, January 20th 2020, 9:26:52 pm                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
# %%
import os

import numpy as np
from pytest import fixture

from .datastudio.base.file import File

@fixture(scope="session")
def get_numpy_arrays():
    a = np.arange(0,100)
    b = np.reshape(a, (25,4))
    c = np.logspace(0,100)
    d = np.reshape(c, (5,-1))
    e = np.array([a,b,c,d])
    return a, b, c, d, e

@fixture(scope='session')
def get_text():
    t1 = """Contrary to popular belief, Lorem Ipsum is not simply random.\n"""
    t2 = """Lorem ipsum dolor sit amet.\n"""
    t3 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam 
    vitae diam id ipsum lacinia congue eget sed nisi. Nam eget.\n"""
    tl = [t1, t2, t3]
    return t1, tl










    