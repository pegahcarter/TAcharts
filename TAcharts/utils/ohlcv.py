#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import TAcharts

import os
import io
import requests
import pandas as pd


class OHLCV:

    path = f'{TAcharts.__path__[0]}/data'
    url = 'https://raw.githubusercontent.com/carlfarterson/TAcharts/master/data/btc-2019.csv'

    def __init__(self, url=None, usecols=None):
        self.url = url
        self.usecols = usecols
        self._add_2019_hourly_ohlcv()

    def _add_2019_hourly_ohlcv(self):
        for csvfile in os.listdir(self.path):
            coin = csvfile[:csvfile.find('.')]
            df = pd.read_csv(f'{self.path}/{csvfile}', usecols=self.usecols)
            setattr(self, coin, df)


    def fetch_ohlcv(self, url=None, usecols=None):

        # No url provided means we use our btc price file
        # Fetch prices with URL provided
        content = requests.get(url).content
        ohlcv = pd.read_csv(io.StringIO(content.decode('utf-8')), usecols=usecols)
