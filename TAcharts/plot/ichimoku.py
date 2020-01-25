#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.utils.draw_candlesticks import draw_candlesticks

import matplotlib.pyplot as plt
import pandas as pd


def plot(df, ichimkou):
    fig, ax = plt.subplots(figsize=(30,10))

    x = df['date']
    try:
        x = pd.to_datetime(x)
    except:
        x = range(len(df))

    plt.plot(x, ichimoku['tenkan'], color='blue')
    plt.plot(x, ichimoku['kijun'], color='maroon')
    plt.plot(x, ichimoku['senkou_a'], color='green', linewidth=0.5)
    plt.plot(x, ichimoku['senkou_b'], color='red', linewidth=0.5)

    draw_candlesticks(ax, df)

    fig.suptitle('Ichimoku', fontsize=30)
    plt.ylabel('BTC price ($)')
    plt.rc('axes', labelsize=20)
    plt.rc('font', size=18)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    plt.xticks(rotation=45)

    plt.fill_between(
        x, ichimoku['senkou_a'], ichimoku['senkou_b'],
        where=ichimoku['senkou_a'] >= ichimoku['senkou_b'],
        facecolor='limegreen',
        interpolate=True
    )
    plt.fill_between(
        x, ichimoku['senkou_a'], ichimoku['senkou_b'],
        where=ichimoku['senkou_a'] <= ichimoku['senkou_b'],
        facecolor='salmon',
        interpolate=True
    )
    return plt.show()
