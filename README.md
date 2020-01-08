# TAcharts
### By: Carter Carlson

This repository provides technical tools to analyze OHLCV data, along with several TA chart functionalities.  These functions are optimized for speed and utilize numpy vectorization over built-in pandas methods.


#### indicators
* `atr(high, low, close, n=2)`: average true range from candlestick data
* `bollinger(df=None, filename=None, interval=None, n=20, ndev=2)`: Bollinger bands for the close of an instrument
* `cmf(df, n=2)`: Chaikin Money Flow of an OHLCV dataset
* `double_smooth(src, n_slow, n_fast)`: The smoothed value of two EMAs
* `ema(src, n=2)`: exponential moving average for a list of `src` across `n` periods
* `ichimoku(df=None, filename=None, interval=None)`: Ichimoku Cloud
* `macd(src, slow=25, fast=13)`: moving average convergence/divergence of `src`
* `mmo(src, n=2)`: Murrey Math oscillator of `src`
* `renko(df=None, filename=None, interval=None)`: Renko Chart
* `roc(src, n=2)`: rate of change of `src` across `n` periods
* `rolling(src, n=2, fn=None, axis=1)`: rolling `sum`, `max`, `min`, or `mean` of `src` across `n` periods
* `rsi(src, n=2)`: relative strength index of `src` across `n` periods
* `sdev(src, n=2)`: standard deviation across n periods
* `sma(src, n=2)`: simple moving average of `src` across `n` periods
* `td_sequential(src, n=2)`: TD sequential of `src` across `n` periods
* `tsi(src, slow=25, fast=13)`: true strength indicator


Basic tools (`ta.py`):

---

Momentum tools (`momentum.py`):
  * Used to measure the velocity and magnitude of directional price movement
* `tsi(src, slow=25, fast=13)`: true strength indicator of `src`
  * Used to determine overbought/oversold conditions, and warning of trend weakness through divergence

---
Technical indicators (`indicators.py`):
---
Additional tools (located in `utils.py`):
* `group_candles(df, interval)`: combine candles so instead of needing a different dataset for each time interval, you can form time intervals using more precise data.
  * Example: you have 15-min candlestick data but want to test a strategy based on 1-hour candlestick data (`interval=4`).
* `fill_values(averages, interval, target_len)`: Fill missing values with evenly spaced samples.
  * Example: You're using 15-min candlestick data to find the 1-hour moving average and want a value at every 15-min mark, and not every 1-hour mark.
* `crossover(x1, x2)`: find all instances of intersections between two lines
* `intersection(a0, a1, b0, b1)`: find the intersection coordinates between vector A and vector B
* `area_between(line1, line2)`: find the area between line1 and line2


### How it works

```python
import pandas as pd
%matplotlib inline

# NOTE: File should contain the columns 'date', 'open', 'high', 'low', and 'close'
df = pd.read_csv('../Daily.csv')
```

#### Bollinger Bands
```python
from bollinger import Bollinger

b = Bollinger(df)
b.build(n=20)
b.plot()
```
![png](img/bollinger.PNG)

#### Ichimoku
```python
from ichimoku import Ichimoku

i = Ichimoku(df)
i.build(20, 60, 120, 30)

i.plot()
```
![png](img/ichimoku.PNG)


#### Renko
```python
from renko import Renko

r = Renko(df)
r.set_brick_size(auto=True, atr_period=2)
r.build()

r.plot()
```
![png](img/renko.PNG)
