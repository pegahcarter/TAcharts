import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from py.utils import *


class Renko:
    def __init__(self, FILEPATH='../data/15min.csv'):
        self.df = pd.read_csv(FILEPATH)
        self.close = iter(self.df['Close'])
        self.renko = {
            'prices': [next(self.close)],
            'directions': [0]
        }


    def set_brick_size(self, brick_size=None, atr_period=14):
        ''' Setting brick size '''
        if len(self.df) < atr_period:
            raise ValueError('ATR period is longer than historical data.')

        self.brick_size = self._optimize_brick_size(brick_size, atr_period)
        return self.brick_size


    def _optimize_brick_size(self, brick_size, atr_period):
        ''' Helper function to get optimal brick size based on ATR '''
        if not brick_size:
            atr = average_true_range(self.df['High'], self.df['Low'], self.df['Close'], atr_period)
            brick_size = atr.median()

        return brick_size


    def build(self):
        ''' Create Renko data '''
        while self.close:
            price = next(self.close)
            self._apply_renko(price)

        return self.renko


    def _apply_renko(self, price):
        ''' Determine if there are any new bricks to paint with current price '''
        num_bricks = 0
        gap = (price - self.renko.prices[-1]) // self.brick_size
        # No gap means there's not a new brick
        if gap == 0:
            return
        # Add brick(s) in the same direction
        if (gap > 0 and self.renko.directions[-1] >= 0) \
        or (gap < 0 and self.renko.directions[-1] <= 0):
            num_bricks = gap
        # Gap >= 2 or -2 and opposite renko direction means we're switching brick direction
        elif abs(gap) >= 2:
            num_bricks = gap - np.sign(gap)
            self._update_renko(gap, 2)

        return [self._update_renko(gap) for brick in range(num_bricks)]


    def _update_renko(self, gap, brick_multiplier=1):
        ''' Append price and new block to renko dict '''
        renko_price = self.renko.prices[-1] + brick_multiplier*self.brick_size*np.sign(gap)
        self.renko.prices.append(renko_price)
        self.renko.directions.append(np.sign(gap))


    def __repr__(self):
        return f"{self.renko}"
