

@pd_series_to_np_array
def sma(src, n=14):
    ''' Returns the "simple moving average" for a list across n periods'''

    summed = rolling(src, fn='sum', n=n)
    _sma = summed / n

    return _sma
