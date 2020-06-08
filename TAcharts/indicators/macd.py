#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import args_to_dtype
from .ema import ema

import pandas as pd


@args_to_dtype(pd.Series)
def macd(src, slow=25, fast=13):
    """ Returns the "moving average convergence/divergence" (MACD) """

    ema_fast = ema(src, n=fast)
    ema_slow = ema(src, n=slow)
    _macd = ema_fast - ema_slow

    return _macd
