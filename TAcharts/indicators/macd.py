#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

# TODO: fix imports

def macd(src, slow=25, fast=13):
    ''' Returns the "moving average convergence/divergence" (MACD) '''

    ema_fast = ema(src, fast)
    ema_slow = ema(src, slow)
    _macd = ema_fast.values - ema_slow.values

    return _macd
