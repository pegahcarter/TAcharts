#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.utils.demo_df import demo_df

from .atr import atr

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np
import pandas as pd
import os


class Renko:
    def __init__(self, df=None, filename=None, interval=None):
        if filename:
            filename_abs_path = f"{os.getcwd()}/{filename}"
            try:
                df = pd.read_csv(filename_abs_path)
            except:
                raise FileNotFoundError(f"{filename_abs_path}\n\nDoes not exist.")
        elif df is None:
            try:
                df = demo_df()
            except:
                return f"Figure out a dataset or connect to the internet, ya goof"

        # Group candles if necessary
        if interval:
            df = group_candles(df, interval)

        # Shift date once to account for close
        df["date"] = df["date"].shift(1)

        self.df = df

    def set_brick_size(self, brick_size=None, auto=True, atr_interval=14):
        """ Setting brick size """

        if len(self.df) < atr_interval:
            raise ValueError("ATR interval is longer than historical data.")

        self.brick_size = self._optimize_brick_size(auto, brick_size, atr_interval)
        return self.brick_size

    def _optimize_brick_size(self, auto, brick_size, atr_interval):
        """ Helper function to get optimal brick size based on ATR """

        if auto and not brick_size:
            average_true_range = atr(
                self.df["high"], self.df["low"], self.df["close"], n=atr_interval
            )
            brick_size = np.median(average_true_range)
        return brick_size

    def _apply_renko(self, i):
        """ Determine if there are any new bricks to paint with current price """

        num_bricks = 0

        gap = (self.close[i] - self.renko["price"][-1]) // self.brick_size
        direction = np.sign(gap)
        # No gap means there's not a new brick
        if direction == 0:
            return
        # Add brick(s) in the same direction
        if (gap > 0 and self.renko["direction"][-1] >= 0) or (
            gap < 0 and self.renko["direction"][-1] <= 0
        ):
            num_bricks = gap
        # Gap >= 2 or -2 and opposite renko direction means we're switching brick direction
        elif np.abs(gap) >= 2:
            num_bricks = gap - 2 * direction
            self._update_renko(i, direction, 2)

        for brick in range(abs(int(num_bricks))):
            self._update_renko(i, direction)

        return

    def _update_renko(self, i, direction, brick_multiplier=1):
        """ Append price and new block to renko dict """

        renko_price = self.renko["price"][-1] + (
            direction * brick_multiplier * self.brick_size
        )
        self.renko["index"].append(i)
        self.renko["price"].append(renko_price)
        self.renko["direction"].append(direction)
        self.renko["date"].append(self.df["date"].iat[i])
        return

    def build(self):
        """ Create Renko data """

        units = self.df["close"].iat[0] // self.brick_size
        start_price = units * self.brick_size

        # Create Genesis block
        self.renko = {
            "index": [0],
            "date": [self.df["date"].iat[0]],
            "price": [start_price],
            "direction": [0],
        }

        # Run price feed through our renko model
        for i in range(1, len(self.close)):
            self._apply_renko(i)

        return self.renko

    def plot(self, num_bricks=None, signal_indices=None):

        prices = self.renko["price"]
        directions = self.renko["direction"]
        brick_size = self.renko["brick_size"]

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
        ax.set_ylabel("Price ($)")

        plt.rc("axes", labelsize=20)
        plt.rc("font", size=16)

        # Setup X-axis
        x_min = 0
        x_max = len(prices) + 1
        ax.set_xlim(x_min, x_max)

        # Setup Y-axis
        y_min = min(prices) - 2 * brick_size
        y_max = max(prices) + 2 * brick_size
        ax.set_ylim(y_min, y_max)

        # Add bricks to chart
        for x, (price, direction) in enumerate(zip(prices, directions)):

            # Setting brick color and y-position
            if direction == 1:
                facecolor = "g"
                y = price - brick_size
            else:
                facecolor = "r"
                y = price

            ax.add_patch(
                patches.Rectangle(
                    (x + 1, y),
                    height=brick_size,
                    width=1,
                    facecolor=facecolor,  # Either Green or Red
                )  # end of patches.Rectangle
            )  # end of ax.add_patch

        return plt.show()
