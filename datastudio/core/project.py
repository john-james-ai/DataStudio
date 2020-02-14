#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : project.py                                                        #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Friday, February 14th 2020, 10:50:17 am                     #
# Last Modified : Friday, February 14th 2020, 10:50:18 am                     #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
""" Creation and management of Project and Task classes. 

The DataStudio Project Model derives from the cross-industry process for
data mining, CRISP-DM [1]_ methodology. It is a robust, well-proven, yet
flexible framework for using analytics to solve business problems.

The CRISP-DM [1]_ methodology has six major phases including:  

    - Business Understanding
    - Data Understanding
    - Data Preparation
    - Modeling
    - Evaluation
    - Deployment

For the DataStudio package, we wil concern ourselves with the data 
understanding and data preparation phases.

The DataStudio Project Model is a two-tier hierarchy of Project and
Task related classes. Projects encapsulate all Task objects associated
with the data understanding and/or data preparation phases of the 
CRISP-DM [1]_ methodology. Reporting, and persistence behaviors are 
defined and managed at the Project level. Task classes capture the 
activities and associated  Entity, Analysis, and Service (EAS) classes 
that implement the core analysis and  data preparation functionality. 
The Task classes define the activities, or more specifically, the 
underlying (EAS) classes required to complete the associated task. The
Task classes also maintain references to supporting EAS classes.

Concretely, the following 12 classes define and implement the DataStudio
Project Framework.
    
    - Project : Container class for Task objects
    - Task : Abstract base class that defines the interface for Task* classes.    

    Data Understanding Task Classes
    ----------------------------------
    - TaskDataCollection : Data collection tasks
    - TaskDataSummary : Data summary tasks
    - TaskDataQuality : Data quality and verification tasks. 
    - TaskDataAnalysis : Univariate, Bivariate and Multivariate analysis tasks.

    Data Preparation Task Classes
    --------------------------------
    - TaskDataSelection : Data selection tasks
    - TaskDataCleaning : Tasks associated with data cleaning
    - TaskDataX4rm : Data transformation tasks
    - TaskDataImputation : Data imputation tasks
    - TaskDataEngineering : Feature engineering tasks 
    - TaskDataFormatting : Data formatting classes

References
----------
.. [1] Shearer, C. (2000) The CRISP-DM Model: The New Blueprint for Data Mining. 
   Journal of Data Warehousing, 5, 13-22.

"""
