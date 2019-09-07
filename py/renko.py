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


    def _optimize_brick_size(self, brick_size, atr_period):
        ''' Helper function to get optimal brick size based on ATR '''
        if not brick_size:
            atr = average_true_range(self.df['High'], self.df['Low'], self.df['Close'], atr_period)
            brick_size = atr.median()

        return brick_size


    def build(self):
        ''' Create Renko data '''
        for price in self.close[1:]:
            self._apply_renko(price)

        return self.renko


    def _apply_renko(self, price):
        pass


    def __repr__(self):
        return f"{self.renko}"
