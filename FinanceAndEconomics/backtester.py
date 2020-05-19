# -*- coding: utf-8 -*-
"""
Created on Sun May 17 18:06:04 2020

@author: Brendan Non-Admin
"""

import pandas as pd
from backtesting import Backtest
from backtesting.lib import SignalStrategy
from alpha_vantage_test import alpha_vantage_query

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
})

df_rsi_lag = df.loc[:, ['RSI']].shift(1).rename(columns={'RSI': 'RSI_Lag'})
df = df.join(df_rsi_lag)

class RsiTrough(SignalStrategy):
    
    def init(self):
        # In init() and in next() it is important to call the
        # super method to properly initialize all the classes
        super().init()
        
        # Taking a first difference (`.diff()`) of a boolean
        # series results in +1, 0, and -1 values. In our signal,
        # as expected by SignalStrategy, +1 means buy,
        # -1 means sell, and 0 means to hold whatever current
        # position and wait. See the docs.
        crossing_below_20 = ((self.data.RSI < 20) & (self.data.RSI > 20)).astype(int)
        crossing_above_40 = ((self.data.RSI > 40) & (self.data.RSI < 40)).astype(int) * -1
        signal = crossing_below_20 + crossing_above_40
        
        # Set the signal vector using the method provided
        # by SignalStrategy
        self.set_signal(signal)
        
            

backtest = Backtest(df, RsiTrough, cash=1000, commission=.002)

output = backtest.run()
backtest.plot()
