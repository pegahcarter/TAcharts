from .wrappers import *
from .ta import ema, roc


def macd(src, fast=8, slow=21):
    ''' Returns the "moving average convergence/divergence" (MACD) '''

    ema_fast = ema(src, fast)
    ema_slow = ema(src, slow)
    _macd = ema_fast.values - ema_slow.values

    return _macd


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


def double_smooth(src, slow=25, fast=13):
    ''' Returns the smoothed value of two EMAs '''

    first_smooth = ema(src, n=slow)
    _double_smooth = ema(first_smooth, n=fast)

    return _double_smooth.values


def tsi(src, slow=25, fast=13):
    ''' Returns the "true strength indicator", which is used to determine overbought
    and oversold conditions, and warning of trend weakness through divergence. '''

    _roc = roc(src, n=1)

    roc_double_smooth = double_smooth(_roc, slow=slow, fast=fast)
    roc_double_smooth_abs = double_smooth(abs(_roc), slow=slow, fast=fast)

    _tsi = (roc_double_smooth / roc_double_smooth_abs) * 100

    return _tsi
