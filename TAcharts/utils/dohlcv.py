#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
import TAcharts

import os
import pandas as pd



class DOHLCV:

    baseurl = 'https://raw.githubusercontent.com/carlfarterson/TAcharts/master/dohlcv'
    coins = ['btc', 'eth', 'ethusd', 'xrp', 'ltc', 'eos', 'ada']

    # Check if we have already pulled the price data and saved it locally
    def __init__(self, usecols=None):

        self.basepath = TAcharts.__path__[0]

        # If we have not yet saved DOHLCV prices locally, fetch them from github
        if 'dohlcv' not in os.listdir(self.basepath):
            self.fetch_DOHLCV()
        # Now that we have DOHLCV prices saved, fetch them and set themn to ourself
        for coin in self.coins:
            df = pd.read_csv(f'{self.basepath}/dohlcv/{coin}.csv')
            setattr(self, coin, df)

    # Download 1-hour CSV DOHLCV files for 2019
    def fetch_DOHLCV(self):
        # Create data directory first
        os.mkdir(f'{self.basepath}/dohlcv')
        # Fetch DOHLCV data for each coin and save it locally
        for coin in self.coins:
            df = pd.read_csv(f'{self.baseurl}/{coin}.csv')
            df.to_csv(f'{self.basepath}/dohlcv/{coin}.csv', index=False)
