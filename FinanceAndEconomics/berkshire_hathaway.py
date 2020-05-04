# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:59:59 2020

@author: Brendan Non-Admin
"""

import re
import io
import numpy as np
import pandas as pd

filename = 'Berkshire Hathaway 10-Q - 20Q1.txt'
#with open(filename, 'r') as f:
#    lines = f.readlines()
    
def line_clean(l):
    return l.replace(r'$ ', '').replace(' )', ')')

f = io.open(filename, mode="r", encoding="utf-8")
lines = f.read()
lines = [line_clean(x) for x in lines.split('\n') if x != '']
f.close()

l = lines[177]

badtext = l
encoded = badtext.encode('cp1252')
goodtext = encoded.decode('utf-8')

l8 = l.encode('utf8')
repr(l), repr(l8)
    
lines_clean = []
for l in lines:
    
    if totals_pat.search(l):
        match = totals_pat.search(l)
        
        start = match.start()
        line_item = l[:start - 1]
        
        data = match.group('data')
        current_q, last_q = data.split(' ', maxsplit=2)
    else:
        line_item = l
        current_q = np.nan
        last_q = np.nan
    lines_clean.append({
        'line_item': line_item,
        'current_q': current_q,
        'last_q': last_q,
    })

(pd.DataFrame(lines_clean)
    .to_csv('berkshire10q.csv', index=False, encoding='cp1252')
)


