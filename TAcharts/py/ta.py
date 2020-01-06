from .wrappers import *


@pd_series_to_np_array
def rolling(src, n=2, fn=None, axis=1):
    ''' Returns the rolling sum, max, or min for a list across n periods '''

    # rolling sum
    if fn == 'sum':

        _rolling = src.cumsum()
        _rolling[n:] = _rolling[n:] - _rolling[:-n]
        _rolling[:n] = 0

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

    return _ema.values


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
    _roc[n:] = (np.diff(src, n) ) / src[:-n]

    return _roc
