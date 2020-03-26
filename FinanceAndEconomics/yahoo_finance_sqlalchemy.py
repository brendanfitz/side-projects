# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:09:46 2020

@author: Brendan Non-Admin
"""


import pandas as pd
import sqlalchemy as db
from tqdm import tqdm
from connection_config import cc

protocol = cc['protocol']
username = cc['username']
password = cc['password']
host = cc['host']
database = cc['database']

engine = db.create_engine(f"{protocol}://{username}:{password}@{host}/{database}")
conn = engine.connect()
metadata = db.MetaData()

stock_prices = db.Table('stock_prices', metadata,
                        db.Column('ticker', db.String(255)),
                        db.Column('date', db.Date()),
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