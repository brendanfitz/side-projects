# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:32:03 2020

@author: Brendan Non-Admin
"""

import pandas as pd
from urllib.parse import urlencode
import requests
import json
from alpha_vantage_config import API_KEY
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.style.use('ggplot')

BASE_URL = 'https://www.alphavantage.co/query?'    

def alpha_vantage_query(function, symbol, interval=None, **kwargs):
    params = dict()
    params['function'] = function
    params['symbol'] = symbol
    
    if interval:
        params['interval'] = interval
    
    params['apikey'] = API_KEY
    params.update(kwargs)
       
    try:
        response = requests.get(BASE_URL, params)
    
        data = json.loads(response.text)
        if function in ['INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW']:
            return data
        data_key = [x for x in list(data.keys()) if x != 'Meta Data'][0]
        
        df = pd.DataFrame.from_dict(data[data_key], orient='index')
        df.index = pd.to_datetime(df.index, )
        #df = df.asfreq(freq='5min')
    except:
        print(params)
        print(response.status_code, response.text)
        raise

    return df

data = alpha_vantage_query('INCOME_STATEMENT', 'TSLA')


df_annual = (pd.DataFrame(data['annualReports'])
    .assign(
        fiscalDateStarting=lambda x: pd.to_datetime(x.fiscalDateEnding) + pd.tseries.offsets.QuarterBegin(),
        fiscalDateEnding=lambda x: pd.to_datetime(x.fiscalDateEnding)
    )
    .set_index('fiscalDateEnding')
    .applymap(lambda x: pd.to_numeric(x, errors='coerce'))
)

df_quarter = (pd.DataFrame(data['quarterlyReports'])
    .assign(
        fiscalDateStarting=lambda x: pd.to_datetime(x.fiscalDateEnding) + pd.tseries.offsets.QuarterBegin(),
        fiscalDateEnding=lambda x: pd.to_datetime(x.fiscalDateEnding)
    )
    .set_index('fiscalDateEnding')
    .applymap(lambda x: pd.to_numeric(x, errors='coerce'))
)


fig, ax = plt.subplots()
ax = df_quarter.loc[:, 'netIncome'].sort_index().plot(ax=ax)
#quarters = mdates.MonthLocator((1, 4, 7, 10))
#months =  mdates.MonthLocator()
# quarters_fmt = mdates.DateFormatter('%Y %m')
# ax.xaxis.set_major_locator(quarters)
# ax.xaxis.set_major_formatter(months_fmt)
# ax.xaxis.set_minor_locator(months)
fig.autofmt_xdate()
ax.set_xlabel('')
ax.set_title('MGM Quarterly Earnings')
plt.show()

fig, ax = plt.subplots()
ax = df_quarter.loc[:, 'netIncome'].sort_index().plot(ax=ax)
#quarters = mdates.MonthLocator((1, 4, 7, 10))
#months =  mdates.MonthLocator()
# quarters_fmt = mdates.DateFormatter('%Y %m')
# ax.xaxis.set_major_locator(quarters)
# ax.xaxis.set_major_formatter(months_fmt)
# ax.xaxis.set_minor_locator(months)
fig.autofmt_xdate()
ax.set_xlabel('')
ax.set_title('MGM Quarterly Earnings')
plt.show()


fig, ax = plt.subplots()
ax = df_annual.loc[:, 'netIncome'].sort_index().plot(ax=ax)
#quarters = mdates.MonthLocator((1, 4, 7, 10))
#months =  mdates.MonthLocator()
# quarters_fmt = mdates.DateFormatter('%Y %m')
# ax.xaxis.set_major_locator(quarters)
# ax.xaxis.set_major_formatter(months_fmt)
# ax.xaxis.set_minor_locator(months)
fig.autofmt_xdate()
ax.set_xlabel('')
ax.set_title('MGM Annual Earnings')
plt.show()
df_annual.loc[:, 'netIncome'].map('${:,.0f}'.format)

df_annual.columns


requests = 