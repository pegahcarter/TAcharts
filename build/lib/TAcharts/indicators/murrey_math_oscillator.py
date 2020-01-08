#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# TODO: imports

@pd_series_to_np_array
def murrey_math_oscillator(src, n=2):
    ''' Returns the Murrey Math Oscillator of the close '''

    # Donchian channel
    highest = rolling(src, fn='max', n=n)
    lowest = rolling(src, fn='min', n=n)

    rng = highest - lowest

    # Oscillator
    rng_multiplier = rng * .125
    midline = lowest + rng_multiplier * 4

    _murrey_math_oscillator = (src - midline) / rng
    _murrey_math_oscillator[:n] = 0

    return _murrey_math_oscillator
