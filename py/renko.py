from .utils import *
from .ta import *
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

class Renko:
    def __init__(self, df):
        try:
            self.date = pd.to_datetime(df['date'])
        except:
            self.date = df['date']

        self.date = self.date.shift(1).tolist()

        self.high = df['high'].tolist()
        self.low = df['low'].tolist()
        self.close = df['close'].tolist()


    def set_brick_size(self, brick_size=None, auto=True, atr_period=14):
        ''' Setting brick size '''
        if len(self.close) < atr_period:
            raise ValueError('ATR period is longer than historical data.')

        self.brick_size = self._optimize_brick_size(auto, brick_size, atr_period)
        return self.brick_size


    def _optimize_brick_size(self, auto, brick_size, atr_period):
        ''' Helper function to get optimal brick size based on ATR '''
        if auto and not brick_size:
            average_true_range = atr(self.high, self.low, self.close, atr_period)
            brick_size = np.median(average_true_range)

        return brick_size


    def build(self):
        ''' Create Renko data '''
        units = self.close[0] // self.brick_size
        start_price = units * self.brick_size

        self.renko = {
            'index': [0],
            'date': [self.date[1]],
            'price': [start_price],
            'direction': [0]
        }
        # TODO: using [1:] fucks up slopemagic.  Need to fix.
        # Hood fix: not adding 1 to signal index
        for i in range(1, len(self.close)):
            self._apply_renko(i)

        return


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
        self.renko['date'].append(self.date[i])
        return


    def plot(self, num_bricks=None, signal_indices=None):
        fig, ax = plt.subplots(1, figsize=(10, 5))

        # fig.suptitle("Renko Chart (brick size = {})".format(round(self.brick_size, 2)), fontsize=20)
        # ax.set_ylabel('Price ($)')
        # plt.rc('axes', labelsize=20)
        # plt.rc('font', size=16)

        prices = self.renko['price']
        directions = self.renko['direction']

        if num_bricks is not None:
            prices = prices[-num_bricks:]
            directions = directions[-num_bricks:]

        if signal_indices is not None:
            for x in signal_indices:
                plt.axvline(x=x)

        # Calculate range for axis
        ax.set_xlim(0, len(prices) + 1)
        # ax.set_xlim(0, len(self.renko['price']) + 1)
        ax.set_ylim(min(prices) - 2*self.brick_size, max(prices) + 2*self.brick_size)
        # ax.set_ylim(min(self.renko['price']) - 2*self.brick_size, max(self.renko['price']) + 2*self.brick_size)

        # Add bricks to chart
        for x, (price, direction) in enumerate(zip(prices, directions)):
        # for x in range(1, len(self.renko['price'])):
            # index, date, price, direction = map(lambda val: val[x], self.renko.values())
            if direction == 1:
                facecolor='g'
                y = price - self.brick_size
            else:
                facecolor='r'
                y = price

            ax.add_patch(
                Rectangle(
                    (x+1, y),
                    height=self.brick_size,
                    width=1,
                    facecolor=facecolor
                )
            )

        return plt.show()
