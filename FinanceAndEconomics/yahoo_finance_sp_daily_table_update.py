# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 18:56:33 2020

@author: Brendan Non-Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:33:04 2020

@author: Brendan Non-Admin
"""

import pandas as pd
import urllib.parse
import datetime as dt
import requests
import sqlalchemy as db
from connection_config import cc
from tqdm import tqdm

def main():
    
    db_url = db.engine.url.URL(**cc)
    
    engine = db.create_engine(db_url)
    conn = engine.connect()
    metadata = db.MetaData()
    stock_prices = db.Table('stock_prices', metadata, 
        autoload=True,
        autoload_with=engine,
        schema='visualizations'
    )
    
    """ future parameters """
    ticker = "^GSPC"
    df = scrape_daily_stock_price_df(ticker)
    
    data = df.to_dict('records')
    
    for row in tqdm(data):
        query = db.insert(stock_prices).values(**row) 
        conn.execute(query)
    
    conn.close()

def calculate_epoch(date):
    return (date - dt.datetime(1970, 1, 1)).total_seconds()


def create_url(ticker, start_date=None, end_date=None):
    """
    Returns data inclusive of both start_date and end_date
    """
    if start_date is None:
        time_to_zeros = dict(hour=0, minute=0, second=0, microsecond=0)
        start_date = dt.datetime.today().replace(**time_to_zeros)
        
    if end_date is None:
        end_date = start_date + dt.timedelta(days=1)
        
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
        .reset_index()
        .assign(ticker=ticker)
    )
    
    return df

if __name__ == 'main':
    main()