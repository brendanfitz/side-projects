# -*- coding: utf-8 -*-
"""
Created on Mon May  6 22:40:46 2019

@author: Brendan Non-Admin
"""

import pandas as pd
import requests
from fred_config import fred_api_key
import json


def series_url(series_id, observation_start, observation_end):
    url = (r'https://api.stlouisfed.org/fred/series/observations?'
           r'series_id=%(series_id)s&'
           r'api_key=%(api_key)s&'
           r'observation_start=%(observation_start)s&'
           r'observation_end=%(observation_end)s&'
           r'file_type=json')
    return url % {'series_id': series_id, 'api_key': fred_api_key,
                  'observation_start': observation_start, 
                  'observation_end': observation_end}

def series(series_id, observation_start, observation_end):
    url = series_url(series_id, observation_start, observation_end)
    response_text = requests.get(url).text
    json_data = json.loads(response_text)
    return (pd.DataFrame(json_data['observations'])
            .drop(['realtime_start', 'realtime_end'], axis=1)
            .rename(columns={'value': series_id}))
    
def category(category_id=0):
    url = (r'https://api.stlouisfed.org/fred/category/children?'
           r'category_id=%(category_id)s&'
           r'api_key=%(api_key)s&'
           r'file_type=json'
           ) % {'category_id': category_id, 'api_key': fred_api_key}
    response_text = requests.get(url).text
    json_data = json.loads(response_text)
    json_data
    return pd.DataFrame(json_data['categories']).set_index('id')