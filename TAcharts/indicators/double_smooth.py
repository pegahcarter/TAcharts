#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import args_to_dtype
from .ema import ema

import pandas as pd


@args_to_dtype(pd.Series)
def double_smooth(src, slow=25, fast=13):
    """ Returns the smoothed value of two EMAs """

    first_smooth = ema(src, n=slow)
    _double_smooth = ema(first_smooth, n=fast)

    return _double_smooth
