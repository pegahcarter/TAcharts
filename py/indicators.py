from .wrappers import *
from .ta import rolling


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
