# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 09:20:27 2020

@author: Brendan Non-Admin
"""

import pandas as pd
import requests
import matplotlib.pyplot as plt
from textwrap import wrap
plt.style.use('ggplot')

url = 'https://www.tsa.gov/coronavirus/passenger-throughput'
response = requests.get(url)
frames = pd.read_html(response.content)


def set_columns(input_df, index_label):
    df = input_df.copy()
    df.columns = df.loc[index_label]
    df = df.drop(index_label)
    return df

df = (frames[0]
    .pipe(set_columns, 0)
    .assign(Date=lambda x: pd.to_datetime(x.Date))
    .set_index('Date')
    .applymap(pd.to_numeric)
)

ax = df.rolling(4).mean().plot(figsize=(12, 5))
ax.legend(loc=0, bbox_to_anchor=(1, 1))

first_axis = [
    'Total Traveler Throughput',
    'Total Traveler Throughput  (1 Year Ago - Same Weekday)', 
]
second axis = ['YoY Change']

df.loc[:, first_axis].plot()

ax1 = df.loc[:, first_axis].rolling(4).mean().plot(figsize=(12, 4))
ax1.legend(labels, loc=0, bbox_to_anchor=(1.2, 1)) # move legend to the side
ax1.yaxis.set_major_formatter(fmt)
ax1.set_title('TSA checkpoint Travel Numbers')

ax2 = ax1.twinx()
df.loc[:, second_axis].plot(ax=ax2, c='k', legend=True)
ax2.legend(labels, loc=0, bbox_to_anchor=(1.2, 0.25))


ax = df.rolling(4).mean().plot(figsize=(12, 5))
ax.legend(loc=0, bbox_to_anchor=(1, 1))

df.iloc[:-7*4] # last four weeks

labels = [ '\n'.join(wrap(l, 20)) for l in df.columns]
#ax = df.iloc[-7*2:].plot(figsize=(12, 4))
ax = df.iloc[:7*2, 0].plot(figsize=(12, 4))
ax.legend(labels, loc=0, bbox_to_anchor=(1, 1))
