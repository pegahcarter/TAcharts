#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .sma import sma
from .sdev import sdev

from TAcharts.utils.group_candles import group_candles

import os


class Bollinger:

    def __init__(self, df, date=None, interval=None):

        self.bollinger = {}
        self.date = date

        if interval:
            df = group_candles(df, interval)
        self.df = df


    def _validate_data(self):
        ''' Make sure we have more rows of data than the rolling average size '''

        if self.n > len(df['close']):
            raise AssertionError('Moving average cannot be larger than number of records.')


    def _apply_bollinger(self):
        self.bollinger['sma'] = sma(df['close'], window=self.n)
        rng = self.ndev * sdev(df['close'], window=self.n)

        self.bollinger['h_band'] = self.bollinger['sma'] + rng
        self.bollinger['l_band'] = self.bollinger['sma'] - rng


    def build(self, n=20, ndev=2):
        self.n = n
        self.ndev = ndev

        self._validate_data()
        self._apply_bollinger()

        return self.bollinger
