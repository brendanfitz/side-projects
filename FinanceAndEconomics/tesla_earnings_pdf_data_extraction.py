# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 09:54:19 2020

@author: Brendan Non-Admin
"""
from PyPDF2 import PdfFileReader
import re
from collections import defaultdict
import pandas as pd
import numpy as np


#############################################################################
# Extract text and output to file
##############################################################################    
path = 'Q2\'20 Update.pdf'
with open(path, 'rb') as f:
    pdf = PdfFileReader(f)
    
    income_statement_text = pdf.getPage(20).extractText()
    balance_sheet_text = pdf.getPage(21).extractText()
    cash_flow_text = pdf.getPage(22).extractText()
    
income_statement_filename = 'tesla_income_statement_text.txt'
with open(income_statement_filename , 'w') as f:
    f.write(income_statement_text)
    
#############################################################################
# Make adjustments in text editor to file and re-read
##############################################################################
with open(income_statement_filename , 'r') as f:
    income_statement_text = f.read()
lines = income_statement_text.split('\n')[:-4] # -4 since the header is at the bottom

##############################################################################
# set loop parameters and iterate
##############################################################################
income_statement_sections = [
    'REVENUES',
    'COST OF REVENUES',
    'OPERATING EXPENSES',
]
income_statement_data = {}

pat = re.compile(r'\d')
current_section = None
i = 0
while i < len(lines):
    line = lines[i]
    line_item = line.replace('\n', '')
    
    if line_item in income_statement_sections:
        current_section = line_item
        income_statement_data[line_item] = [np.nan] * 5
        i = i + 1
    elif i + 1 < len(lines) and not pat.search(lines[i] + lines[i+1]):
        i = i + 1
        income_statement_data[line_item] = [np.nan] * 5
    elif current_section:
        income_statement_data[line_item] = lines[i+1:i+6]
        i = i + 6
    else:
        i = i + 1
        income_statement_data[line_item] = [np.nan] * 5
                    
##############################################################################
# convert to dataframe and output to csv
##############################################################################
index = ['Q2-2019', 'Q3-2019', 'Q4-2019', 'Q1-2020', 'Q2-2020']
df = (pd.DataFrame(income_statement_data, index=index)
    .T
)

df.to_csv('tesla_income_statement.csv')