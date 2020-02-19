#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : lab.py                                                            #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Wednesday, February 19th 2020, 5:49:14 am                   #
# Last Modified : Wednesday, February 19th 2020, 5:49:16 am                   #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
#%%
from abc import ABC
class Foo(ABC):
    def __init__(self, name, *args, **kwargs):
        print(name, *args, **kwargs)

class Bar(Foo):
    def __init__(self, name, *args, **kwargs):
        super(Bar, self).__init__(name, args, kwargs)
        f = Far(name, args, kwargs)        

class Far:
    def __init__(self, name, *args, **kwargs):
        print(name, *args, **kwargs)

class Boo:
    def __init__(self, name, path):
        print(name, path)
b = Bar('some name', path = 'some_path')
path = "path boo"
c = Boo('boo name', **path)
#%%
d = {'one': 1, 'two': 2, 'three': 3}
d2 = {'five': 5, 'six': 6}
print(next((k,v) for (k, v) in d.items() if 'on' in k))
res = dict(filter(lambda item: 'on' in item[0], d.items())) 
print(res)
d2.update(res)
print(d2)
# %%
