# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:30:50 2020

@author: Brendan Non-Admin
"""

import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
df = pd.read_html(url)[0]

num_sp_companies = 505
if df.shape[0] != num_sp_companies:
    err_str = (
        "The S&P 500 contains {} companies, ".format(num_sp_companies) +
        "this table only has {}".format(df.shape[0])
    )
    raise ValueError(err_str)
    

dims = ['GICS Sector']
df.groupby(dims).size()

dims = ['GICS Sector', 'GICS Sub Industry']
df.groupby(dims).size()

mask = df.loc[:, 'GICS Sub Industry'] == 'Advertising'
df.loc[mask, ]