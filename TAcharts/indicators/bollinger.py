#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.utils.group_candles import group_candles

from .sma import sma
from .sdev import sdev

import pandas as pd
import os


def bollinger(df=None, filename=None, interval=None, n=20, ndev=2):

    if filename:
        filename_abs_path = f'{os.getcwd()}/{filename}'
        try:
            df = pd.read_csv(filename_abs_path)
        except:
            raise FileNotFoundError(f'{filename_abs_path}\n\nDoes not exist.')

    # Make all columns lowercase
    df.columns = [col.lower() for col in df]

    if interval:
        df = group_candles(df, interval)

    # Make sure we have more rows of data than the size of the rolling average
    if len(df) < n:
        raise AssertionError('Rolling average cannot be larger than number of records.')

    df['date'] = df['date'].shift(1)

    _bollinger = {}

    # Create base simple moving average
    _bollinger['sma'] = sma(df['close'], n=n)

    rng = ndev * sdev(df['close'], n=n)

    # Create upper and lower bands
    _bollinger['h_band'] = _bollinger['sma'] + rng
    _bollinger['l_band'] = _bollinger['sma'] - rng

    return _bollinger
