#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import args_to_dtype

import numpy as np


@args_to_dtype(list)
def rsi(src, n=2):
    """ Returns the "relative strength index", which is used to measure the velocity
    and magnitude of directional price movement. """

    deltas = np.diff(src)
    seed = deltas[: n + 1]
    up = seed[seed > 0].sum() / n
    down = -seed[seed < 0].sum() / n

    _rsi = np.zeros_like(src)
    _rsi[:n] = 100.0 - 100.0 / (1.0 + up / down)

    for i in range(n, len(src)):
        delta = deltas[i - 1]
        if delta > 0:
            up_val = delta
            down_val = 0
        else:
            up_val = 0
            down_val = -delta

        up = (up * (n - 1) + up_val) / n
        down = (down * (n - 1) + down_val) / n

        _rsi[i] = 100.0 - 100.0 / (1.0 + up / down)

    return _rsi
