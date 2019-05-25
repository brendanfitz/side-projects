import pandas as pd
import fred_api as fred
import requests
import  xml.etree.ElementTree as et
import os
import io
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
%pylab
sns.set(style='whitegrid')

df = fred.series('PAYEMS', )

url = (r'https://api.stlouisfed.org/fred/series?'
       r'series_id=%s&'
       r'api_key=%s') % ('PAYEMS', fred.fred_api_key)

response = requests.get(url)

f = io.StringIO(response.text)
tree = et.parse(f)
root = tree.getroot()

os.makedirs('Data')

tree.write(r'Data/payems.xml')
for child in root:
    print(child.tag)
root.find('series').attrib['notes']

url = 'https://api.stlouisfed.org/fred/tags/series'
params = {'api_key':fred.fred_api_key, 'tag_names':'income',
          'file_type':'json'}
response = requests.get(url, params=params)

df = (fred.series('MEHOINUSA672N', '1986-01-01', '2019-03-01')
      .assign(value=lambda x: x.value.astype('float64')))

@ticker.FuncFormatter
def y_formatter(value, pos):
    return '{:,.0f}'.format(value)

ax = (df.assign(date=lambda x: x.date.astype('datetime64'))
 .set_index('date')
 .pipe((sns.lineplot, 'data'), palette='tab10', linewidth=2.5,
       legend=False))
ax.yaxis.set_major_formatter(y_formatter)
ax.set(title="Median US Income", xlabel='')
plt.show()
