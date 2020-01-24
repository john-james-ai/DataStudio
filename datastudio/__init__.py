#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : __init__.py                                                       #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Saturday, January 18th 2020, 1:08:34 pm                     #
# Last Modified : Friday, January 24th 2020, 12:15:50 pm                      #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Top-level package for Data Studio."""
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler

__author__ = """John James"""
__email__ = 'jjames@decisionscients.com'
__version__ = '0.1.0'

# Instantiate logger
LOG_FILENAME = "datastudio.log"
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Setup rotating file handler
fh = TimedRotatingFileHandler(filename=LOG_FILENAME, when='midnight')
fh.setLevel(logging.DEBUG)

# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# Add handlers to Logger
log.addHandler(fh)
log.addHandler(ch)
log.info("Logger configuration complete!")