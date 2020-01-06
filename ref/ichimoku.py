
https://github.com/carlfarterson/ichimoku-backtests/blob/master/py/ichimoku.py
# Main script for ichimoku cloud

import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
pd.plotting.register_matplotlib_converters()


def ichimoku(df,  tenkan_period, kijun_period, senkou_b_period, displacement):

    # NOTE: commented out since we're only looking at current date range of
    # extend_dates(df, displacement)
    df['price'] = df['close'].shift(1)

    make_lines(df, tenkan=tenkan_period, kijun=kijun_period)
    make_spans(df, displacement=displacement, senkou_b_period=senkou_b_period)

    return df

# Function to extend table by the displacement
def extend_dates(df, displacement):
    # df['date'] = list(map(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), df['date']))
    # df['date'] = [datetime.strptime(hr, '%Y-%m-%d %H:%M:%S') for hr in df['date']]
    last_date = df['date'].at[len(df)-1]
    last_date = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
    dates = [last_date + timedelta(hours=i+1) for i in range(displacement)]
    df = df.append({'date': dates}, ignore_index=True, sort=False)


# Tenkan (conversion line) = (highest high + highest low)/2 for the past 9 periods
# Kijun (base line) = (highest high + lowest low)/2 for the past 26 periods
def make_lines(df, **kwargs):
    for i in kwargs:
        high = df['high'].rolling(window=kwargs[i]).max()
        low = df['low'].rolling(window=kwargs[i]).min()
        df[i] = (high + low)/2


# Chikou (lagging span) = Current closing price time-shifted backwards 26 periods
# Senkou span A (leading span A) = (tenkan + kijun)/2 time-shifted forwards 26 periods
# Senkou span B (leading span B) = (highest high + lowest low)/2 for past 52 periods, shifted forwards 26 periods
def make_spans(df, displacement, senkou_b_period):
    df['chikou'] = df['close'].shift(-displacement)
    df['senkou_a'] = (df['tenkan'] + df['kijun']) / 2

    make_lines(df, senkou_b=senkou_b_period)
    df[['senkou_a', 'senkou_b']] = df[['senkou_a', 'senkou_b']].shift(displacement)


# Determines intersection points between two lines
# TODO: add confirmation period
def lines_intersect(line1, line2):
    intersections = []
    l1_gt_l2 = line1 > line2
    current_val = l1_gt_l2.pop(l1_gt_l2.index[0])
    for next_val in l1_gt_l2:
        intersections.append(current_val != next_val)
        current_val = next_val

    return intersections


# Creates chart with i-cloud
# def chart(df, intersections):
def chart(df, chart_title, signals=None):
    x = df['date']

    fig, ax = plt.subplots(figsize=(20, 20))
    plt.plot(x, df['senkou_a'], color='green', linewidth=0.5)
    plt.plot(x, df['senkou_b'], color='red', linewidth=0.5)
    plt.plot(x, df['tenkan'], color='blue')
    plt.plot(x, df['kijun'], color='maroon')
    plt.plot(x, df['price'], color='black', linewidth=1)
    if signals is not None:
        for i in df.index:
            if signals[i] == True:
                plt.axvline(x=x[i])

    # ax.set(xlabel='Date', ylabel='BTC price ($)', title='2019 BTC/USD price (Bitmex)')
    ax.set(xlabel='Date', ylabel='BTC price ($)')
    ax.set_title(chart_title)
    plt.rc('axes', labelsize=20)
    plt.rc('font', size=16)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.xticks(rotation=45)

    # Span A > Span B == green cloud
    # Span A < Span B == red cloud
    plt.fill_between(
        x, df['senkou_a'], df['senkou_b'],
        where=df['senkou_a'] >= df['senkou_b'],
        facecolor='limegreen',
        interpolate=True
    )
    plt.fill_between(
        x, df['senkou_a'], df['senkou_b'],
        where=df['senkou_a'] <= df['senkou_b'],
        facecolor='salmon',
        interpolate=True
    )
    plt.show()




import pandas as pd
from py.ichimoku import ichimoku, chart
from py.variables import hr_intervals, ichimoku_periods


for period in ichimoku_periods:
    for interval in hr_intervals:

        candles = pd.read_csv('data/' + interval + '/candles.csv')
        results = pd.read_csv('data/' + interval + '/results.csv')
        results = results[results.columns[1:]]

        period_str = '-'.join(map(str, period))

        ichimoku(candles, period)

        signals = results[period_str]
        date_range = candles['date'].dt.strftime('%Y-%m-%d').between('2017-01-01', '2017-12-27')

        title = '2017 Bull Run- ' + period_str + ' ' + interval + 'hrs'
        chart(candles[date_range], title, signals)
