#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import pd_series_to_np_array

import pandas as pd
import numpy as np

import numpy.lib.stride_tricks as stride_tricks


@pd_series_to_np_array
def rolling(src, n=2, fn=None, axis=1):
    """ Returns the rolling sum, max, or min for a list across n periods """

    if len(src) == 0:
        raise ValueError("`src` is length 0")
    # rolling sum
    if fn == "sum":
        _rolling = src.cumsum()
        _rolling[n:] = _rolling[n:] - _rolling[:-n]
        _rolling[:n] = 0
        return _rolling
    # rolling max, min, or mean
    elif fn in ["max", "min", "mean"]:
        shape = (len(src) - n + 1, n)
        strides = src.strides * 2
        src_strided = stride_tricks.as_strided(src, shape=shape, strides=strides)
        _rolling = np.zeros_like(src)
        _rolling[n - 1 :] = getattr(np, fn)(src_strided, axis=axis)
        return _rolling
    else:
        raise ValueError('Enter "sum", "max", "min", or "mean" as fn argument')
