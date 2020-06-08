#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import args_to_dtype

from .roc import roc
from .double_smooth import double_smooth

import pandas as pd


@args_to_dtype(pd.Series)
def tsi(src, slow=25, fast=13):
    """ Returns the "true strength indicator", which is used to determine overbought
    and oversold conditions, and warning of trend weakness through divergence. """

    _roc = roc(src, n=1)

    roc_double_smooth = double_smooth(_roc, slow=slow, fast=fast)
    roc_double_smooth_abs = double_smooth(abs(_roc), slow=slow, fast=fast)

    _tsi = (roc_double_smooth / roc_double_smooth_abs) * 100

    return _tsi
