#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.utils.group_candles import group_candles

from .sma import sma
from .sdev import sdev

import pandas as pd
import os


class Bollinger:

    def __init__(self, df, date=None, filename=None, interval=None, n=14):

        if filename:
            filename_abs_path = f'{os.getcwd()}/{filename}'
            try:
                df = pd.read_csv(filename_abs_path)
            except:
                raise FileNotFoundError(f'{filename_abs_path}\n\nDoes not exist.')
        elif df is None:
            df = demo_df

        # Make all columns lowercase
        df.columns = [col.lower() for col in df]

        if interval:
            df = group_candles(df, interval)

        self._validate_data(df, n)

        df['date'] = df['date'].shift(1)
        self.df = df
        return


    def _validate_data(self, df, n):
        ''' Make sure we have more rows of data than the rolling average size '''

        if len(df) < n:
            raise AssertionError('Moving average cannot be larger than number of records.')


    def build(self, n=20, ndev=2):

        self.n = n
        self.ndev = ndev
        self.bollinger = {}

        # Create base simple moving average
        self.bollinger['sma'] = sma(df['close'], n=n)

        rng = ndev * sdev(df['close'], n=n)

        # Create upper and lower bands
        self.bollinger['h_band'] = self.bollinger['sma'] + rng
        self.bollinger['l_band'] = self.bollinger['sma'] - rng

        return self.bollinger
