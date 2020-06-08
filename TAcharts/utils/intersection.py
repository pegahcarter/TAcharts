#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


def intersection(a0, a1, b0, b1):
    """ Return the intersection coordinates between vector A and vector B """

    a_diff = a1 - a0
    b_diff = b1 - b0

    pos0_diff = float(a0 - b0)

    x = pos0_diff / (b_diff - a_diff)
    y = b_diff * x + b0

    return x, y
