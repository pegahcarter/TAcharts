#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.utils.demo_df import demo_df

from .atr import atr

import numpy as np
import pandas as pd
import os


class renko:
    def __init__(self, df=None, filename=None, interval=None):
        if filename:
            filename_abs_path = f'{os.getcwd()}/{filename}'
            try:
                df = pd.read_csv(filename_abs_path)
            except:
                raise FileNotFoundError(f'{filename_abs_path}\n\nDoes not exist.')
        elif df is None:
            try:
                df = demo_df()
            except:
                return f'Figure out a dataset or connect to the internet, ya goof'

        # Group candles if necessary
        if interval:
            df = group_candles(df, interval)

        # Shift date once to account for close
        df['date'] = df['date'].shift(1)
        
        self.df = df


    def set_brick_size(self, brick_size=None, auto=True, atr_interval=14):
        ''' Setting brick size '''

        if len(self.df) < atr_interval:
            raise ValueError('ATR interval is longer than historical data.')

        self.brick_size = self._optimize_brick_size(auto, brick_size, atr_interval)
        return self.brick_size


    def _optimize_brick_size(self, auto, brick_size, atr_interval):
        ''' Helper function to get optimal brick size based on ATR '''

        if auto and not brick_size:
            average_true_range = atr(self.df['high'], self.df['low'], self.df['close'], n=atr_interval)
            brick_size = np.median(average_true_range)
        return brick_size


    def _apply_renko(self, i):
        ''' Determine if there are any new bricks to paint with current price '''

        num_bricks = 0

        gap = (self.close[i] - self.renko['price'][-1]) // self.brick_size
        direction = np.sign(gap)
        # No gap means there's not a new brick
        if direction == 0:
            return
        # Add brick(s) in the same direction
        if (gap > 0 and self.renko['direction'][-1] >= 0) \
        or (gap < 0 and self.renko['direction'][-1] <= 0):
            num_bricks = gap
        # Gap >= 2 or -2 and opposite renko direction means we're switching brick direction
        elif np.abs(gap) >= 2:
            num_bricks = gap - 2*direction
            self._update_renko(i, direction, 2)

        for brick in range(abs(int(num_bricks))):
            self._update_renko(i, direction)

        return


    def _update_renko(self, i, direction, brick_multiplier=1):
        ''' Append price and new block to renko dict '''

        renko_price = self.renko['price'][-1] + (direction * brick_multiplier * self.brick_size)
        self.renko['index'].append(i)
        self.renko['price'].append(renko_price)
        self.renko['direction'].append(direction)
        self.renko['date'].append(self.df['date'].iat[i])
        return


    def build(self):
        ''' Create Renko data '''

        units = self.df['close'].iat[0] // self.brick_size
        start_price = units * self.brick_size

        # Create Genesis block
        self.renko = {
            'index': [0],
            'date': [self.df['date'].iat[0]],
            'price': [start_price],
            'direction': [0]
        }

        # Run price feed through our renko model
        for i in range(1, len(self.close)):
            self._apply_renko(i)

        return self.renko
