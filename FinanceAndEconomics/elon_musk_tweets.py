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

def scrape_elon_musk_tweets(access_token, max_id=None, tesla_tweets_only=False):
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'content-type': 'application/json'
    }
    data = {
        "query":"from:elonmusk tesla", 
        "fromDate": "202007010000", 
        "toDate": "202007100000"
    }
    if max_id:
        data['max_id'] = max_id
    
    #data = '{"query": "from:elonmusk tesla", "fromDate": "202007010000", "toDate": "202007100000"}'
    
    url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/nlpanalysis.json'
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.json()
    
    df = pd.DataFrame(json_data)
    
    try:
        next_max_id = df.id.min() - 1
    except Exception as e:
        print(request_params)
        if 'errors' in df.columns.tolist():
            print(df.errors)
        raise e        
    
    if tesla_tweets_only:
        mask = df.text.str.contains('Tesla')
        df = df.loc[mask, :]
    
    return df, next_max_id

frames = list()
next_max_id = None
access_token = authenticate()
while True:
    df, next_max_id = scrape_elon_musk_tweets(access_token, max_id=next_max_id)
    frames.append(df)
    if next_max_id is None:
        break
    
df = pd.concat(frames)

#timeline_mask = df.in_reply_to_user_id.isna()
#df = df.loc[timeline_mask, ]

mask = df.full_text.str.contains('Tesla', case=False)
df = df.loc[mask, :]

df = df.assign(created_at=lambda x: pd.to_datetime(x.created_at))

df.full_text.head()

df.to_csv(r'Data/elon_musk_tweets.csv', index=False)


endpoint = "https://api.twitter.com/1.1/tweets/search/fullarchive/nlpanalysis.json" 

data = '{"query":"tesla from:bf2398", "fromDate": "201901010000", "toDate": "202004010000"}'

data = '{"query":"tesla from:elonmusk", "fromDate": "201001010000", "toDate": "202004010000"}'
response = requests.post(endpoint,data=data,headers=headers)
response.json().get('results')

response.request.body