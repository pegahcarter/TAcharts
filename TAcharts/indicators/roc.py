#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import pd_series_to_np_array

import numpy as np


@pd_series_to_np_array
def roc(src, n=2):
    """ Returns the rate of change in price over n periods """

    _roc = np.zeros_like(src)
    _roc[n:] = (np.diff(src, n)) / src[:-n]

    return _roc
