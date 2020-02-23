#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : test_print.py                                                     #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Saturday, February 22nd 2020, 11:40:42 pm                   #
# Last Modified : Saturday, February 22nd 2020, 11:40:42 pm                   #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Unit Centrality tests."""
import numpy as np
import pandas as pd
import pytest
from pytest import mark
import time

from datastudio.utils.print import Printer
class UnivariateCentralityTests:
  
    @mark.printer
    def test_printer(self, get_dict, get_dict_of_lists):
        d = get_dict
        dol = get_dict_of_lists
        title = "Some Random Title"
        p = Printer()
        p.print_dictionary(d, title)
        p.print_table(dol,title) 
