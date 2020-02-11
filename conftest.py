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

from datastudio.file import File
USECOLS = ["id", "host_id",
            "host_response_rate",
            "host_total_listings_count",
            "host_response_time",
            "host_neighbourhood",
            "host_since",
            "host_is_superhost",
            "host_location",
            "city",
            "zipcode",
            "state",
            "market",
            "neighbourhood_cleansed",
            "accommodates",
            "bed_type",
            "square_feet",
            "beds",
            "room_type",
            "bedrooms",
            "bathrooms",
            "guests_included",
            "property_type",
            "amenities",
            "is_business_travel_ready",
            "maximum_nights",
            "availability_30",
            "minimum_nights",
            "experiences_offered",
            "cleaning_fee",
            "extra_people",
            "price",
            "security_deposit",
            "cancellation_policy",
            "review_scores_cleanliness",
            "review_scores_location",
            "review_scores_communication",
            "review_scores_accuracy",
            "review_scores_rating",
            "review_scores_checkin",
            "number_of_reviews_ltm",
            "reviews_per_month",
            "review_scores_value",
            "license",
            "host_verifications",
            "require_guest_phone_verification",
            "require_guest_profile_picture",
            "host_identity_verified",
            "instant_bookable",
            "requires_license",
            "host_has_profile_pic",
            "last_scraped",
            "calculated_host_listings_count_entire_homes",
            "calculated_host_listings_count_private_rooms",
            "calculated_host_listings_count_shared_rooms",
            "reviews_per_month"]

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

@fixture(scope='session')
def get_dfs():
    nash = "./tests/test_data/test_file/nashville.csv"
    sf = "./tests/test_data/test_file/san_francisco.csv"
    fn = File(path=nash, name="Nashville")
    fsf = File(path=sf, name='San Francisco')
    dfn = fn.read(filter=USECOLS)
    dfsf = fsf.read(filter=USECOLS)
    dfs = [dfn, dfsf]
    return dfs











    