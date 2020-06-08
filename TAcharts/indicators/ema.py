#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import args_to_dtype

import pandas as pd


@args_to_dtype(pd.Series)
def ema(src, n=2):
    """ Returns the "exponential moving average" for a list """

    _ema = src.ewm(span=n, min_periods=1, adjust=False).mean()

    return _ema.values
