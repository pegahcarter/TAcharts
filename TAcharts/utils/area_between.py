#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import pd_series_to_np_array

import numpy as np


@pd_series_to_np_array
def area_between(line1, line2):
    """ Return the area between line1 and line2 """

    diff = line1 - line2
    x1 = diff[:-1]
    x2 = diff[1:]

    triangle_area = sum(abs(x2 - x1) * 0.5)
    square_area = sum(np.min(zip(x1, x2), axis=1))
    _area_between = triangle_area + square_area

    return _area_between
