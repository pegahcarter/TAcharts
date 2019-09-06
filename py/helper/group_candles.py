import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def group_candles(period, df):
    candles = np.array(df)
    results = []
    for i in range(0, len(df)-period, period):
        results.append([
            candles[i, 0],                  # date
            candles[i, 1],                  # open
            candles[i:i+period, 2].max(),   # high
            candles[i:i+period, 3].min(),   # low
            candles[i+period, 4],           # close
            candles[i:i+period, 5].sum()    # volume
        ])

    return pd.DataFrame(results, columns=df.columns)
