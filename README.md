# TA-charts

This repository models price movement using several TA chart techniques:
* Ichimoku
* Bollinger Bands
* Renko


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
r.set_brick_size(auto=True, atr_period=14)
r.build()

r.plot()
```
![png](img/renko.PNG)
