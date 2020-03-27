# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:09:46 2020

@author: Brendan Non-Admin
"""


import pandas as pd
import sqlalchemy as db
from tqdm import tqdm
from connection_config import cc

db_url = db.engine.url.URL(**cc)
engine = db.create_engine(db_url)
conn = engine.connect()
metadata = db.MetaData()

stock_prices = db.Table('stock_prices', metadata,
                        db.Column('ticker', db.String(255), primary_key=True),
                        db.Column('date', db.Date(), primary_key=True),
                        db.Column('open', db.Numeric()),
                        db.Column('high', db.Numeric()),
                        db.Column('low', db.Numeric()),
                        db.Column('close', db.Numeric()),
                        db.Column('adj_close', db.Numeric()),
                        db.Column('volume', db.BigInteger()),
                        schema='visualizations'
                        )

metadata.create_all(engine)
    
data = (pd.read_csv('^GSPC.csv')
    .rename(columns=lambda x: x.lower().replace(' ', '_'))
    .assign(
            ticker='^GSPC',
            date=lambda x: pd.to_datetime(x.date)
            )
    .to_dict('records')
)   

for row in tqdm(data):
    query = db.insert(stock_prices).values(**row) 
    result_proxy = conn.execute(query)
    
conn.close()