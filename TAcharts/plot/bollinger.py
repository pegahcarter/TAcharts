#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.utils.draw_candlesticks import draw_candlesticks


def plot(self):
    fig, ax = plt.subplots(1, figsize=(20, 10))

    if date:
        x = self.date
    else:
        x = range(len(self.close))
    plt.plot(x, self.bollinger['sma'], label='Simple Moving Average', color='orange')
    plt.plot(x, self.bollinger['l_band'], color='blue', label=None)
    plt.plot(x, self.bollinger['h_band'], color='blue')

    draw_candlesticks(ax, self.df)

    plt.rc('axes', labelsize=20)
    plt.rc('font', size=18)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)

    fig.suptitle('Bollinger Bands', fontsize=30)
    plt.ylabel('BTC price ($)')
    plt.legend(f'{self.n}MA')

    return plt.show()
