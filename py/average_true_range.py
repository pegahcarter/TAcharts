import numpy as np

def average_true_range(df, n=14):

    high = np.array(df['high'])
    low = np.array(df['low'])
    close = np.array(df['close'])

    cs = np.insert(close[1:], 0, None)

    tr = np.amax([cs, high], axis=0) - np.amin([cs, low], axis=0)
    tr[0] = high[0] - low[0]

    atr = np.zeros(len(close))
    atr[0] = tr[1:].mean()

    for i in range(len(atr)):
        atr[i] = (atr[i-1] * (n - 1) + tr[i]) / float(n)

    return atr
