# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:09:46 2020

@author: Brendan Non-Admin
"""


import datetime as dt
import sqlalchemy as db
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

dummy_data = [
        {
         'ticker': '^GSPC',
         'date': dt.date(2019, 1, 1),
         'open': 1.0, 
         'high': 3.0,
         'low': 0.5,
         'close': 2.0,
         'adj_close': 2.1,
         'volume': 100,
        },
        {
         'ticker': '^GSPC',
         'date': dt.date(2019, 1, 2),
         'open': 1.0, 
         'high': 3.0,
         'low': 0.5,
         'close': 2.0,
         'adj_close': 2.1,
         'volume': 100,
        }
]

query = db.insert(stock_prices)
result_proxy = conn.execute(query, dummy_data)