# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 17:03:16 2020

@author: Brendan Non-Admin
"""

import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.expanduser('~'), 'Documents', 'config.ini'))

tc = config['twitter']


import pandas as pd
import requests
import base64
import json
# from twitter_config import tc
import datetime as dt
import urllib
import json


_strftime_fmt = '%Y%m%d%H%M'

_base_url = r'https://api.twitter.com/'

def authenticate():
    key_secret = '{}:{}'.format(tc['api_key'], tc['api_secret_key']).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    auth_url = '{}oauth2/token'.format(_base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    access_token = auth_resp.json()['access_token']
    
    return access_token

def user_lookup(access_token, screen_name):
    request_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }
    request_params = {
        'screen_name': screen_name,
    }
    url = 'https://api.twitter.com/1.1/users/lookup.json'
    response = requests.get(url, headers=request_headers, params=request_params)

    data = response.json()[0]
    _id = data.get('id')
    
    return _id

def scrape_elon_musk_tweets(access_token, _next=None):
    """    
    Example Token String
    --------------------
    '{"query": "from:elonmusk tesla", "fromDate": "202007010000", "toDate": "202007100000"}'
    """
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'content-type': 'application/json'
    }
    payload = {
        "query": "from:elonmusk tesla", 
        "maxResults": "100",
        "fromDate": dt.datetime(2017, 1, 1).strftime(_strftime_fmt), 
        "toDate": dt.date.today().strftime(_strftime_fmt),
    }
    if _next:
        payload['next'] = _next
       
    url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/nlpanalysis.json'
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_data = response.json()
          
    try:
        df = (pd.DataFrame(response_data.get('results'))
            .assign(
                created_at=lambda x: pd.to_datetime(x.created_at),
                screen_name=lambda x: x.user.apply(lambda x: x.get('screen_name'))
            )
        )
        _next = response_data.get('next')
    except Exception as e:
        print(response_data)
        if 'errors' in df.columns.tolist():
            print(df.errors)
        raise e
    
    return df, _next


def main():
    access_token = authenticate()
    
    frames = list()
    _next = None
    while True:
        df, _next = scrape_elon_musk_tweets(access_token, _next)
        frames.append(df)
        if _next is None:
            break
        
    df = pd.concat(frames)
    filepath = r'Data/elon_musk_tweets.csv'
    df.to_csv(filepath, index=False)
    print(f"Success\n\nSee file located at '{filepath}'")
    
if __name__ == '__main__':
    main()