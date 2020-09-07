# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:28:23 2020

@author: Brendan Non-Admin
"""

import os
import pandas as pd

datapath = os.path.join(
    os.path.expanduser('~'),
    'Documents',
    'DocsBF',
    'Investing',
    'Levi'
)

filename = 'Levi --10Q--20Q2.xlsx'
filepath = os.path.join(datapath, filename)
df = pd.read_excel(filepath)

sheet_names = [
    'Consolidated Balance Sheets',
    'Consolidated Statements of Oper',
    'Consolidated Statements of Comp',
]
frames = list()
for sheet_name in sheet_names:
    df = pd.read_excel(filepath, sheet_name, index_col=1)
    frames.append(df)


df = frames[1]
df.columns
