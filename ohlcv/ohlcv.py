#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import TAcharts

import os
import io
import requests
import pandas as pd


class OHLCV:

    basepath = os.listdir(TAcharts.__path__[0])
    baseurl = 'https://raw.githubusercontent.com/carlfarterson/TAcharts/master/data/'
    coins = ['btc', 'eth', 'ethusd', 'xrp', 'ltc', 'eos', 'ada']

    # Check if we have already pulled the price data and saved it locally
    def __init__(self, usecols=None):
        # If we have not yet saved ohlcv prices locally, fetch them from github
        if 'ohlcv' not in os.listdir(basepath):
            self.fetch_ohlcv()
        # Now that we have ohlcv prices saved, fetch them and set themn to ourself
        for coin in self.coins:
            df = pd.read_csv(f'{self.basepath}/ohclv/{coin}.csv')
            setattr(self, coin, df)

    # Download 1-hour CSV OHLCV files for 2019
    def fetch_ohlcv(self):
        # Create data directory first
        os.mkdir(f'{basepath}/ohlcv')
        # Fetch ohlcv data for each coin and save it locally
        for coin in self.coins:
            df = pd.read_csv(f'{self.baseurl}{coin}.csv')
            df.to_csv(f'{basepath}/ohlcv/{coin}.csv)
