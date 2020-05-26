# -*- coding: utf-8 -*-
"""
Created on Thu May 21 12:55:12 2020

@author: Brendan Non-Admin
"""

import os
import math
import pandas as pd

filename = os.path.join('data', 'nhl_player_data_2000-2020.csv')
df = pd.read_csv(filename)

df.columns
subsetcols = ['skaterFullName', 'seasonId', 'goals', 'gamesPlayed', 'positionCode']
df = (df.loc[:, subsetcols]
 .sort_values(['skaterFullName', 'seasonId'])
)

df.loc[:, 'year_season_start'] = df.seasonId.astype(str).str[:4].astype('int64')
df.loc[:, 'year_season_end'] = df.seasonId.astype(str).str[4:].astype('int64')

df.loc[:, 'season_number'] = (df.groupby(['skaterFullName'])
    ['year_season_start'].rank()
)

df.loc[:, 'years_played'] = (df.groupby('skaterFullName')
    ['season_number'].transform('max')
)
df = df.sort_values(['skaterFullName', 'season_number'])

#import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("whitegrid")

x = df.loc[:, ['skaterFullName', 'years_played']].drop_duplicates().years_played
sns.distplot(x)

data = df.groupby('season_number', as_index=False)['goals'].sum()
sns.lineplot('season_number', 'goals', data=data)

df.groupby('positionCode').goals.mean()

def goals_per_player_by_season(input_df):
    """
    Parameters
    ----------
    input_df : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.
    
    Updates Required
    ----------
    Need to divide each year by numbers of players

    """
    df = input_df.copy()
    df = df.groupby('season_number')['goals'].mean().reset_index(name='goals_per_player')
    return df

df.groupby('year_season_start')['goals'].mean()

def plot_goals_per_player_by_season(df, years_played, ax=None):
    label = "All Players" if years_played is None else "{} Years+".format(years_played)
    if years_played:
        mask = df.loc[:, 'years_played'] >= years_played
        df = df.loc[mask, :]
    data = df.pipe(goals_per_player_by_season)
    if ax:
        return sns.lineplot('season_number', 'goals_per_player', label=label, data=data, ax=ax)
    return sns.lineplot('season_number', 'goals_per_player', label=label, data=data)
        
""" Run all at once for same plot """
import numpy as np

ax = plot_goals_per_player_by_season(df, None)
ax = plot_goals_per_player_by_season(df, 3)
ax = plot_goals_per_player_by_season(df, 5)
ax = plot_goals_per_player_by_season(df, 7)
ax = plot_goals_per_player_by_season(df, 9)
plt.xticks(np.arange(1, df.years_played.max(), step=1))
plt.legend()
plt.show()

import statsmodels.formula.api as smf

additional_cols = ['season_number', 'gamesPlayed', 'positionCode']

def create_df(n, additional_cols):
    """
    Using this to avoid excessive dropping of na's
    """
    frames = [df.groupby('skaterFullName').goals.shift(i) for i in range(n)]
    keys = ['y'] + ['L%s' % i for i in range(1, n)]
    X = (pd.concat(frames, axis=1, keys=keys)
        .dropna()
    )
    
    X = X.join(df.loc[:, additional_cols])
    return X

mask = df.loc[:, 'years_played'] >= 5
df = df.loc[mask, :]

X = create_df(6, additional_cols)

model = smf.ols('y ~ L1 + L2 + L3 + L4 + L5', data=X)
results = model.fit()
results.summary()

X = create_df(4, additional_cols)

mod = smf.ols('y ~ L1 + L2 + L3', data=X)
results = mod.fit()
results.summary()

mod = smf.ols('y ~ L1 + L2 + L3 + season_number', data=X)
results = mod.fit()
results.summary()

mod = smf.ols('y ~ L1 + L2 + L3 + season_number + gamesPlayed', data=X)
results = mod.fit()
results.summary()

X.loc[:, 'season_number_squared'] = X.season_number.pow(2)
formula = ('y ~ L1 + L2 + L3 + season_number + season_number_squared + '
           'gamesPlayed')
mod = smf.ols(formula, data=X)
results = mod.fit()
results.summary()
X.drop('season_number_squared', axis=1)

X = create_df(6, additional_cols)

l5_str = 'L1 + L2 + L3 + L4 + L5'
formula = 'y ~ {} + season_number + gamesPlayed'.format(l5_str)
mod = smf.ols(formula, data=X)
results = mod.fit()
results.summary()

formula = ('y ~ {} + season_number + gamesPlayed + C(positionCode)'
           .format(l5_str))
mod = smf.ols(formula, data=X)
results = mod.fit()
results.summary()

position_code_map = {'D': 'D', 'C': 'F', 'R': 'F', 'L': 'F'}
X.loc[:, 'positionCode'] = X.loc[:, 'positionCode'].map(position_code_map)

formula = ('y ~ {} + season_number + gamesPlayed + C(positionCode)'
           .format(l5_str))
mod = smf.ols(formula, data=X)
results = mod.fit()
results.summary()

print("Root MSE (Total): {:0.2f}".format(math.sqrt(results.mse_total)))

y_pred = results.predict(X).rename('predicted_goals')

cols = [
    "skaterFullName",
    "season_number", 
    "year_season_start", 
    "year_season_end", 
    "gamesPlayed", 
    "years_played", 
    "positionCode", 
    "L1", 
    "L2", 
    "L3", 
    "L4", 
    "L5", 
    "goals", 
    "predicted_goals",
    "mae",
]
filename = os.path.join('data', 'nhl_player_goal_predictions.xlsx')
(df.join(y_pred)
    .join(X.drop(['y'] + additional_cols, axis=1))
    .loc[:, cols]
    .assign(mae=lambda x: (x.goals - x.predicted_goals).abs())
    .to_excel(filename, index=False)
)