# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 13:47:03 2019

@author: Brendan Non-Admin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

"""
import requests
import xml.etree.ElementTree as ET
url = (r'https://www.treasury.gov/resource-center/data-chart-center'
       r'/interest-rates/Datasets/yield.xml')
xml = requests.get(url).text
root = ET.fromstring(xml)
node = (root.find('LIST_G_WEEK_OF_MONTH')
        .find('G_WEEK_OF_MONTH')
        .find('LIST_G_NEW_DATE'))
cols_names = ['date', '1 mo', '2 mo', '3 mo', '6 mo', '1 yr', '2 yr', '3 yr',
              '5 yr',  '7 yr', '10 yr', '20 yr', '30 yr']
rows = list()
for child in node:
    row = list()
    row.append(child.find('BID_CURVE_DATE').text)
    for gchild in child.find('LIST_G_BC_CAT').find('G_BC_CAT'):
        row.append(gchild.text)
    rows.append(row)
"""
df = (pd.read_excel('yield_curve_data.xlsx')
      .set_index('Date')
      .T
      .reset_index()
      .rename(columns={'index': 'maturity'})
      .rename(columns=str)
      .rename(columns=lambda x: x.replace(' 00:00:00', '')))

f, axes = plt.subplots(4, 4, figsize=(14, 14), sharex=True, sharey=True)
for i, ax_tup in enumerate(itertools.product(list(range(4)), list(range(4)))):
    ax = axes[ax_tup[0], ax_tup[1]]
    (df.iloc[:, 66 + i]
     .plot(use_index=True, ax=ax, rot=45, title=df.iloc[:, 66 + i].name))
    ax.set_xticklabels(df.maturity)
plt.tight_layout()
f.savefig('yield_curve_multiple_lineplots.png')

def plot_yield_curve(df, dt_str):
    yticks = np.arange(2, 4, 0.5)
    ax = df[dt_str].plot(use_index=True, xticks=df.index, yticks=yticks, 
                         rot=45)
    ax.set_xticklabels(df.maturity)
    plt.show()
    
for col in df.columns.tolist()[1:]:
    plot_yield_curve(df, col)
    
plot_yield_curve(df, )


curve_dts = ['2019-01-02', '2019-02-01', '2019-03-01', 
             '2019-04-01', '2019-05-01']
sns.set(rc={'figure.figsize':(32,16)})
fig, ax = plt.subplots(figsize=(24, 16))
ax = (df.loc[:, curve_dts]
      .pipe((sns.lineplot, 'data'), ax=ax, palette="tab10", linewidth=2.5))
ax.set_xticklabels(df.maturity, rotation=45)
ax.set(title='Yield Curve', xlabel='Maturity', ylabel='Interest Rate')
plt.tight_layout()
ax.figure
ax.figure.savefig("yield_curve.png")