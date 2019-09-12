from TAcharts.py.utils import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
pd.plotting.register_matplotlib_converters()


class Bollinger:
    def __init__(self, df, period=None):
        if period:
            df = group_candles(df, period)
        df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        self.df = df
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
        self.bollinger['sma'] = self.df['close'].rolling(self.n, min_periods=0).mean()
        sdev = self.df['close'].rolling(self.n, min_periods=0).std()

        self.bollinger['h_band'] = self.bollinger['sma'] + self.ndev*sdev
        self.bollinger['l_band'] = self.bollinger['sma'] - self.ndev*sdev


    def plot(self):
        fig, ax = plt.subplots(1, figsize=(20, 10))

        x = self.df['date']
        plt.plot(x, self.bollinger['sma'], label='Simple Moving Average', color='orange')
        plt.plot(x, self.bollinger['l_band'], color='blue', label=None)
        plt.plot(x, self.bollinger['h_band'], color='blue')

        draw_candlesticks(ax, self.df)

        plt.rc('axes', labelsize=20)
        plt.rc('font', size=16)

        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
        plt.xticks(rotation=45)

        ax.set(ylabel='Price ($)', title='Bollinger Bands')
        plt.legend(['{}MA'.format(self.n)])

        return plt.show()


df = pd.read_csv('data/15min.csv')[:10000]
b = Bollinger(df, period=96)
b.build()

b.plot()
