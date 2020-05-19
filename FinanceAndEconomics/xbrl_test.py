# -*- coding: utf-8 -*-
"""
Created on Mon May  4 17:11:06 2020

@author: Brendan Non-Admin
"""

from bs4 import BeautifulSoup
import requests
import sys

# Access page
cik = '0000051143'
type = '10-K'
dateb = '20160101'

# Obtain HTML for search page
base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&dateb={}"
edgar_resp = requests.get(base_url.format(cik, type, dateb))
edgar_str = edgar_resp.text

# Find the document link
doc_link = ''
soup = BeautifulSoup(edgar_str, 'html.parser')
table_tag = soup.find('table', class_='tableFile2')
rows = table_tag.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 3:
        if '2015' in cells[3].text:
            doc_link = 'https://www.sec.gov' + cells[1].a['href']
            
            
# Obtain HTML for document page
doc_resp = requests.get(doc_link)
doc_str = doc_resp.text

# Find the XBRL link
xbrl_link = ''
soup = BeautifulSoup(doc_str, 'html.parser')
table_tag = soup.find('table', class_='tableFile', summary='Data Files')
rows = table_tag.find_all('tr') 
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 3:
        if 'INS' in cells[3].text:
            xbrl_link = 'https://www.sec.gov' + cells[2].a['href']
            
 
# Obtain XBRL text from document
xbrl_resp = requests.get(xbrl_link)
xbrl_str = xbrl_resp.text            
'{:,.0f}'.format(len(xbrl_str))

# Find and print stockholder's equity

import xml.etree.ElementTree as ET

root = ET.fromstring(xbrl_str)

root.tag

for child in root:
     print(child.tag, child.attrib)

child = root[6]
child.tag, child.attrib, child.text


soup = BeautifulSoup(xbrl_str, 'lxml')
tag_list = soup.find_all()
for tag in tag_list:
    if tag.name == 'us-gaap:stockholdersequity':
        print("Stockholder's equity: " + tag.text)

soup.prettify()