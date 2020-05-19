# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:32:03 2020

@author: Brendan Non-Admin
"""

import pandas as pd
from urllib.parse import urlencode
import requests
import json
from alpha_vantage_config import API_KEY
from pandas.tseries.offsets import Minute

BASE_URL = 'https://www.alphavantage.co/query?'

def alpha_vantage_query(function, symbol, interval, **kwargs):
    params = dict()
    params['function'] = function
    params['symbol'] = symbol
    params['interval'] = interval
    params['apikey'] = API_KEY
    params.update(kwargs)
       
    try:
        qstr = urlencode(params)
        response = requests.get(BASE_URL + qstr)
    
        data = json.loads(response.text)
        data_key = [x for x in list(data.keys()) if x != 'Meta Data'][0]
        
        df = pd.DataFrame.from_dict(data[data_key], orient='index')
        df.index = pd.to_datetime(df.index, )
        df = df.asfreq(freq='5min')
    except:
        print(params)
        print(response.status_code, response.text)
        raise

    return df


symbol = 'AAPL'
interval = '5min'

kwargs = {
    'outputsize': 'full',
}
df_price = alpha_vantage_query('TIME_SERIES_INTRADAY', symbol, interval, **kwargs)

kwargs = {}
df_vwap = alpha_vantage_query('VWAP', symbol, interval, **kwargs)

kwargs = {
    'series_type': 'close',
    'time_period': 20,
}
df_bbands = alpha_vantage_query('BBANDS', symbol, interval, **kwargs)

df = df_price.join(df_vwap).join(df_bbands).sort_index()

df.head()







