# Reference for ATR calculation
# https://github.com/bukosabino/ta/blob/master/ta/volatility.py

"""
.. module:: volatility
   :synopsis: Volatility Indicators.
.. moduleauthor:: Dario Lopez Padial (Bukosabino)
"""
import numpy as np
import pandas as pd

from .utils import *


def average_true_range(high, low, close, n=14, fillna=False):
    """Average True Range (ATR)
    The indicator provide an indication of the degree of price volatility.
    Strong moves, in either direction, are often accompanied by large ranges,
    or large True Ranges.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_true_range_atr
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    cs = close.shift(1)
    tr = high.combine(cs, max) - low.combine(cs, min)

    atr = np.zeros(len(close))
    atr[0] = tr[1::].mean()
    for i in range(1, len(atr)):
        atr[i] = (atr[i-1] * (n-1) + tr.iloc[i]) / float(n)

    atr = pd.Series(data=atr, index=tr.index)

    if fillna:
        atr = atr.replace([np.inf, -np.inf], np.nan).fillna(0)

    return pd.Series(atr, name='atr')


def bollinger_mavg(close, n=20, fillna=False):
    """Bollinger Bands (BB)
    N-period simple moving average (MA).
    https://en.wikipedia.org/wiki/Bollinger_Bands
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    mavg = close.rolling(n, min_periods=0).mean()
    if fillna:
        mavg = mavg.replace(
            [np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(mavg, name='mavg')


def bollinger_hband(close, n=20, ndev=2, fillna=False):
    """Bollinger Bands (BB)
    Upper band at K times an N-period standard deviation above the moving
    average (MA + Kdeviation).
    https://en.wikipedia.org/wiki/Bollinger_Bands
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation
    Returns:
        pandas.Series: New feature generated.
    """
    mavg = close.rolling(n, min_periods=0).mean()
    mstd = close.rolling(n, min_periods=0).std()
    hband = mavg + ndev*mstd
    if fillna:
        hband = hband.replace(
            [np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(hband, name='hband')


def bollinger_lband(close, n=20, ndev=2, fillna=False):
    """Bollinger Bands (BB)
    Lower band at K times an N-period standard deviation below the moving
    average (MA − Kdeviation).
    https://en.wikipedia.org/wiki/Bollinger_Bands
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation
    Returns:
        pandas.Series: New feature generated.
    """
    mavg = close.rolling(n, min_periods=0).mean()
    mstd = close.rolling(n, min_periods=0).std()
    lband = mavg - ndev * mstd
    if fillna:
        lband = lband.replace(
            [np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(lband, name='lband')


def bollinger_hband_indicator(close, n=20, ndev=2, fillna=False):
    """Bollinger High Band Indicator
    Returns 1, if close is higher than bollinger high band. Else, return 0.
    https://en.wikipedia.org/wiki/Bollinger_Bands
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation
    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close]).transpose()
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    hband = mavg + ndev * mstd
    df['hband'] = 0.0
    df.loc[close > hband, 'hband'] = 1.0
    hband = df['hband']
    if fillna:
        hband = hband.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(hband, name='bbihband')


def bollinger_lband_indicator(close, n=20, ndev=2, fillna=False):
    """Bollinger Low Band Indicator
    Returns 1, if close is lower than bollinger low band. Else, return 0.
    https://en.wikipedia.org/wiki/Bollinger_Bands
    Args:
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
        ndev(int): n factor standard deviation
    Returns:
        pandas.Series: New feature generated.
    """
    df = pd.DataFrame([close]).transpose()
    mavg = close.rolling(n).mean()
    mstd = close.rolling(n).std()
    lband = mavg - ndev * mstd
    df['lband'] = 0.0
    df.loc[close < lband, 'lband'] = 1.0
    lband = df['lband']
    if fillna:
        lband = lband.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(lband, name='bbilband')
