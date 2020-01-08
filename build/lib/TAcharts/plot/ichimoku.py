#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

from .renko import *






# ------------------------------------------------------------------------------


def plot():

    fig, ax = plt.subplots(figsize=(30,10))

    x = self.df['date']
    plt.plot(x, self.ichimoku['tenkan'], color='blue')
    plt.plot(x, self.ichimoku['kijun'], color='maroon')
    plt.plot(x, self.ichimoku['senkou_a'], color='green', linewidth=0.5)
    plt.plot(x, self.ichimoku['senkou_b'], color='red', linewidth=0.5)

    draw_candlesticks(ax, self.df)

    fig.suptitle('Ichimoku', fontsize=30)
    plt.ylabel('BTC price ($)')
    plt.rc('axes', labelsize=20)
    plt.rc('font', size=18)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    plt.xticks(rotation=45)

    plt.fill_between(
        x, self.ichimoku['senkou_a'], self.ichimoku['senkou_b'],
        where=self.ichimoku['senkou_a'] >= self.ichimoku['senkou_b'],
        facecolor='limegreen',
        interpolate=True
    )
    plt.fill_between(
        x, self.ichimoku['senkou_a'], self.ichimoku['senkou_b'],
        where=self.ichimoku['senkou_a'] <= self.ichimoku['senkou_b'],
        facecolor='salmon',
        interpolate=True
    )
    return plt.show()
