from matplotlib import colors as mcolors
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
import itertools
import time
import requests
from datetime import datetime, timedelta

from .wrappers import *


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
    avgs_unpack += [averages[-1]] * (target_len - len(avgs_unpack))
    return avgs_unpack


@pd_series_to_np_array
def crossover(x1, x2):
    ''' Find all instances of intersections between two lines '''

    x1_gt_x2 = x1 > x2
    cross = np.diff(x1_gt_x2)
    cross = np.insert(cross, 0, False)
    cross_indices = np.flatnonzero(cross)
    return cross_indices


def intersection(a0, a1, b0, b1):
    ''' Return the intersection coordinates between vector A and vector B '''

    a_diff = a1 - a0
    b_diff = b1 - b0

    pos0_diff = float(a0 - b0)

    x = pos0_diff / (b_diff - a_diff)
    y = b_diff*x + b0

    return x, y


@pd_series_to_np_array
def area_between(line1, line2):
    ''' Return the area between line1 and line2 '''

    diff = line1 - line2
    x1 = diff[:-1]
    x2 = diff[1:]

    triangle_area = abs(x2 - x1) * .5
    square_area = np.amin(zip(x1, x2), axis=1)

    return np.sum([triangle_area, square_area])


@args_to_dtype(list)
def maxmin(*args, max_or_min=None, axis=0):
    ''' Compare lists and return the max or min value at each index '''

    if max_or_min == 'max':
        return np.amax(args, axis=axis)
    elif max_or_min == 'min':
        return np.amin(args, axis=axis)
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
