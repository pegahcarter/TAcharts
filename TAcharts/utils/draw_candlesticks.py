#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.dates import date2num

import pandas as pd

def draw_candlesticks(ax, df):
    """ Add candlestick visuals to a matplotlib graph """

    df = df[["date", "open", "high", "low", "close"]].dropna()
    df['date'] = pd.to_datetime(df['date'])

    lines = []
    patches = []

    for i, (date, _open, high, low, close) in df.iterrows():
        date = date2num(date)
        if close >= _open:
            color = "g"
            lower = _open
            height = close - _open
        else:
            color = "r"
            lower = close
            height = _open - close

        vline = Line2D(
            xdata=(date, date),
            ydata=(low, high),
            color=color,
            linewidth=0.5,
            antialiased=True,
        )

        rect = Rectangle(
            xy=(date - 0.4, lower),
            width=0.8,
            height=height,
            facecolor=color,
            edgecolor=color,
            alpha=1.0,
        )

        lines.append(vline)
        ax.add_line(vline)
        patches.append(rect)
        ax.add_patch(rect)

    ax.autoscale_view()
    return lines, patches
