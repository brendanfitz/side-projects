# -*- coding: utf-8 -*-
"""
Created on Sun May 17 18:06:04 2020

@author: Brendan Non-Admin
"""

import pandas as pd
from backtesting import Backtest
from backtesting.lib import Strategy
from alpha_vantage_test import alpha_vantage_query
import numpy as np


"""
symbol = 'GPRO'
interval = '5min'

kwargs = {
    'outputsize': 'full',
}
df_price = alpha_vantage_query('TIME_SERIES_INTRADAY', symbol, interval, **kwargs)

kwargs = {
    'time_period': 14,
    'series_type': 'close'
}
df_rsi = alpha_vantage_query('RSI', symbol, interval, **kwargs)

df = df_price.join(df_rsi)

mask = ~df.isna().any(axis=1)
df = df.loc[mask, ]

df = df.sort_index()

df = df.apply(pd.to_numeric, axis=1)

df = df.rename(columns={
    '1. open': 'Open', 
    '2. high': 'High', 
    '3. low':'Low', 
    '4. close': 'Close',
    '5. volume': 'Volume',
})

df_rsi_lag = df.loc[:, ['RSI']].shift(1).rename(columns={'RSI': 'RSI_Lag'})
df = df.join(df_rsi_lag)

df.drop('RSI_Lag', axis=1).to_csv('GPRO.csv')
"""

df = pd.read_csv('GPRO.csv', index_col=0, dtype={
    'Open': np.dtype('float64'),
    'High': np.dtype('float64'),
    'Low': np.dtype('float64'),
    'Close': np.dtype('float64'),
    'Volume': np.dtype('float64'),
    'RSI': np.dtype('float64'),
    }, parse_dates=True)

class RsiTrough(Strategy):

    def init(self):
        self.rsi = self.data.RSI
        self.in_trade = False

    def next(self):
        print(self.rsi[0], self.rsi[1])
        if self.rsi[0] < 20 and self.rsi[1] > 20:
            self.buy()
            self.in_trade = True
        elif self.in_trade and self.rsi[0] > 40:
            self.sell()
            self.in_trade = False
        
            

backtest = Backtest(df, RsiTrough, cash=1000, commission=.002)

output = backtest.run()
backtest.plot()
