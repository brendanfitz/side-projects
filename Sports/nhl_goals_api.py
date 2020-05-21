# -*- coding: utf-8 -*-
"""
Created on Thu May 21 10:51:24 2020

@author: Brendan Non-Admin
"""

import pandas as pd
import requests
import urllib.parse as up
import json
import copy
import os

url = 'https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D,%7B%22property%22:%22assists%22,%22direction%22:%22DESC%22%7D%5D&start=101&limit=100&factCayenneExp=gamesPlayed%3E=1&cayenneExp=gameTypeId=2%20and%20seasonId%3C=20192020%20and%20seasonId%3E=20192020'

response = requests.get(url)
data = json.loads(response.text)

data['data'][0]
len(data['data'])

url_base, qstr = url.split('?')
qsobj = up.urlsplit(qstr)

up.parse_qsl(qstr)

def urlencode_wrapper(qstrobj):
    return (up.urlencode(qstrobj, quote_via=up.quote)
        .replace('%3D', '=')
        .replace('%3A', ':')
        .replace('%2C', ',')
        .replace('%5B%27', '')
        .replace('%27%5D', '')
    )

qstr == urlencode_wrapper(up.parse_qs(qstr))

qstrobj = up.parse_qs(qstr)
qstrobj['cayenneExp'][0] = qstrobj['cayenneExp'][0].replace('20192020', '{year}')


def generate_qstrobj(qstrobj, start, year):
    qstrobj = copy.deepcopy(qstrobj)
    qstrobj['start'] = start
    qstrobj['cayenneExp'][0] = qstrobj['cayenneExp'][0].format(year=year)
    return urlencode_wrapper(qstrobj)

start = 101
year = '20002001'
    
qstr_pagination_adj = urlencode_wrapper(qstrobj)
url_pagination_adj = url_base + '?' + qstr_pagination_adj

years = [str(x) + str(x+1) for x in range(2000, 2021, 1)]
pagination = [0] + [x * 100 + 1 for x in range(1, 4)]
frames = []

for year in years:
    for start in pagination:
        url = url_base + '?' + generate_qstrobj(qstrobj, start, year)
        response = requests.get(url)
        data = json.loads(response.text)
        frames.append(pd.DataFrame.from_records(data['data']))

df = pd.concat(frames)

filename = os.path.join('data', 'nhl_player_data_2000-2020.csv')
df.to_csv(filename, index=False)




