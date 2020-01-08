#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from datetime import datetime, timedelta
import matplotlib.dates as mdates


import pandas as pd



class Ichimoku:

    def __init__(self, df=None, filename=None, period=None):

        if filename:
            df = pd.read_csv(os.getcwd() + '/' + filename)

        # Now that we have our df, make all headers lowercase
        df.columns = [col.lower() for col in df]

        if period:
            df = group_candles(df, period)

        self.df = df
        self.ichimoku = {}

        self._validate_data(period)


    def _validate_data(self, period):
        ''' Make sure we have enough data to form the cloud '''

        if period > len(self.df):
            raise AssertionError(f'Error: make sure the dataset has more than {period} rows.')


    def _extend_window(self, displacement):
        last_date = self.df['date'].iat[-1]
        window = last_date - self.df['date'].iat[-2]
        new_dates = [last_date + window*(1+i) for i in range(displacement)]
        self.df = self.df.append(pd.DataFrame(new_dates, columns=['date']), ignore_index=True, sort=False)
        return


    def _build_lines(self, **kwargs):
        for key, val in kwargs.items():
            high = sma(self.df['high'], val, 'max')
            low = sma(self.df['low'], val, 'min')
            self.ichimoku[key] = (high + low)/2
        return


    def _build_spans(self, senkou_b_period, displacement):
        self.ichimoku['chikou'] = self.df['close'].shift(-displacement)
        self.ichimoku['senkou_a'] = (self.ichimoku['tenkan'] + self.ichimoku['kijun']) / 2

        self._build_lines(senkou_b=senkou_b_period)

        self.ichimoku['senkou_a'] = self.ichimoku['senkou_a'].shift(displacement)
        self.ichimoku['senkou_b'] = self.ichimoku['senkou_b'].shift(displacement)

        for indicator in ['tenkan', 'kijun', 'chikou', 'senkou_a', 'senkou_b']:
            self.ichimoku[indicator] = self.ichimoku[indicator][senkou_b_period+displacement:]

        self.df = self.df[senkou_b_period+displacement:]
        return


    def build(self, tenkan_period, kijun_period, senkou_b_period, displacement):
        ''' Create Ichimoku data '''

        self._validate_data(senkou_b_period)
        self._extend_window(displacement)

        # Tenkan (conversion line) = (highest high + highest low)/2 for the past x periods
        # Kijun (base line) = (highest high + lowest low)/2 for the past x*3 periods
        self._build_lines(tenkan=tenkan_period, kijun=kijun_period)

        # Chikou (lagging span) = Current closing price time-shifted backwards x*3 periods
        # Senkou span A (leading span A) = (tenkan + kijun)/2 time-shifted forwards x*3 periods
        # Senkou span B (leading span B) = (highest high + lowest low)/2 for past x*6 periods, shifted forwards x*3 periods
        self._build_spans(senkou_b_period=senkou_b_period, displacement=displacement)

        return self.ichimoku
