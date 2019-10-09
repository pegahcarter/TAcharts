import pandas as pd
import numpy as np

from .utils import maxmin


def ema(line, span):
    ''' Returns the "exponential moving average" for a list '''

    line = pd.Series(line)
    return line.ewm(span=span, min_periods=1, adjust=False).mean()


def sma(line, window, attribute='mean'):
    ''' Returns the "simple moving average" for a list '''

    line = pd.Series(line)
    return getattr(line.rolling(window=window, min_periods=1), attribute)()


def macd(close, fast=8, slow=21):
    ''' Returns the "moving average convergence/divergence" (MACD) '''

    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    return ema_fast - ema_slow


def atr(high, low, close, window=14):
    ''' Returns the average true range from candlestick data '''

    high = np.array(high)
    low = np.array(low)
    close = np.array(close)
    prev_close = np.insert(close[:-1], 0, 0)
    # True range is largest of the following:
    #   a. Current high - current low
    #   b. Absolute value of current high - previous close
    #   c. Absolute value of current low - previous close
    true_range = maxmin('max', high - low, abs(high - prev_close), abs(low - prev_close))
    return sma(true_range, window)


def sdev(line, window):
    ''' Returns the standard deviation of a list '''

    line = pd.Series(line)
    return line.rolling(window=window, min_periods=0).std()


def roc(close, n=14):
    ''' Returns the rate of change in price over n periods '''

    close = np.array(close)
    pct_diff = np.diff(close, n) / close[:-n] * 100
    pct_diff = np.insert(pct_diff, 0, [0 for _ in range(n+1)])
    return pct_diff


def rsi(close, n=14):
    ''' Returns the "relative strength index", which is used to measure the velocity
    and magnitude of directional price movement.'''

    deltas = np.diff(close)
    seed = deltas[:n+1]
    up = seed[seed > 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rsi = np.zeros_like(close)
    rsi[:n] = 100. - 100./(1.+ up/down)
    for i in range(n, len(close)):
        delta = deltas[i-1]
        if delta > 0:
            up_val = delta
            down_val = 0
        else:
            up_val = 0
            down_val = -delta

        up = (up*(n-1) + up_val)/n
        down = (down*(n-1) + down_val)/n

        rsi[i] = 100. - 100./(1. + up/down)

    return rsi
