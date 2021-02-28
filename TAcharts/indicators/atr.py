#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import pd_series_to_np_array

from .rolling import rolling
from .sma import sma

import numpy as np
import pandas as pd


@pd_series_to_np_array
def atr(high, low, close, n=14):
    """ Returns the average true range from candlestick data """

    prev_close = np.insert(close[:-1], 0, 0)
    # True range is largest of the following:
    #   a. Current high - current low
    #   b. Absolute value of current high - previous close
    #   c. Absolute value of current low - previous close
    true_range = np.max([high - low, abs(high - prev_close), abs(low - prev_close)])
    true_range = rolling(
        high - low, abs(high - prev_close), abs(low - prev_close), fn="max", n=1, axis=0
    )

    _atr = sma(true_range, n)

    return _atr
