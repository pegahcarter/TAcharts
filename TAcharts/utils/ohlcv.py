#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
import TAcharts

import os
import pandas as pd


class OHLCV:

    baseurl = "https://raw.githubusercontent.com/carlfarterson/TAcharts/master/ohlcv"
    coins = ["btc", "eth", "ethusd", "xrp", "ltc", "eos", "ada"]

    # Check if we have already pulled the price data and saved it locally
    def __init__(self, usecols=None):

        self.basepath = TAcharts.__path__[0] + "/ohlcv"

        # If we have not yet saved OHLCV prices locally, fetch them from github
        if "ohlcv" not in os.listdir(self.basepath):
            self.fetch_OHLCV()
        # Now that we have OHLCV prices saved, fetch them and set themn to ourself
        for coin in self.coins:
            df = pd.read_csv(f"{self.basepath}/{coin}.csv")
            setattr(self, coin, df)

    # Download 1-hour CSV OHLCV files for 2019
    def fetch_OHLCV(self):
        # Create data directory first
        os.mkdir(self.basepath)
        # Fetch OHLCV data for each coin and save it locally
        for coin in self.coins:
            df = pd.read_csv(f"{self.baseurl}/{coin}.csv")
            df.to_csv(f"{self.basepath}/{coin}.csv", index=False)
