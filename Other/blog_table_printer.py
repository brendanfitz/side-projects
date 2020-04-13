# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 13:41:33 2020

@author: Brendan Non-Admin
"""

import os
import pandas as pd
import psycopg2
from connection_config import cc_heroku_psycopg2 as cc

fpath = os.path.join(
    os.path.expanduser('~'),
    'Documents',
    'GitHub',
    'metis-projects-flask-app',
    'metis_app',
    'blog_posts',
    'templates',
    'blog_posts',
    'include_docs',
    'last_four_weeks_ending_udf',
)

conn = psycopg2.connect(**cc)

code_range = range(2, 4)
filenames = ['code{}.sql'.format(x) for x in code_range]

for i, num in enumerate(code_range):
    filename = filenames[i]
    file = os.path.join(fpath, filename)
    sql = open(file, 'r').read()
    df = pd.read_sql(sql, conn)
    html = (df.head(15)
            .to_html(classes="table", index=False, border=0, justify="left")
            .replace('class="dataframe ', 'class="')
           )
    fout = os.path.join(fpath, "table{}.html".format(num))
    with open(fout, 'w') as f:
        f.write(html)

conn.close()