#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import pd_series_to_np_array

from .rolling import rolling


@pd_series_to_np_array
def mmo(src, n=2):
    """ Returns the Murrey Math Oscillator of the close """

    # Donchian channel
    highest = rolling(src, fn="max", n=n)
    lowest = rolling(src, fn="min", n=n)

    rng = highest - lowest

    # Oscillator
    rng_multiplier = rng * 0.125
    midline = lowest + rng_multiplier * 4

    _mmo = (src - midline) / rng
    _mmo[:n] = 0

    return _mmo
