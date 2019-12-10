from .utils import maxmin
from .wrappers import *


@args_to_dtype(pd.Series)
def ema(line, span=2):
    ''' Returns the "exponential moving average" for a list '''

    return line.ewm(span=span, min_periods=1, adjust=False).mean()


@pd_series_to_np_array
def sma(close, window=14):
    ''' Returns the "simple moving average" for a list '''

    arr = close.cumsum()
    arr[window:] = arr[window:] - arr[:-window]
    arr[:window] = 0
    return arr / window



def macd(close, fast=8, slow=21):
    ''' Returns the "moving average convergence/divergence" (MACD) '''

    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    return ema_fast - ema_slow


@pd_series_to_np_array
def atr(high, low, close, window=14):
    ''' Returns the average true range from candlestick data '''

    prev_close = np.insert(close[:-1], 0, 0)
    # True range is largest of the following:
    #   a. Current high - current low
    #   b. Absolute value of current high - previous close
    #   c. Absolute value of current low - previous close
    true_range = maxmin('max', high - low, abs(high - prev_close), abs(low - prev_close))
    return sma(true_range, window)


@pd_series_to_np_array
def roc(close, n=14):
    ''' Returns the rate of change in price over n periods '''

    pct_diff = np.zeros_like(close)
    pct_diff[n:] = np.diff(close, n) / close[:-n] * 100
    return pct_diff


@args_to_dtype(list)
def rsi(close, n=14):
    ''' Returns the "relative strength index", which is used to measure the velocity
    and magnitude of directional price movement. '''

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



@args_to_dtype(list)
def td_sequential(close, n=4):
    ''' Returns the TD sequential of the close '''

    old_gt_new = close[:-n] > close[n:]
    diff_lst = np.diff(old_gt_new)
    diff_lst = np.insert(diff_lst, 0, False)

    td_sequential = [0, 0, 0, 0]

    for diff in diff_lst:
        if not diff:
            td_sequential.append(td_sequential[-1] + 1)
        else:
            td_sequential.append(1)

    return td_sequential
