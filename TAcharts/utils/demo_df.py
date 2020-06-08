# File to create a quick, easy DataFrame using BTC's hourly 2019 prices
import requests
import pandas as pd
from datetime import datetime


def demo_df(url=None):

    if url is None:
        url = "https://raw.githubusercontent.com/carlfarterson/TAcharts/master/data/btc.csv"

    try:
        _demo_df = pd.read_csv(url)
        return _demo_df
    except:
        return
