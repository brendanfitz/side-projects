# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 00:04:35 2019

@author: Brendan Non-Admin
"""

import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

stocks = ['AAPL', 'BA', 'GS']
df = (web.DataReader(stocks, data_source='iex', start='2019-04-08',
                    end='2019-04-22')
      .loc[:, 'close'])

sns.lineplot(data=df, palette="tab10", linewidth=2.5)

sns.lineplot(data=df.loc[:, ['AAPL', 'GS']], palette="tab10", linewidth=2.5)

amzn = (web.DataReader('AMZN', data_source='iex', 
                       start='2014-05-01', end='2019-05-01'))

amzn = amzn.set_index(pd.to_datetime(amzn.index))

(amzn.loc[:, 'close']
 .pipe((sns.lineplot, 'data'), palette="tab10", linewidth=2.5))

def rotate_xticklabels(ax, rot):
    for item in ax.get_xticklabels():
        item.set_rotation(rot)

ax = (amzn.loc['2016':'2018', ['close']]
      .assign(moving_average=amzn.close.rolling(28).mean())
      .pipe((sns.lineplot, 'data'), palette="tab10", linewidth=2.5))
rotate_xticklabels(ax, 30)
ax.set(title='Amazon Stock Price', xlabel='Date', ylabel='Price')
plt.legend(labels=('Closing Price', '28-Day Moving Average'))
sns.despine()
plt.show()

ax = (amzn.loc['2016':'2018', ['close']]
      .assign(moving_average=amzn.close.rolling(28).mean())
      .drop('close', axis=1)
      .pipe((sns.lineplot, 'data'), palette="tab10", linewidth=2.5))
rotate_xticklabels(ax, 30)
ax.set(title='Amazon Stock Price', xlabel='Date', ylabel='Price')
sns.despine()
plt.show()

ax = (amzn.loc[:, ['close']]
      .assign(moving_average_28d=amzn.close.rolling(28).mean(),
              moving_average_60d=amzn.close.rolling(60).mean(),
              moving_average_365d=amzn.close.rolling(365).mean())
      .drop('close', axis=1)
      .pipe((sns.lineplot, 'data'), palette="tab10", linewidth=2.5))
rotate_xticklabels(ax, 30)
ax.set(title='Amazon Stock Price', xlabel='Date', ylabel='Price')
plt.legend(labels=('28-Day Moving Average', '60-Day Moving Average',
                   '365-Day Moving Average'))
sns.despine()
plt.show()