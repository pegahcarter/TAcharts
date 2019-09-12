import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from matplotlib import colors as mcolors
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.dates import date2num



def group_candles(df, period):
    candles = np.array(df)
    results = []
    for i in range(0, len(df)-period, period):
        results.append([
            candles[i, 0],                  # date
            candles[i, 1],                  # open
            candles[i:i+period, 2].max(),   # high
            candles[i:i+period, 3].min(),   # low
            candles[i+period, 4],           # close
            candles[i:i+period, 5].sum()    # volume
        ])
    return pd.DataFrame(results, columns=df.columns)


def average_true_range(high, low, close, n=14):
    high = np.array(high)
    low = np.array(low)
    close = np.array(close)

    cs = np.insert(close[1:], 0, None)
    tr = np.amax([cs, high], axis=0) - np.amin([cs, low], axis=0)
    tr[0] = high[0] - low[0]

    atr = np.zeros(len(close))
    atr[0] = tr[1:].mean()
    for i in range(len(atr)):
        atr[i] = (atr[i-1] * (n - 1) + tr[i]) / float(n)
    return atr


def draw_candlesticks(ax, df):

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
