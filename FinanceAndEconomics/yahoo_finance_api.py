# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:33:04 2020

@author: Brendan Non-Admin
"""

import pandas as pd
import urllib.parse
import datetime as dt
import requests


def calculate_epoch(date):
    return (date - dt.datetime(1970, 1, 1)).total_seconds()


def create_url(ticker, start_date, end_date):
    """
    Returns data inclusive of both start_date and end_date
    """
    domain = "https://finance.yahoo.com/"
    
    ticker_url_encoded = urllib.parse.quote(ticker)
    path = "quote/{}/history".format(ticker_url_encoded)
    
    epoch_start = calculate_epoch(start_date)
    epoch_end = calculate_epoch(end_date + dt.timedelta(days=1))
    qstr = ("?period1={:.0f}&period2={:.0f}&interval=1d&filter=history&frequency=1d"
            .format(epoch_start, epoch_end))
    
    url = domain + path + qstr
    return url


def scrape_daily_stock_price_df(ticker, start_date, end_date):
    """
    Returns data inclusive of both start_date and end_date
    """
    url = create_url(ticker, start_date, end_date)

    response = requests.get(url)
    
    df = (pd.read_html(response.text)[0].iloc[0:-1]
        .rename(columns=lambda x: x.replace(' ', '_').replace('*', '').lower())
        .assign(date=lambda x: pd.to_datetime(x.date))
        .set_index('date')
        .apply(lambda x: pd.to_numeric(x))
    )
    
    return df

""" future parameters """
ticker = "^GSPC"

start_date = dt.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
end_date = start_date
df = scrape_daily_stock_price_df(ticker, start_date, end_date)

          