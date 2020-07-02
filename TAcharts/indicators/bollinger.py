#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.utils.group_candles import group_candles
from TAcharts.utils.draw_candlesticks import draw_candlesticks

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from .sma import sma
from .sdev import sdev

import pandas as pd
import os


class Bollinger:
    def __init__(self, df=None, filename=None, interval=None):
        if filename:
            filename_abs_path = f"{os.getcwd()}/{filename}"
            try:
                df = pd.read_csv(filename_abs_path)
            except:
                raise FileNotFoundError(f"{filename_abs_path}\n\nDoes not exist.")

        # Make all columns lowercase
        df.columns = [col.lower() for col in df]

        if interval:
            df = group_candles(df, interval)

        self.df = df
        self.bollinger = {}

    def _validate_data(self, interval):
        """ Make sure we have enough data """

        if interval and interval > len(self.df):
            raise AssertionError(
                f"Error: make sure the dataset has more than {interval} rows."
            )

    def build(self, n=20, ndev=2):
        """ Create Bollinger data """

        self._validate_data(n)

        # Create base simple moving average
        self.bollinger["sma"] = sma(self.df["close"], n=n)

        rng = ndev * sdev(self.df["close"], n=n)

        # Create upper and lower bands
        self.bollinger["h_band"] = self.bollinger["sma"] + rng
        self.bollinger["l_band"] = self.bollinger["sma"] - rng

        self.n = n
        self.ndev = ndev
        return self.bollinger

    def plot(self):
        fig, ax = plt.subplots(1, figsize=(20, 10))

        try:
            x = pd.to_datetime(self.df["date"])
        except:
            x = range(len(self.df))

        plt.plot(x, self.bollinger["l_band"], color="blue", label=None)
        plt.plot(x, self.bollinger["h_band"], color="blue", label=None)
        plt.plot(
            x, self.bollinger["sma"], color="orange", label="Simple Moving Average"
        )

        draw_candlesticks(ax, self.df)

        plt.rc("axes", labelsize=20)
        plt.rc("font", size=18)

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45)

        fig.suptitle("Bollinger Bands", fontsize=30)
        plt.ylabel("BTC price ($)")
        plt.legend(f"{self.n}MA")

        return plt.show()
