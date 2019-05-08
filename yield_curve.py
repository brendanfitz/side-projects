# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 13:47:03 2019

@author: Brendan Non-Admin
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import fred_api as fred

series_ids = {'yield_rate_1mo': 'DGS1MO', 'yield_rate_3mo': 'DGS3MO', 
              'yield_rate_6mo': 'DGS6MO', 'yield_rate_1yr': 'DGS1', 
              'yield_rate_2yr': 'DGS2', 'yield_rate_3yr': 'DGS3', 
              'yield_rate_4yr': 'DGS5', 'yield_rate_10yr': 'DGS10', 
              'yield_rate_20yr': 'DGS20', 'yield_rate_30yr': 'DGS30'}

def main(argv):
    df = (fred.fred_series('DGS2MO', '2019-01-02', '2019-05-06')
          .set_index('date'))
    """ relplot with long format data """
    frames = [yield_df(series_id, col) for col, series_id in series_ids.items()]
    curve_dts = ['2019-01-02', '2019-02-01', '2019-03-01', 
                 '2019-04-01', '2019-05-01']
    mat_map = dict(zip(df.columns.tolist(), range(1, df.columns.size+1)))
    df = pd.concat(frames, axis=1)
    g = (df.loc[curve_dts, ]
          .stack()
          .reset_index()
          .rename(columns={'level_1': 'maturity', 0: 'interest_rate'})
          .assign(maturity_ord=lambda x: x.maturity.map(mat_map))
          .pipe((sns.relplot, 'data'), x='maturity_ord', y='interest_rate', 
                hue='date', kind='line'))
    xticklabels = [x.replace('yield_rate_', '') for x in list(mat_map.keys())]
    g.set(xticks=list(mat_map.values()), xticklabels=xticklabels)
    """ wide format data """
    df = (pd.concat(frames, axis=1)
          .T
          .reset_index()
          .rename(columns={'index': 'maturity'})
          .rename(columns=str)
          .rename(columns=lambda x: x.replace(' 00:00:00', ''))
          .assign(maturity=lambda x: x.maturity.str.replace('yield_rate_', '')))
    """ 2019 Yield Curves """
    f, axes = plt.subplots(4, 4, figsize=(14, 14), sharex=True, sharey=True)
    for i, ax_tup in enumerate(itertools.product(list(range(4)), list(range(4)))):
        ax = axes[ax_tup[0], ax_tup[1]]
        (df.iloc[:, 66 + i]
         .plot(use_index=True, ax=ax, rot=45, title=df.iloc[:, 66 + i].name))
        ax.set_xticklabels(df.maturity)
    plt.tight_layout()
    f.savefig('yield_curve_multiple_lineplots.png')
    """ 2019 Beginning of Month Yield Curves """
    curve_dts = ['2019-01-02', '2019-02-01', '2019-03-01', 
                 '2019-04-01', '2019-05-01']
    sns.set(rc={'figure.figsize':(32,16)})
    fig, ax = plt.subplots(figsize=(24, 16))
    ax = (df.loc[:, curve_dts]
          .pipe((sns.lineplot, 'data'), ax=ax, palette="tab10", linewidth=2.5))
    ax.set_xticklabels(df.maturity, rotation=45)
    ax.set(title='Yield Curve', xlabel='Maturity', ylabel='Interest Rate')
    plt.tight_layout()
    ax.figure.savefig(r'Data\yield_curve.png')

def yield_df(series_id, col):
    return (fred.fred_series(series_id, '2019-01-01', '2019-05-06')
            .set_index('date')
            .query('value != "."')
            .assign(value=lambda x: x.value.astype('float64'))
            .rename(columns={'value': col}))
    
if __name__ == '__main__':
    main(sys.argv)