#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import numpy as np


def fill_values(averages, interval):
    """ Fill missing values with evenly spaced samples.

    Example: You're using 15-min candlestick data but want to include a 1-hour moving
        average with a value at every 15-min mark, and not just every 1-hour mark.
    """

    # Combine every two values with the number of intervals between each value
    avgs_zip = zip(
        averages[:-1], averages[1:], itertools.repeat(interval), itertools.repeat(False)
    )

    # Generate evenly-spaced samples between every point
    avgs_gen = (np.linspace(*x, end) for x in avgs_zip)

    # Unpack all values into one list
    _fill_values = list(itertools.chain.from_iterable(avgs_gen))

    return _fill_values
