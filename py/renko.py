import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from renko.py.average_true_range import average_true_range


class Renko:
    def __init__(self, FILEPATH, atr_period):
        self.df = pd.read_csv(FILEPATH)
        self.renko_prices = []
        self.source_prices = []
        self.renko_directions = []


    def _optimize_brick_size(self, atr_period):
        atr = average_true_range(self.df['high'], self.df['low'], self.df['close'], atr_period)
        brick_size = atr.median()
        return brick_size


    def set_brick_size(self, atr_period, brick_size=10):
        if brick_size != 10:
            brick_size = self._optimize_brick_size(atr_period)
        self.brick_size = brick_size
