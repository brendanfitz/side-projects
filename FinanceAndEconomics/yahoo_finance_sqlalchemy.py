# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:09:46 2020

@author: Brendan Non-Admin
"""


import pandas as pd
import sqlalchemy as db
from tqdm import tqdm
from connection_config import cc_heroku as cc

db_url = db.engine.url.URL(**cc)
engine = db.create_engine(db_url)
conn = engine.connect()
metadata = db.MetaData()
schema_name = 'visualizations'

if not engine.dialect.has_schema(engine, schema_name):
    engine.execute(db.schema.CreateSchema(schema_name))

stock_prices = db.Table('stock_prices', metadata,
                        db.Column('ticker', db.String(255), primary_key=True),
                        db.Column('date', db.Date(), primary_key=True),
                        db.Column('open', db.Numeric()),
                        db.Column('high', db.Numeric()),
                        db.Column('low', db.Numeric()),
                        db.Column('close', db.Numeric()),
                        db.Column('adj_close', db.Numeric()),
                        db.Column('volume', db.BigInteger()),
                        schema=schema_name
                        )

metadata.create_all(engine)
    

def filter_dates(input_df, year):
    df = input_df.copy()
    return df.loc[df.date >= year, ]

data = (pd.read_csv('^GSPC.csv')
    .rename(columns=lambda x: x.lower().replace(' ', '_'))
    .assign(
            ticker='^GSPC',
            date=lambda x: pd.to_datetime(x.date)
            )
    .pipe(filter_dates, year='1990')
    .to_dict('records')
)
    
for row in tqdm(data):
    query = db.insert(stock_prices).values(**row) 
    result_proxy = conn.execute(query)
    
conn.close()