#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import pandas as pd



def plot(renko, num_bricks=None, signal_indices=None):

    prices = renko['price']
    directions = renko['direction']
    brick_size = renko['brick_size']

    # Limits display to a custom sized set
    if num_bricks:
        prices = prices[-num_bricks:]
        directions = directions[-num_bricks:]

    if signal_indices:
        for index in signal_indices:
            plt.axvline(x=index)

    # Create `fig` and `ax`
    fig, ax = plt.subplots(1, figsize=(10, 5))

    # Add title to chart
    fig.suptitle(f"Renko Chart (brick size = {round(brick_size, 2)})", fontsize=20)

    # Add label to Y-axis
    ax.set_ylabel('Price ($)')

    plt.rc('axes', labelsize=20)
    plt.rc('font', size=16)

    # Setup X-axis
    x_min = 0
    x_max = len(prices) + 1
    ax.set_xlim(x_min, x_max)

    # Setup Y-axis
    y_min = min(prices) - 2 * brick_size
    y_max = max(prices) + 2 * bricksize
    ax.set_ylim(y_min, y_max)

    # Add bricks to chart
    for x, (price, direction) in enumerate(zip(prices, directions)):

        # Setting brick color and y-position
        if direction == 1:
            facecolor='g'
            y = price - brick_size
        else:
            facecolor = 'r'
            y = price

        ax.add_patch(
            patches.Rectangle(
                (x+1, y),
                height=brick_size,
                width=1,
                facecolor=facecolor # Either Green or Red
            )  # end of patches.Rectangle
        )   # end of ax.add_patch

    return plt.show()
