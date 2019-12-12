from .utils import maxmin
from .wrappers import *


@pd_series_to_np_array
def sma(close, n=14):
    ''' Returns the "simple moving average" for a list across n periods'''

    summed = rolling_sum(close, n=n)
    _sma = summed / n
    return _sma


@args_to_dtype(np.array)
def rolling_sum(close, n=20):
    ''' Returns the rolling sum for a list across n periods '''

    _rolling_sum = close.cumsum()
    _rolling_sum[n:] = _rolling_sum[n:] - _rolling_sum[:-n]
    _rolling_sum[:n] = 0.000000001
    return _rolling_sum


@args_to_dtype(pd.Series)
def ema(line, span=2):
    ''' Returns the "exponential moving average" for a list '''

    _ema = line.ewm(span=span, min_periods=1, adjust=False).mean()
    return _ema


def macd(close, fast=8, slow=21):
    ''' Returns the "moving average convergence/divergence" (MACD) '''

    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    _macd = ema_fast - ema_slow
    return _macd


@pd_series_to_np_array
def atr(high, low, close, n=14):
    ''' Returns the average true range from candlestick data '''

    prev_close = np.insert(close[:-1], 0, 0)
    # True range is largest of the following:
    #   a. Current high - current low
    #   b. Absolute value of current high - previous close
    #   c. Absolute value of current low - previous close
    true_range = maxmin(high - low, abs(high - prev_close), abs(low - prev_close), max_or_min='max')
    _atr = sma(true_range, n)
    return _atr


@pd_series_to_np_array
def roc(close, n=14):
    ''' Returns the rate of change in price over n periods '''

    _roc = np.zeros_like(close)
    _roc[n:] = np.diff(close, n) / close[:-n] * 100
    return _roc


@args_to_dtype(list)
def rsi(close, n=14):
    ''' Returns the "relative strength index", which is used to measure the velocity
    and magnitude of directional price movement. '''

    deltas = np.diff(close)
    seed = deltas[:n+1]
    up = seed[seed > 0].sum()/n
    down = -seed[seed < 0].sum()/n
    _rsi = np.zeros_like(close)
    _rsi[:n] = 100. - 100./(1.+ up/down)
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

        _rsi[i] = 100. - 100./(1. + up/down)

    return _rsi



@args_to_dtype(list)
def td_sequential(close, n=4):
    ''' Returns the TD sequential of the close '''

    old_gt_new = close[:-n] > close[n:]
    diff_lst = np.diff(old_gt_new)
    diff_lst = np.insert(diff_lst, 0, False)

    _td_sequential = [0, 0, 0, 0]

    for diff in diff_lst:
        if not diff:
            _td_sequential.append(_td_sequential[-1] + 1)
        else:
            _td_sequential.append(1)

    return _td_sequential


def chaikin_money_flow(df, n=20):
    ''' Returns the Chaikin Money Flow of a OHLCV dataframe'''

    high = df['high'].values
    low = df['low'].values
    close = df['close'].values
    volume = df['volume'].values

    avg = (2*close - high - low) / (high - low + .000000001) * volume

    avg_roll = rolling_sum(avg, n=n)
    vol_roll = rolling_sum(volume, n=n)

    _chaikin_money_flow = avg_roll / vol_roll
    _chaikin_money_flow[:n] = 0

    return _chaikin_money_flow


@pd_series_to_np_array
def murrey_math_oscillator(close, n=100):
    ''' Returns the Murrey Math Oscillator of the close '''

    shape = (len(close) - n + 1, n)
    strides = close.strides * 2
    close_strided = np.lib.stride_tricks.as_strided(close, shape=shape, strides=strides)

    # Donchian channel
    highest = np.amax(close_strided, axis=1)
    lowest = np.amin(close_strided, axis=1)

    rng = highest - lowest

    # Oscillator
    rng_multiplier = rng * .125
    midline = lowest + rng_multiplier * 4

    _murrey_math_oscillator = np.zeros_like(close)
    _murrey_math_oscillator[n-1:] = (close[n-1:] - midline) / rng

    return _murrey_math_oscillator
