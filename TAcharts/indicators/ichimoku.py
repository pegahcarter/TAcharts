#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from TAcharts.utils.group_candles import group_candles
from TAcharts.utils.draw_candlesticks import draw_candlesticks

from .sma import sma

from datetime import datetime, timedelta
import matplotlib.dates as mdates

import matplotlib.pyplot as plt

import pandas as pd


class Ichimoku:
    def __init__(self, df=None, filename=None, interval=None):

        if filename:
            filename_abs_path = f"{os.getcwd()}/{filename}"
            try:
                df = pd.read_csv(filename_abs_path)
            except:
                raise FileNotFoundError(f"{filename_abs_path}\n\nDoes not exist.")

        # Now that we have our df, make all headers lowercase
        df.columns = [col.lower() for col in df]

        if interval:
            df = group_candles(df, interval)

        self.df = df
        self.ichimoku = {}

        self._validate_data(interval)

    def _validate_data(self, interval):
        """ Make sure we have enough data to form the cloud """

        if interval and interval > len(self.df):
            raise AssertionError(
                f"Error: make sure the dataset has more than {interval} rows."
            )

    def _extend_window(self, displacement):
        last_date = self.df["date"].iat[-1]
        window = last_date - self.df["date"].iat[-2]
        new_dates = [last_date + window * (1 + i) for i in range(displacement)]
        self.df = self.df.append(
            pd.DataFrame(new_dates, columns=["date"]), ignore_index=True, sort=False
        )
        return

    def _build_lines(self, **kwargs):
        for key, val in kwargs.items():
            high = sma(self.df["high"], val)
            low = sma(self.df["low"], val)
            self.ichimoku[key] = (high + low) / 2
        return

    def _build_spans(self, senkou_b_interval, displacement):
        self.ichimoku["chikou"] = self.df["close"].shift(-displacement)
        self.ichimoku["senkou_a"] = (
            self.ichimoku["tenkan"] + self.ichimoku["kijun"]
        ) / 2

        self._build_lines(senkou_b=senkou_b_interval)

        self.ichimoku["senkou_a"] = self.ichimoku["senkou_a"].shift(displacement)
        self.ichimoku["senkou_b"] = self.ichimoku["senkou_b"].shift(displacement)

        for indicator in ["tenkan", "kijun", "chikou", "senkou_a", "senkou_b"]:
            self.ichimoku[indicator] = self.ichimoku[indicator][
                senkou_b_interval + displacement :
            ]

        self.df = self.df[senkou_b_interval + displacement :]
        return

    def build(self, tenkan_interval, kijun_interval, senkou_b_interval, displacement):
        """ Create Ichimoku data """

        self._validate_data(senkou_b_interval)
        self._extend_window(displacement)

        # Tenkan (conversion line) = (highest high + highest low)/2 for the past x intervals
        # Kijun (base line) = (highest high + lowest low)/2 for the past x*3 intervals
        self._build_lines(tenkan=tenkan_interval, kijun=kijun_interval)

        # Chikou (lagging span) = Current closing price time-shifted backwards x*3 intervals
        # Senkou span A (leading span A) = (tenkan + kijun)/2 time-shifted forwards x*3 intervals
        # Senkou span B (leading span B) = (highest high + lowest low)/2 for past x*6 intervals, shifted forwards x*3 intervals
        self._build_spans(
            senkou_b_interval=senkou_b_interval, displacement=displacement
        )

        return self.ichimoku

    def plot(self):
        fig, ax = plt.subplots(figsize=(30, 10))

        x = self.df["date"]
        try:
            x = pd.to_datetime(x)
        except:
            x = range(len(self.df))

        plt.plot(x, self.ichimoku["tenkan"], color="blue")
        plt.plot(x, self.ichimoku["kijun"], color="maroon")
        plt.plot(x, self.ichimoku["senkou_a"], color="green", linewidth=0.5)
        plt.plot(x, self.ichimoku["senkou_b"], color="red", linewidth=0.5)

        draw_candlesticks(ax, self.df)

        fig.suptitle("Ichimoku", fontsize=30)
        plt.ylabel("BTC price ($)")
        plt.rc("axes", labelsize=20)
        plt.rc("font", size=18)

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%y"))
        plt.xticks(rotation=45)

        plt.fill_between(
            x,
            self.ichimoku["senkou_a"],
            self.ichimoku["senkou_b"],
            where=self.ichimoku["senkou_a"] >= self.ichimoku["senkou_b"],
            facecolor="limegreen",
            interpolate=True,
        )
        plt.fill_between(
            x,
            self.ichimoku["senkou_a"],
            self.ichimoku["senkou_b"],
            where=self.ichimoku["senkou_a"] <= self.ichimoku["senkou_b"],
            facecolor="salmon",
            interpolate=True,
        )
        return plt.show()
