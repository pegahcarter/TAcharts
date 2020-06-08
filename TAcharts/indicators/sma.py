#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import pd_series_to_np_array

from .rolling import rolling


@pd_series_to_np_array
def sma(src, n=2):
    """ Returns the "simple moving average" for a list across n periods"""

    summed = rolling(src, fn="sum", n=n)
    _sma = summed / n

    return _sma
