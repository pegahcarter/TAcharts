#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import TAcharts

import os
import io
import requests
import pandas as pd


class OHLCV:

    url = 'https://github.com/carlfarterson/TAcharts/data/btc.csv'

    def __init__(self, url=url, usecols=None):
        self.url = url
        self.usecols = usecols
        self.btc = pd.read_csv('/home/carter/Documents/TAcharts/data/btc.csv', usecols=usecols)

    #     self._add_2019_hourly_ohlcv()
    #
    # def _add_2019_hourly_ohlcv(self):
        # path = f'{TAcharts.__path__[0]}/data'
    #     for csvfile in os.listdir(self.path):
    #         coin = csvfile[:csvfile.find('.')]
    #         df = pd.read_csv(f'{self.path}/{csvfile}', usecols=self.usecols)
    #         setattr(self, coin, df)


    def fetch_ohlcv(self, url=None, usecols=None):

        # No url provided means we use our btc price file
        # Fetch prices with URL provided
        content = requests.get(url).content
        _fetch_ohlcv = pd.read_csv(io.StringIO(content.decode('utf-8')), usecols=usecols)
        self.ohlcv = _fetch_ohlcv
        return _fetch_ohlcv
