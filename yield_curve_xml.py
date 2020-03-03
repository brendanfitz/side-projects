#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse as p
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = ("https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData"
"?$filter=month(NEW_DATE)%20eq%203%20and%20year(NEW_DATE)%20eq%202020")
print(p.unquote(url))

response = requests.get(url)
xml = response.content
root = ET.fromstring(xml)

ns = {'ns': 'http://www.w3.org/2005/Atom',
      'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata', 
      'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices'}

data = list()
for entry in root.findall('ns:entry', ns):
    content = (entry.find('ns:content', ns)
     .find('m:properties', ns)
    )
    row = dict()
    for child in content:
        row[child.tag.replace('{' + ns['d'] + '}', '')] = child.text
    data.append(row)

colord = [
    'BC_1MONTH', 'BC_2MONTH', 'BC_3MONTH', 'BC_6MONTH', 'BC_1YEAR', 'BC_2YEAR', 
    'BC_3YEAR', 'BC_5YEAR', 'BC_7YEAR', 'BC_10YEAR', 'BC_20YEAR', 'BC_30YEAR', 
]
df = (pd.DataFrame.from_records(data)
 .rename(columns={'NEW_DATE': 'new_date'})
 .assign(new_date=lambda x: pd.to_datetime(x['new_date']))
 .set_index('new_date')
 .drop(['Id', 'BC_30YEARDISPLAY'], axis=1)
 .loc[:, colord]
 .apply(pd.to_numeric, axis=1)
)

d = df.loc['20200302', ].T.reset_index()
d.columns = ['x', 'y']
ax = sns.lineplot(x=d.index, y=d.y, data=d)
ax.set_xticks([x for x in d.index])
ax.set_xticklabels(d.x)
plt.xticks(rotation=-40, ha='left')
plt.show()
