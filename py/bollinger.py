from utils import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
pd.plotting.register_matplotlib_converters()


class Bollinger:
    def __init__(self, df, period=None):
        self.df = df.copy()
        if period:
            self.df = group_candles(self.df, period)
        self.df['date'] = self.df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        self.bollinger = {}


    def build(self, n=20, ndev=2):
        self.n = n
        self.ndev = ndev

        self._validate_data()
        self._apply_bollinger()


    def _validate_data(self):
        ''' Make sure we have more rows of data than the rolling average size '''
        if self.n > len(self.df):
            raise AssertionError('Moving average cannot be larger than number of records.')


    def _apply_bollinger(self):
        self.bollinger['sma'] = sma(self.df['close'], window=self.n)
        rng = self.ndev * sdev(self.df['close'], window=self.n)

        self.bollinger['h_band'] = self.bollinger['sma'] + rng
        self.bollinger['l_band'] = self.bollinger['sma'] - rng


    def plot(self):
        fig, ax = plt.subplots(1, figsize=(20, 10))

        x = self.df['date']
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
