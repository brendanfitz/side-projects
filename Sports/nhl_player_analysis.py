# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 11:56:22 2020

@author: Brendan Non-Admin
"""

import os
import pandas as pd

filename = os.path.join('data', 'nhl_player_data_1917-2020.csv')
data = pd.read_csv(filename)


def pre_proc(input_df):
    df = input_df.copy()
    
    df = df.sort_values(['skaterFullName', 'seasonId'])
    
    df.loc[:, 'year_season_start'] = df.seasonId.astype(str).str[:4].astype('int64')
    df.loc[:, 'year_season_end'] = df.seasonId.astype(str).str[4:].astype('int64')
    
    df.loc[:, 'season_number'] = (df
        .sort_values(['skaterFullName', 'seasonId'])
        .groupby(['skaterFullName'])
        ['year_season_start'].rank(method="first")
    )
    
    df.loc[:, 'years_played'] = (df.groupby('skaterFullName')
        ['season_number'].transform('max')
    )
    
    df = df.sort_values(['skaterFullName', 'season_number'])
    return df

data = data.pipe(pre_proc)

player_name = 'Jaromir Jagr'
mask = data.skaterFullName == player_name
data.loc[mask, 'playerId'].unique()

data = df

player_name = 'Mark Messier'
mask = data.skaterFullName == player_name
dim_cols = [
    'year_season_start',
    'teamAbbrevs',
    'positionCode',
    'gamesPlayed',
    'goals', 
    'assists',
    'faceoffWinPct', 
    'gameWinningGoals',
    'otGoals',
    'penaltyMinutes',
    'plusMinus',
    'points',
    'ppGoals',
    'ppPoints',
    'shGoals',
    'shPoints', 
    'shootingPct',
    'shots',
    'timeOnIcePerGame',
]
df = data.loc[mask, columns]

df_yearly_avgs = (data
    .groupby('year_season_start')
    .agg(
        average_goals=pd.NamedAgg(column='goals', aggfunc='mean'),
        average_assists=pd.NamedAgg(column='assists', aggfunc='mean'),
   )
)

def calc_goals_and_assists_by_year(input_df, to_dict=False):
    df = input_df.copy()
    
    df = (df.set_index('year_season_start')
     .loc[:, ['goals', 'assists']]
     .join(df_yearly_avgs)
    )
    
    if to_dict:
        df = df.reset_index().to_dict(orient='records')
    
    return df

goals_and_assists_by_year = df.pipe(calc_goals_and_assists_by_year, True)

def calc_games_by_team(input_df, to_dict=False):
    df = input_df.copy()
    df = df.groupby('teamAbbrevs').gamesPlayed.sum()
    
    if to_dict:
        df = df.to_dict()
        
    return df

games_by_team = df.pipe(calc_games_by_team, True)

def calc_all_time_rankings(input_df, to_dict=False):
    pass

all_time_rankings = df.pipe(calc_all_time_rankings, True)

def create_photo_url(player_name):
    mask = data.skaterFullName == player_name
    player_id = data.loc[mask, 'playerId'].unique()[0]
    
    url_str = 'https://nhl.bamcontent.com/images/headshots/current/168x168/{}.jpg'
    
    return url_str.format(player_id)

photo_url = create_photo_url(player_name)


import json

player_data = {
    'player_info': {
            'player_name': player_name,
            'teams': games_by_team.index.tolist(),
            'years_played': df.shape[0],
            'rookie_year': df.year_season_start.min(),
            'retirement_year': df.year_season_start.max() + 1,
            'photo_url': photo_url,
        },
    'all_time_rankings': all_time_rankings,
    'goals_and_assists_by_year': goals_and_assists_by_year,
    'games_by_team': games_by_team,
}

json.dumps(player_data)