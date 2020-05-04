# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:59:59 2020

@author: Brendan Non-Admin
"""

import re
import io
import numpy as np
import pandas as pd

   
def line_clean(l):
    return l.replace(r'$ ', '').replace(' )', ')')

def read_file(filename):
    f = io.open(filename, mode="r", encoding="utf-8")
    lines = f.read()
    lines = [line_clean(x) for x in lines.split('\n') if x != '']
    f.close()
    return lines

filename = 'Berkshire Hathaway 10-Q - 20Q1.txt'
lines = read_file(filename)

def scrape_line(l):
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
    return line_item, current_q, last_q
    
lines_clean = []
for l in lines:
    
    line_item, current_q, last_q = scrape_line(l)
    lines_clean.append({
        'line_item': line_item,
        'current_q': current_q,
        'last_q': last_q,
    })

(pd.DataFrame(lines_clean)
    .to_csv('berkshire10q.csv', index=False, encoding='cp1252')
)


