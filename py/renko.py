from .utils import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Renko:
    def __init__(self, df):
        try:
            self.date = df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        except:
            self.date = df['date']

        self.high = df['high']
        self.low = df['low']
        self.close = df['close']
        self.renko = {
            'date': [self.date[0]],
            'price': [self.close[0]],
            'direction': [0]
        }


    def set_brick_size(self, auto=True, brick_size=None, atr_period=14):
        ''' Setting brick size '''
        if len(self.close) < atr_period:
            raise ValueError('ATR period is longer than historical data.')

        self.brick_size = self._optimize_brick_size(auto, brick_size, atr_period)
        return self.brick_size


    def _optimize_brick_size(self, auto, brick_size, atr_period):
        ''' Helper function to get optimal brick size based on ATR '''
        if auto:
            atr = average_true_range(self.high, self.low, self.close, atr_period)
            brick_size = np.median(atr)

        return brick_size


    def build(self):
        ''' Create Renko data '''
        for date, price in zip(self.date[1:], self.close[1:]):
            self._apply_renko(date, price)
        return self.renko.values()


    def _apply_renko(self, date, price):
        ''' Determine if there are any new bricks to paint with current price '''
        num_bricks = 0
        gap = (price - self.renko['price'][-1]) // self.brick_size
        # No gap means there's not a new brick
        if gap == 0:
            return
        # Add brick(s) in the same direction
        if (gap > 0 and self.renko['direction'][-1] >= 0) \
        or (gap < 0 and self.renko['direction'][-1] <= 0):
            num_bricks = gap
        # Gap >= 2 or -2 and opposite renko direction means we're switching brick direction
        elif abs(gap) >= 2:
            num_bricks = gap - np.sign(gap)
            self._update_renko(date, gap, 2)

        for brick in range(int(abs(num_bricks))):
            self._update_renko(date, gap)

        return self.renko


    def _update_renko(self, date, gap, brick_multiplier=1):
        ''' Append price and new block to renko dict '''
        renko_price = self.renko['price'][-1] + brick_multiplier*self.brick_size*np.sign(gap)
        self.renko['date'].append(date)
        self.renko['price'].append(renko_price)
        self.renko['direction'].append(np.sign(gap))
        return


    def plot(self):
        fig, ax = plt.subplots(1, figsize=(20,10))

        fig.suptitle("Renko Chart (brick size = {})".format(round(self.brick_size, 2)), fontsize=20)
        ax.set_ylabel('Price ($)')
        plt.rc('axes', labelsize=20)
        plt.rc('font', size=16)

        # Calculate range for axis
        ax.set_xlim(0, len(self.renko['price'])+1)
        ax.set_ylim(min(self.renko['price']) - 2*self.brick_size, max(self.renko['price']) + 2*self.brick_size)

        # Add bricks to chart
        for x in range(1, len(self.renko['price'])):
            date, price, direction = map(lambda val: val[x], self.renko.values())
            if direction == 1:
                facecolor='g'
                y = price - self.brick_size
            else:
                facecolor='r'
                y = price

            ax.add_patch(
                patches.Rectangle(
                    (x, y),
                    height=self.brick_size,
                    width=1,
                    facecolor=facecolor
                )
            )

        return plt.show()
