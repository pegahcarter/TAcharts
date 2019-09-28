import pandas as pd
import numpy as np
import itertools
from datetime import datetime, timedelta
from matplotlib import colors as mcolors
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.dates import date2num


def group_candles(df, interval):
    ''' Combine candles so instead of needing one dataset for each time interval,
        you can form time intervals using more precise data.

    Example: You have 15-min candlestick data but want to test a strategy based
        on 1-hour candlestick data  (interval=4).
    '''
    columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    candles = np.array(df[columns])
    results = []
    for i in range(0, len(df)-interval, interval):
        results.append([
            candles[i, 0],                      # date
            candles[i, 1],                      # open
            candles[i:i+interval, 2].max(),     # high
            candles[i:i+interval, 3].min(),     # low
            candles[i+interval, 4],             # close
            candles[i:i+interval, 5].sum()      # volume
        ])
    return pd.DataFrame(results, columns=columns)


def fill_values(averages, interval, target_len):
    ''' Fill missing values with evenly spaced samples.

    Example: You're using 15-min candlestick data but want to include a 1-hour moving
        average with a value at every 15-min mark, and not just every 1-hour mark.
    '''
    # Combine every two values with the number of intervals between each value
    avgs_zip = zip(averages[:-1], averages[1:], itertools.repeat(interval), itertools.repeat(False))
    # Generate evenly-spaced samples between every point
    avgs_gen = (np.linspace(*x) for x in avgs_zip)
    # Unpack all values into one list
    avgs_unpack = list(itertools.chain.from_iterable(avgs_gen))
    # Extend the list to have as many values as our target dataframe
    avgs_unpack.extend([averages[-1]] * (target_len - len(avgs_unpack)))
    return avgs_unpack


def ema(line, span):
    ''' Returns the exponential moving average for a list '''
    line = pd.Series(line)
    return line.ewm(span=span, min_periods=1, adjust=False).mean()


def sma(line, window, attribute='mean'):
    ''' Returns the simple moving average for a list '''
    line = pd.Series(line)
    return getattr(line.rolling(window=window, min_periods=1), attribute)()


def sdev(line, window):
    ''' Returns the standard deviation of a list '''
    line = pd.Series(line)
    return line.rolling(window=window, min_periods=0).std()


def macd(close, fast=8, slow=21):
    ''' Returns the "moving average convergence/divergence" (MACD) '''
    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    return ema_fast - ema_slow


def average_true_range(high, low, close, span=14):
    ''' Returns the average true range from candlestick data '''
    high = np.array(high)
    low = np.array(low)
    close = np.array(close)
    prev_close = np.insert(close[1:], 0, 0)

    # True range is largest of the following:
    #   a. Current high - current low
    #   b. Absolute value of current high - previous close
    #   c. Absolute value of current low - previous close
    true_range = maxmin('max', high - low, abs(high - prev_close), abs(low - prev_close))
    atr = ema(true_range, span)
    return atr


def crossover(x1, x2):
    ''' Find all instances of intersections between two lines '''
    crossovers = {}
    x1_gt_x2 = list(x1 > x2)
    current_val = x1_gt_x2[0]
    for index, val in enumerate(x1_gt_x2[1:]):
        if val != current_val:
            crossovers[index+1] = val
        current_val = val
    return crossovers


def intersection(a1, a2, b1, b2):
    ''' Return the intersection coordinates between vector A and vector B '''
    da = np.subtract(a1, a2)
    db = np.subtract(b1, b2)
    dp = np.subtract(a1, b1)

    dap = np.array([-da[1], da[0]])

    denom = dap.dot(db)
    num = dap.dot(dp)

    return (float(num) / denom)*db + b1


def area_between(line1, line2):
    ''' Return the area between line1 and line2 '''
    diff = np.subtract(line1, line2)
    x1 = diff[:-1]
    x2 = diff[1:]

    triangle_area = abs(x2 - x1) * .5
    square_area = np.amin(zip(x1, x2), axis=1)

    return np.sum([triangle_area, square_area])


def maxmin(max_or_min, *args):
    ''' Compare lists and return the max or min value at each index '''
    if max_or_min == 'max':
        return np.amax(args, axis=0)
    elif max_or_min == 'min':
        return np.amin(args, axis=0)
    else:
        raise ValueError('Enter "max" or "min" as max_or_min parameter.')


def draw_candlesticks(ax, df):
    ''' Add candlestick visuals to a matplotlib graph '''
    df = df[['date', 'open', 'high', 'low', 'close']].dropna()
    lines = []
    patches = []

    for i, (date, _open, high, low, close) in df.iterrows():
        date = date2num(date)
        if close >= _open:
            color = 'g'
            lower = _open
            height = close - _open
        else:
            color = 'r'
            lower = close
            height = _open - close

        vline = Line2D(
            xdata=(date, date), ydata=(low, high),
            color=color,
            linewidth=0.5,
            antialiased=True
        )

        rect = Rectangle(
            xy=(date - .4, lower),
            width=0.8,
            height=height,
            facecolor=color,
            edgecolor=color,
            alpha=1.0
        )

        lines.append(vline)
        ax.add_line(vline)
        patches.append(rect)
        ax.add_patch(rect)

    ax.autoscale_view()
    return lines, patches
