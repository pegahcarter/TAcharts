#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pandas as pd
import io
import requests


# Fetch BTC's 2019 price in CSV from github in case no df is presented
url = 'https://raw.githubusercontent.com/carlfarterson/TAcharts/master/data/btc-2019.csv'
content = requests.get(url).content
demo_df = pd.read_csv(io.StringIO(content.decode('utf-8')))
