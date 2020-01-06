#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# TODO: imports

def double_smooth(src, slow=25, fast=13):
    ''' Returns the smoothed value of two EMAs '''

    first_smooth = ema(src, n=slow)
    _double_smooth = ema(first_smooth, n=fast)

    return _double_smooth.values
