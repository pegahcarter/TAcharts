

@args_to_dtype(pd.Series)
def ema(src, n=2):
    ''' Returns the "exponential moving average" for a list '''

    _ema = src.ewm(span=n, min_periods=1, adjust=False).mean()

    return _ema.values
