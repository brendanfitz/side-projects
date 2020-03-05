# -*- coding: utf-8 -*-
"""
Created on Sun May  5 23:29:44 2019

@author: Brendan Non-Admin
"""

import pandas as pd
import numpy as np
import requests
from fred_config import fred_api_key
import json
import seaborn as sns


def series_url(series_id, api_key, realtime_start, realtime_end):
    url = (r'https://api.stlouisfed.org/fred/series/observations?'
           r'series_id=%(series_id)s&'
           r'api_key=%(api_key)s&'
           r'realtime_start=%(realtime_start)s&'
           r'realtime_end=%(realtime_end)s&'
           r'file_type=json')
    return url % {'series_id': series_id, 'api_key': api_key,
                  'realtime_start': realtime_start, 
                  'realtime_end': realtime_end}

url = series_url('FEDFUNDS', fred_api_key, '2019-04-01', '2019-04-30')
json_text = requests.get(url).text
json = json.loads(json_text)

df = (pd.DataFrame(json['observations'])
      .set_index('date')
      .rename(columns={'value': 'fed_funds_rate'})
      .assign(fed_funds_rate=lambda x: x.fed_funds_rate.astype('float64')))

ax = (df.loc[:, ['fed_funds_rate']]
      .assign(fed_funds_rate_1_yr=lambda x: x.fed_funds_rate.rolling(12).mean())
      .assign(fed_funds_rate_5_yr=lambda x: x.fed_funds_rate.rolling(12 * 5).mean())
      .pipe((sns.lineplot, 'data'), palette="tab10", linewidth=2.5))
ax.figure.savefig(r'Data\fed_funds_rate.png')

df.nlargest(10, 'fed_funds_rate').loc[:, ['fed_funds_rate']]
df.head()
df.tail()