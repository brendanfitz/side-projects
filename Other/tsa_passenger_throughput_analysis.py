# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 09:43:22 2020

@author: Brendan Non-Admin
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import wrap
from matplotlib.ticker import FuncFormatter
plt.style.use('ggplot')

url = 'https://www.tsa.gov/coronavirus/passenger-throughput'
response = requests.get(url)

frames = pd.read_html(response.content)

df = frames[0]
df.columns = df.iloc[0].tolist()
df = df.drop(0)
df = df.assign(Date=lambda x: pd.to_datetime(x.Date)).set_index('Date')
df = df.applymap(pd.to_numeric)


df.plot()
fmt =  FuncFormatter(lambda x, p: format(int(x), ','))
labels = [ '\n'.join(wrap(l, 10)) for l in df.columns]
ax = df.rolling(4).mean().plot(figsize=(12, 4))
ax.legend(labels, loc=0, bbox_to_anchor=(1, 1)) # move legend to the side
ax.yaxis.set_major_formatter(fmt)
ax.set_title('TSA checkpoint Travel Numbers')

dividend = 'Total Traveler Throughput'
divisor = 'Total Traveler Throughput  (1 Year Ago - Same Weekday)'
df.loc[:, 'YoY Change'] = df.loc[:, dividend] / df.loc[:, divisor] - 1

df.loc[:, 'YoY Change'].rolling(7).mean().plot()

df.loc[:, 'YoY Change'].ewm(7).mean().plot()

first_axis = [
    'Total Traveler Throughput',
    'Total Traveler Throughput  (1 Year Ago - Same Weekday)', 
]
second_axis = ['YoY Change']

ax1 = df.loc[:, first_axis].rolling(4).mean().plot(figsize=(12, 4))
ax1.legend(labels, loc=0, bbox_to_anchor=(1.2, 1)) # move legend to the side
ax1.yaxis.set_major_formatter(fmt)
ax1.set_title('TSA checkpoint Travel Numbers')

ax2 = ax1.twinx()
df.loc[:, second_axis].plot(ax=ax2, c='k', legend=True)
ax2.legend(labels, loc=0, bbox_to_anchor=(1.2, 0.25))

