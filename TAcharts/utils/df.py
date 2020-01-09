#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pandas as pd
import io
import requests

import os


class Df:
    def __init__(self, url=None, usecols=None):
        self.url = url
        self.usecols = usecols

    def use_url()


    def _add_2019_hourly_ohlcv(self, *coins)
        if url is None:
            # Provide BTC 2019 prices from local file
            # TODO: figure out how to reference package location
            _demo_df = pd.read_csv('/home/carter/Documents/TAcharts/data/btc-2019.csv')

        else:
            # Fetch prices with URL provided
            url = 'https://raw.githubusercontent.com/carlfarterson/TAcharts/master/data/btc-2019.csv'
            content = requests.get(url).content
            _demo_df = pd.read_csv(io.StringIO(content.decode('utf-8')))



    if usecols:
        # Only return columns requested
        return _demo_df[usecols]
    else:
        # return all columns
        return _demo_df
