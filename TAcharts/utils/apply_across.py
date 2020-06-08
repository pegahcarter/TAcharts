#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import pd_series_to_np_array

import numpy as np


@pd_series_to_np_array
def apply_across(*args, fn=None):
    # Apply function across every `i` index for multiple lists

    if len(args) <= 0:
        raise StandardError("Enter more than one argument.")
    elif fn == None:
        raise ValueError("Enter a function name.")

    applied_across = getattr(np, fn)(args, axis=0)

    return applied_across
