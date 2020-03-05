# -*- coding: utf-8 -*-
"""
Created on Thu May  9 22:12:24 2019

@author: Brendan Non-Admin
"""

import numpy as np
import pandas as pd
import fred_api as fred
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib_util as mplu

series_ids = ['DGS2', 'DGS10', 'T10Y2Y']
frames = [fred.series(x, '2018-01-01', '2018-12-31').set_index('date') for x in series_ids]
df = (pd.concat(frames, axis=1).query('DGS2 != "."')
      .transform(lambda x: x.astype('float64')))

mask = (df.DGS10 - df.DGS2) != df.T10Y2Y
df.loc[mask, :].head()

df = df.assign(diff=lambda x: x.DGS10 - x.DGS2)

sns.set_style('darkgrid')
figsize = (22.14, 16.54)
fig, ax = plt.subplots(figsize=figsize)
df.pipe((sns.lineplot, 'data'), palette='tab10', linewidth=2.5, 
        markers=True, ax=ax)
ax.xaxis.set_major_locator(plt.MaxNLocator(12))
ax.set(title='10 Year vs 2 Year Yields', xlabel='', ylabel='Yield')
sns.despine()
mplu.rotate_xticklabels(ax, 45)

figsize = (22.14, 16.54)
fig, ax = plt.subplots(figsize=figsize)
(df.loc[:, ['DGS10']]
 .assign(DGS10=lambda x: x.DGS10.rolling(10).mean(),
         DGS10_1=lambda x: np.gradient(x.DGS10),
         DGS10_2=lambda x: np.gradient(x.DGS10_1))
 .drop(['DGS10_1', 'DGS10'], axis=1)
 .pipe((sns.lineplot, 'data'), palette='tab10', linewidth=2.5, 
       markers=True, ax=ax))
ax.xaxis.set_major_locator(plt.MaxNLocator(12))
ax.set(title='10 Year Yields and Gradients', xlabel='', ylabel='Yield')
sns.despine()
mplu.rotate_xticklabels(ax, 45)
plt.tight_layout()
fig.savefig(r'Data\Gradient.png')