#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import matplotlib.dates as mdates
pd.plotting.register_matplotlib_converters()

# TODO: imports

class Bollinger:
    def __init__(self, close, date=None, period=None):
        self.close = close
        self.date = date
        if period:
            self.close = group_candles(self.close, period)
        # self.df['date'] = self.df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        self.bollinger = {}


    def build(self, n=20, ndev=2):
        self.n = n
        self.ndev = ndev

        self._validate_data()
        self._apply_bollinger()


    def _validate_data(self):
        ''' Make sure we have more rows of data than the rolling average size '''
        if self.n > len(self.close):
            raise AssertionError('Moving average cannot be larger than number of records.')


    def _apply_bollinger(self):
        self.bollinger['sma'] = sma(self.close, window=self.n)
        rng = self.ndev * sdev(self.close, window=self.n)

        self.bollinger['h_band'] = self.bollinger['sma'] + rng
        self.bollinger['l_band'] = self.bollinger['sma'] - rng


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
        plt.legend(['{}MA'.format(self.n)])

        return plt.show()
