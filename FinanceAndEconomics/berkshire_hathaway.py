# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:59:59 2020

@author: Brendan Non-Admin
"""

import re
import pandas as pd

pat = re.compile('')

with open('Berkshire Hathaway 10-Q - 20Q1.txt', 'r') as f:
    lines = f.readlines()
    
lines_clean = []
for l in lines:
    split = str.split(l.replace(r'$ ', ''))
    if len(split) > 2:
        current_q = split[-2]
        last_q = split[-1]
        line_item = ' '.join(split[:-2])
    else:
        line_item = ' '.join(split)
        current_q = None,
        last_q = None
    lines_clean.append({
        'line_item': line_item,
        'current_q': current_q,
        'last_q': last_q,
    })
    
pd.DataFrame(lines_clean).to_csv('berkshire10q.csv', index=False)
    


