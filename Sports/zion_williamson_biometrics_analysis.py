# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 10:16:20 2020

@author: Brendan Non-Admin

source_url: https://stats.nba.com/players/bio/?Season=2019-20&SeasonType=Regular%20Season

background: I downloaded html file to use since testing the API directly didn't work

"""

import re
from os import path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import scipy.stats.stats
plt.style.use('ggplot')

filename = 'NBA.com_Stats _ Players Bios.html'
filepath = path.join('data', filename)

with open(filepath, 'r') as f:
    df = (pd.read_html(f)[0]
        .set_index('Player')
    )
    
# sanity check for players per team (should be around 15)
len(df) / 30

##############################################################################
# check all heights match pattern
##############################################################################
pat = re.compile(r'\d-\d{1,2}')

mask = ~df.Height.str.match(pat)
assert(df.loc[mask, 'Height'].empty)

df.loc[:, 'Height (Inches)'] = (df.Height
    .str.split('-')
    .apply(lambda x: int(x[0]) * 12 + int(x[1]))
)

ax = df.plot.scatter(x='Height (Inches)', y='Weight')
ax.set(title='NBA Player BioMetrics')
plt.show()

##############################################################################
# z-score
##############################################################################
columns = ['Height (Inches)', 'Weight']
X = df.loc[:, columns]

mu = np.mean(X)
std = np.cov(X.T)

zscore = 2 * (1 - stats.multivariate_normal.cdf(X, mean=mu, cov=np.diag(std)))

##############################################################################
# Quartile deviation - interquartile range (1.5 * IQR)
##############################################################################


##############################################################################
# scaling
##############################################################################
from sklearn.preprocessing import StandardScaler

height_scaler = StandardScaler()
x = df.loc[:, ['Height (Inches)']]
df.loc[:, 'height_scaled'] = height_scaler.fit_transform(x)

weight_weight = StandardScaler()
x = df.loc[:, ['Weight']]
df.loc[:, 'weight_scaled'] = height_scaler.fit_transform(x)

df.plot.scatter(x='height_scaled', y='weight_scaled')

##############################################################################
# dbscan
##############################################################################
from sklearn.cluster import DBSCAN

X = df.loc[:, ['height_scaled', 'weight_scaled']]

db = DBSCAN().fit(X)

df.loc[:, 'DBSCAN Results'] = (pd.Categorical(db.labels_)
    .rename_categories({-1: 'Outlier', 0: 'Core Data'})
)

mask = df.loc[:, 'DBSCAN Results'] == 'Outlier'
df.loc[mask, ['Height', 'Weight']]

plot_kwargs = dict(
    x='Height (Inches)', y='Weight', hue='DBSCAN Results', data=df,
    palette=sns.color_palette("RdBu", n_colors=2)[::-1]
)
ax = sns.scatterplot(**plot_kwargs)
ax.set(title='NBA Player BioMetrics')
plt.show()

##############################################################################
# Isolation Forests
##############################################################################
from sklearn.ensemble import IsolationForest

X = df.loc[:, ['height_scaled', 'weight_scaled']]

clf = IsolationForest(contamination=0.01).fit(X)

df.loc[:, 'IsolationForest Results'] = (pd.Categorical(clf.predict(X))
    .rename_categories({-1: 'Outlier', 1: 'Core Data'})
)

mask = df.loc[:, 'IsolationForest Results'] == 'Outlier'
df.loc[mask, ['Height', 'Weight']]

mask = df.loc[:, 'IsolationForest Results'] == 'Outlier'
df.loc[mask, ['Height', 'Weight']]

plot_kwargs = dict(
    x='Height (Inches)', y='Weight', hue='IsolationForest Results', data=df,
    palette=sns.color_palette("RdBu", n_colors=2)[::-1]
)
ax = sns.scatterplot(**plot_kwargs)
ax.set(title='NBA Player BioMetrics')
plt.show()
