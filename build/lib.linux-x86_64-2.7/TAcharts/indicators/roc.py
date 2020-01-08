

@pd_series_to_np_array
def roc(src, n=14):
    ''' Returns the rate of change in price over n periods '''

    _roc = np.zeros(src.shape)
    _roc[n:] = (np.diff(src, n) ) / src[:-n]

    return _roc
