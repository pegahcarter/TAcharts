#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.wrappers import pd_series_to_np_array

import numpy as np


@pd_series_to_np_array
def td_sequential(src, n=2):
    """ Returns the TD sequential of the close """

    old_gt_new = src[:-n] > src[n:]
    diff_lst = np.diff(old_gt_new)
    diff_lst = np.insert(diff_lst, 0, False)

    _td_sequential = [0 for _ in range(n)]

    for diff in diff_lst:
        if not diff:
            _td_sequential.append(_td_sequential[-1] + 1)
        else:
            _td_sequential.append(1)

    return _td_sequential
