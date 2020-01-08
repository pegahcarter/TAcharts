#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import matplotlib.pyplot as plt
import matplotlib.patches as patches



def plot():

    prices = self.renko['price']
    directions = self.renko['direction']
    brick_size = self.brick_price

    if 'num_bricks' in kwargs:
        prices = prices[-num_bricks:]
        directions = directions[-num_bricks:]

    if 'signal_indices' in kwargs:
        for x in kwargs.pop('signal_indices'):
            plt.axvline(x=x)


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
                facecolor=facecolor     # Either Green or Red
            )  # end of patches.Rectangle
        )   # end of ax.add_patch

    return plt.show()
