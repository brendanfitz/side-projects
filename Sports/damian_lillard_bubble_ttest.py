# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 17:43:10 2020

@author: Brendan Non-Admin

background: Damian Lillard claims it was easier to play in the bubble than normal
Let's run a t-test of his points in and out of the bubble to see if there was a statistically significant uptick in points
"""

import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import t

filename = 'data/Damian Lillard 2019-20 Game Log _ Basketball-Reference.com.html'

tables = pd.read_html(filename)

for table in tables:
    print(table.columns[:4])

df_full = (pd.concat(tables[-2:], axis=0)
    .query('Rk != "Rk"')
)

df_full.iloc[:, 0:5].head()

df_full.columns.tolist()

subset = ['Rk', 'G', 'Date', 'Opp', 'PTS']
mask = df_full.loc[:, subset].isna().any(axis=1)
df_full.loc[mask, subset]

df  = (df_full.loc[~mask, subset]
    .astype({
        'Rk': 'int32', 
        'G': 'int32', 
        'Date': 'datetime64',
        'PTS': 'int32'
    })
    .assign(bubble = lambda x: (x.Date >= '2020-04-01').astype('int32'))
)

calcs = (df.groupby('bubble')
    .agg({
        'PTS': ['mean', 'std', 'count']
    })
)

pts_mean = calcs.loc[:, ('PTS', 'mean')]
per_inc = (pts_mean[1] / pts_mean[0] - 1) * 1
print(f"Percent Increase in Bubble: {per_inc:.2%}")

n1, n2 = calcs.loc[:, ('PTS', 'count')]

y_bar1, y_bar2 = calcs.loc[:, ('PTS', 'mean')]
y_bar_diff = y_bar1 - y_bar2

s1, s2 = calcs.loc[:, ('PTS', 'std')]

degf = min(n1 - 1, n2 - 1)

conf_level = 0.95
perc_crit_value = conf_level + ((1 - conf_level)  / 2)

t_star = t.ppf(perc_crit_value, degf)

se = ((s1**2 / n1) + (s2**2 / n2))**(1/2)

# ht
t_stat = y_bar_diff / se
p_value = t.cdf(-abs(t_stat), degf) * 2

# ci
margin_o_err = t_star * se
ci = y_bar_diff + np.array([-1, 1]) * margin_o_err

l, u = -3 * se, 3 * se
x = np.arange(l, u, (u - l) / 1000)
y= t.pdf(x, degf)

ax = sns.lineplot(x, y)
ax.vlines(t_stat, 0, max(y), colors='r', alpha=0.7, width=2)
ax.axvspan(l, t_stat, alpha=0.3, color='red')



df.to_csv('data/damian_lillard.csv', index=False)

sns

g = sns.FacetGrid(df, row='bubble')
g.map_dataframe(sns.distplot, x='PTS')

sns.distplot(df.PTS, kde=False, hue=df.bubble)
