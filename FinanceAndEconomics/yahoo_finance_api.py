# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:33:04 2020

@author: Brendan Non-Admin
"""

import pandas as pd
import urllib.parse
import datetime as dt
import requests

def calculate_epoch(date):
    return (date - dt.datetime(1970,1,1)).total_seconds()


""" future parameters """
ticker = "^GSPC"
start_date = dt.datetime(1927, 12, 29, 0, 0)
end_date = dt.datetime(2020, 3, 23)


""" uri """
ticker_url_encoded = urllib.parse.quote(ticker)
uri = "https://finance.yahoo.com/quote/{}/history".format(ticker_url_encoded)

epoch_start = calculate_epoch(start_date + dt.timedelta(days=1))
epoch_end = calculate_epoch(end_date + dt.timedelta(days=1))
qstr = ("period1={:.0f}&period2={:.0f}&interval=1d&filter=history&frequency=1d"
        .format(epoch_start, epoch_end))
url = uri + "?" + qstr

response = requests.get(url)

df = pd.read_html(response.text)[0].iloc[0:-1]

df = (df.rename(columns=lambda x: x.replace(' ', '_').replace('*', '').lower())
    .set_index('date')
    .apply(lambda x: pd.to_numeric(x))
)