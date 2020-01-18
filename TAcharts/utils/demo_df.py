# File to create a quick, easy DataFrame using BTC's hourly 2019 prices
import requests
import pandas as pd



def demo_df(url=url):

    url = 'https://raw.githubusercontent.com/carlfarterson/TAcharts/master/data/btc.csv'

    _demo_df = pd.read_csv(url)
    return _demo_df
