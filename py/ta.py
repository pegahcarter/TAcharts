from .wrappers import *


# @pd_series_to_np_array
def rolling(src, n=2, fn=None, axis=1):
    ''' Returns the rolling sum, max, or min for a list across n periods '''

    # rolling sum
    if fn == 'sum':

        _rolling = src.cumsum()
        _rolling[n:] = _rolling[n:] - _rolling[:-n]
        _rolling[:n] = .000000001

        return _rolling

    # rolling max, min, or mean
    elif fn in ['max', 'min', 'mean']:

        shape = (len(src) - n + 1, n)
        strides = src.strides * 2
        src_strided = np.lib.stride_tricks.as_strided(src, shape=shape, strides=strides)

        _rolling = np.zeros(src.shape)
        _rolling[n-1:] = getattr(np, fn)(src_strided, axis=axis)

        return _rolling

    else:
        raise ValueError('Enter "sum", "max", "min", or "mean" as fn argument')


@pd_series_to_np_array
def sma(src, n=14):
    ''' Returns the "simple moving average" for a list across n periods'''

    summed = rolling(src, fn='sum', n=n)
    _sma = summed / n

    return _sma


@args_to_dtype(pd.Series)
def ema(src, n=2):
    ''' Returns the "exponential moving average" for a list '''

    _ema = src.ewm(span=n, min_periods=1, adjust=False).mean()

    return _ema


def macd(src, fast=8, slow=21):
    ''' Returns the "moving average convergence/divergence" (MACD) '''

    ema_fast = ema(src, fast)
    ema_slow = ema(src, slow)
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
    true_range = rolling(high - low, abs(high - prev_close), abs(low - prev_close), fn='max', n=1, axis=0)
    _atr = sma(true_range, n)

    return _atr


@pd_series_to_np_array
def roc(src, n=14):
    ''' Returns the rate of change in price over n periods '''

    _roc = np.zeros(src.shape)
    _roc[n:] = (np.diff(src, n) ) / src[:-n] * 100

    return _roc


@args_to_dtype(list)
def rsi(src, n=14):
    ''' Returns the "relative strength index", which is used to measure the velocity
    and magnitude of directional price movement. '''

    deltas = np.diff(src)
    seed = deltas[:n+1]
    up = seed[seed > 0].sum()/n
    down = -seed[seed < 0].sum()/n
    _rsi = np.zeros_like(src)
    _rsi[:n] = 100. - 100./(1.+ up/down)
    for i in range(n, len(src)):
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


@pd_series_to_np_array
def td_sequential(src, n=4):
    ''' Returns the TD sequential of the close '''

    old_gt_new = src[:-n] > src[n:]
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

    avg_roll = rolling(avg, fn='sum', n=n)
    vol_roll = rolling(volume, fn='sum', n=n)

    _chaikin_money_flow = avg_roll / vol_roll
    _chaikin_money_flow[:n] = 0.000000001

    return _chaikin_money_flow


@pd_series_to_np_array
def murrey_math_oscillator(src, n=100):
    ''' Returns the Murrey Math Oscillator of the close '''

    # Donchian channel
    highest = rolling(src, fn='max', n=n)
    lowest = rolling(src, fn='min', n=n)

    rng = highest - lowest

    # Oscillator
    rng_multiplier = rng * .125
    midline = lowest + rng_multiplier * 4

    _murrey_math_oscillator = (src - midline) / rng

    return _murrey_math_oscillator
