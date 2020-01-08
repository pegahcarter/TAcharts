

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
