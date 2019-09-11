from TAcharts.py.utils import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
import matplotlib.pyplot as plt


class Ichimoku:
    def __init__(self, FILE='data/15min.csv'):
        self.df = pd.read_csv(FILE)
        self.price = self.df['Close']
        self.high = self.df['High']
        self.low = self.df['Low']
        self.ichimoku = {
            'tenkan': [],
            'kijun': [],
            'chikou': [],
            'senkou_a': [],
        }


    def build(self, tenkan_period, kijun_period, senkou_b_period, displacement):
        ''' Create Ichimoku data '''
        # Tenkan (conversion line) = (highest high + highest low)/2 for the past x periods
        # Kijun (base line) = (highest high + lowest low)/2 for the past x*3 periods
        self._build_lines(tenkan=tenkan_period, kijun=kijun_period)

        # Chikou (lagging span) = Current closing price time-shifted backwards x*3 periods
        # Senkou span A (leading span A) = (tenkan + kijun)/2 time-shifted forwards x*3 periods
        # Senkou span B (leading span B) = (highest high + lowest low)/2 for past x*6 periods, shifted forwards x*3 periods
        self._build_spans(senkou_b_period=senkou_b_period, displacement=displacement)


    def _build_lines(self, **kwargs):
        for i in kwargs:
            high = self.high.rolling(window=kwargs[i]).max()
            low = self.low.rolling(window=kwargs[i]).low()
            self.ichimoku[i] = (high + low)/2


    def _build_spans(self, senkou_b_period, displacement):
        self.ichimoku['chikou'] = self.price.shift(-displacement)
        self.ichimoku['senkou_a'] = (self.ichimoku['tenkan'] + self.ichimoku['kijun']) / 2

        self._build_lines(senkou_b=senkou_b_period)

        self.ichimoku['senkou_a'] = self.ichimoku['senkou_a'].shift(displacement)
        self.ichimoku['senkou_b'] = self.ichimoku['senkou_b'].shift(displacement)


    def plot(self):
        fig, ax = plt.subplots(figsize=(20,20))




df = pd.read_csv('data/15min.csv')

df['High'].rolling(window=10).max()
