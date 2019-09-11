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
        self.close = df['close']
        self.date = df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        self.bollinger = {}


    def build(self, n=20, ndev=2):
        self.n = n
        self.ndev = ndev

        self._apply_bollinger()


    def _apply_bollinger(self):
        self.bollinger['sma'] = self.close.rolling(self.n, min_periods=0).mean()
        sdev = self.close.rolling(self.n, min_periods=0).std()

        self.bollinger['h_band'] = self.bollinger['sma'] + self.ndev*sdev
        self.bollinger['l_band'] = self.bollinger['sma'] - self.ndev*sdev


    def plot(self):
        fig, ax = plt.subplots(1, figsize=(20, 10))

        x = self.date
        plt.plot(x, self.close, label='Close', color='black')
        plt.plot(x, self.bollinger['sma'], label='Simple Moving Average', color='green')
        plt.plot(x, self.bollinger['l_band'], color='blue')
        plt.plot(x, self.bollinger['h_band'], color='blue')

        plt.rc('axes', labelsize=20)
        plt.rc('font', size=16)

        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
        plt.xticks(rotation=45)

        ax.set(xlabel='Date', ylabel='Price ($)', title='Bollinger Bands (n = {}, std = {})'.format(self.n, self.ndev))
        plt.legend()

        plt.show()


df = pd.read_csv('data/15min.csv')[:300]
b = Bollinger(df)
b.build()

b.plot()
