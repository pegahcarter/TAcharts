#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import args_to_dtype

from .rolling import rolling

import pandas as pd


@args_to_dtype(pd.DataFrame)
def cmf(df, n=2):
    ''' Returns the Chaikin Money Flow of a OHLCV dataframe'''

    high = df['high'].values
    low = df['low'].values
    close = df['close'].values
    volume = df['volume'].values

    avg = (2*close - high - low) / (high - low + .000000001) * volume

    avg_roll = rolling(avg, fn='sum', n=n)
    vol_roll = rolling(volume, fn='sum', n=n)

    _chaikin_money_flow = avg_roll / vol_roll
    _chaikin_money_flow[:n] = 0

    return _chaikin_money_flow
