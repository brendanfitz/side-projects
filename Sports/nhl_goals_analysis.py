# -*- coding: utf-8 -*-
"""
Created on Thu May 21 12:55:12 2020

@author: Brendan Non-Admin
"""

import os
import numpy as np
import math
import pandas as pd

filename = os.path.join('data', 'nhl_player_data_1990-2020.csv')
df = pd.read_csv(filename)


subsetcols = [
    'skaterFullName', 'seasonId', 'goals', 'gamesPlayed', 'positionCode', 
    'penaltyMinutes', 'plusMinus', 'shootingPct', 'shots'
]
df = (df.loc[:, subsetcols]
 .sort_values(['skaterFullName', 'seasonId'])
)

df.loc[:, 'year_season_start'] = df.seasonId.astype(str).str[:4].astype('int64')
df.loc[:, 'year_season_end'] = df.seasonId.astype(str).str[4:].astype('int64')

df.loc[:, 'season_number'] = (df.sort_values(['skaterFullName', 'seasonId'])
    .groupby(['skaterFullName'])
    ['year_season_start'].rank(method="first")
)

df.loc[:, 'years_played'] = (df.groupby('skaterFullName')
    ['season_number'].transform('max')
)

df = df.sort_values(['skaterFullName', 'season_number'])

import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("whitegrid")

x = (df.loc[:, ['skaterFullName', 'years_played']]
     .drop_duplicates()
     .years_played
    )
sns.distplot(x)

data = df.groupby('season_number', as_index=False)['goals'].sum()
sns.lineplot('season_number', 'goals', data=data)

df.groupby('positionCode').goals.mean()

def goals_per_player_by_season(input_df):
    """
    Parameters
    ----------
    input_df : dataframe with goals and season_number columns

    Returns
    -------
    df : dataframe grouped by goals and season number
    """
    df = input_df.copy()
    df = (df.groupby('season_number')['goals'].mean()
          .reset_index(name='goals_per_player')
         )
    return df

df.groupby('year_season_start')['goals'].mean()

def plot_goals_per_player_by_season(df, years_played, ax=None):
    label = "All Players" if years_played is None else "{} Years".format(years_played)
    if years_played:
        mask = df.loc[:, 'years_played'] == years_played
        df = df.loc[mask, :]
    data = df.pipe(goals_per_player_by_season)
    if ax:
        return sns.lineplot('season_number', 'goals_per_player', label=label, data=data, ax=ax)
    return sns.lineplot('season_number', 'goals_per_player', label=label, data=data)
        
""" Run all at once for same plot """
ax = plot_goals_per_player_by_season(df, None)
for i in range(15):
    ax = plot_goals_per_player_by_season(df, i)
plt.xticks(np.arange(1, df.years_played.max(), step=1))
plt.legend()
plt.show()


df.season_number.value_counts()
sns.countplot(df.season_number)

ovi = df.loc[df.skaterFullName == 'Alex Ovechkin', ]
ax = plot_goals_per_player_by_season(ovi, None)
plt.xticks(np.arange(1, df.years_played.max(), step=1))
plt.legend()
plt.show()

import statsmodels.formula.api as smf

additional_cols = ['season_number', 'gamesPlayed', 'positionCode']

def create_lags(input_df, metric, n=5, include_metric_name_in_columns=False):
    df = input_df.copy()
    frames = [df.groupby('skaterFullName')[metric].shift(i) for i in range(n+1)]
    if include_metric_name_in_columns:
        keys = [metric] + [metric + '_L%s' % i for i in range(1, n+1)]
    else:
        keys = ['y'] + ['L%s' % i for i in range(1, n+1)]
    df = (pd.concat(frames, axis=1, keys=keys)
        .dropna()
    )
    return df

def create_X(n, additional_cols):
    """
    Using this to avoid excessive dropping of na's
    """
    X = create_lags(df, 'goals', n)
    
    X = X.join(df.loc[:, additional_cols])
    return X

mask = df.loc[:, 'years_played'] >= 5
df = df.loc[mask, :]

X = create_X(5, additional_cols)

model = smf.ols('y ~ L1 + L2 + L3 + L4 + L5', data=X)
results = model.fit()
results.summary()

X = create_X(3, additional_cols)    

mod = smf.ols('y ~ L1 + L2 + L3', data=X)
results = mod.fit()
results.summary()

mod = smf.ols('y ~ L1 + L2 + L3 + season_number', data=X)
results = mod.fit()
results.summary()

mod = smf.ols('y ~ L1 + L2 + L3 + season_number + gamesPlayed', data=X)
results = mod.fit()
results.summary()

X = create_X(5, additional_cols)

l5_str = 'L1 + L2 + L3 + L4 + L5'
formula = 'y ~ {} + season_number + gamesPlayed'.format(l5_str)
mod = smf.ols(formula, data=X)
results = mod.fit()
results.summary()

X.loc[:, 'season_number_squared'] = X.season_number.pow(2)
formula = ('y ~ {} + season_number + season_number_squared + '
           'gamesPlayed').format(l5_str)
mod = smf.ols(formula, data=X)
results = mod.fit()
results.summary()
X.drop('season_number_squared', axis=1) """ Ignore due to multi-collinearity """

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
filename = os.path.join('data', 'nhl_player_goal_predictions_1990-2019.xlsx')
(df.join(y_pred)
    .join(X.drop(['y'] + additional_cols, axis=1))
    .assign(mae=lambda x: (x.goals - x.predicted_goals).abs())
    .loc[:, cols]
    .to_excel(filename, index=False)
)

model_filename = os.path.join('data', 'nhl_goals_regression_model.pkl')
results.save(model_filename)

from statsmodels.regression.linear_model import OLSResults

nhl_goals_mod = OLSResults.load(model_filename)

row = pd.DataFrame({
        'L1': 17,
        'L2': 20,
        'L3': 18,
        'L4': 18,
        'L5': 18,
        'season_number': 1,
        'gamesPlayed': 50,
        'positionCode': 'D'
    }, index=[0]
)
results.predict(row)[0]

"""
Additional lag test
"""

lagged_metrics = ['penaltyMinutes', 'plusMinus', 'shootingPct', 'shots',]
lagged_dfs = [create_lags(df, x, 1, include_metric_name_in_columns=True).drop(x, axis=1) for x in lagged_metrics]

for x in lagged_dfs:
    df = df.join(x)
    
additional_cols = ['season_number', 'gamesPlayed', 'positionCode',
                   'penaltyMinutes_L1', 'plusMinus_L1', 'shootingPct_L1', 'shots_L1'
                   ]
X = create_X(5, additional_cols)
position_code_map = {'D': 'D', 'C': 'F', 'R': 'F', 'L': 'F'}
X.loc[:, 'positionCode'] = X.loc[:, 'positionCode'].map(position_code_map)

formula = ('y ~ {} + season_number + gamesPlayed + C(positionCode) + penaltyMinutes_L1 + plusMinus_L1 + shootingPct_L1 + shots_L1'
           .format(l5_str))
mod = smf.ols(formula, data=X)
results = mod.fit()
results.summary()