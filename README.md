# Renko Indicator

This repository models price movement using a Renko chart.  Renko charts consist of bricks instead of candles, more clearly show market trends, and reduce the noise present on normal candlestick charts.

### How it works

```python
from py.renko import Renko

# NOTE: File should be a CSV of candlestick data that contains columns 'High', 'Low', and 'Close' 
renko = Renko(<FILEPATH>)
renko.set_brick_size()
renko.build()

renko.plot()
```


![png](renko.png)



#### References
* [pyrenko](https://github.com/quantroom-pro/pyrenko)
* [ta-lib](https://github.com/mrjbq7/ta-lib)
