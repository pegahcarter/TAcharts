#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import pandas as pd
import numpy as np


def group_candles(df, interval):
    ''' Combine candles so instead of needing one dataset for each time interval,
        you can form time intervals using more precise data.

    Example: You have 15-min candlestick data but want to test a strategy based
        on 1-hour candlestick data  (interval=4).
    '''

    columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    candles = df[columns].values
    results = []
    for i in range(0, len(df)-interval, interval):
        results.append([
            candles[i, 0],                      # date
            candles[i, 1],                      # open
            candles[i:i+interval, 2].max(),     # high
            candles[i:i+interval, 3].min(),     # low
            candles[i+interval, 4],             # close
            candles[i:i+interval, 5].sum()      # volume
        ])
    return pd.DataFrame(results, columns=columns)
