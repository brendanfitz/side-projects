#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 15:23:27 2020

@author: BFitzpatrick
"""

import os
import json
import numpy as np
import pandas as pd
import requests
import datetime as dt
from bs4 import BeautifulSoup

def main():
    data = scrape_nhl_data()
     
    colmap = create_colmap()
    df = (data.rename(columns=colmap)
        .pipe(filter_unplayed_games)
        .set_index('date', append=True)
        .rename_axis(["game_id", "date"])
        .assign(home_win=lambda x: (x.home_goals > x.away_goals),
                away_win=lambda x: (x.home_goals < x.away_goals))
    )
        
    df_teams = create_df_teams(df)
    
    ds = dt.datetime.today().strftime('%y%m%d')
    teams_fout = os.path.join('data', f"nhl_results_{ds}.csv")
    df_teams.to_csv(teams_fout)
    
    df_team_games = create_df_team_games(df_teams)
    
    results = create_results(df_team_games)

    team_games_fout = os.path.join('data', f"nhl_results_by_game_{ds}.json")
    with open(team_games_fout, 'w') as fout:
        json.dump(results , fout, indent=4)
        
    print("NHL Point Data Scrape Successful!"
          f"\nSee files located at {teams_fout} & {team_games_fout}")


def scrape_nhl_data():
    url = 'https://www.hockey-reference.com/leagues/NHL_2020_games.html'
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = str(soup.find('table', {'id': 'games'}))
    df = pd.read_html(table)[0]
    return df

def create_colmap():
    return {
        'Date': 'date',
        'Visitor': 'away_team',
        'G': 'away_goals',
        'Home': 'home_team',
        'G.1': 'home_goals',
        'Unnamed: 5': 'extra_time',
        'Att.': 'attendance',
        'LOG': 'game_length',
        'Notes': 'notes',
    }

def points_calc(win, extra_time):
    extra_time_loss = ~win & ~extra_time.isnull()
    loss_points = np.where(extra_time_loss, 1, 0)
    points = np.where(win, 2, loss_points)
    return points

def filter_unplayed_games(input_df):
    df = input_df.copy()
    today = dt.date.today().isoformat()
    mask = df.date < today
    return df.loc[mask, ]

def create_df_teams(df):
    home_cols = ['home_team', 'home_win', 'extra_time']
    away_cols = ['away_team', 'away_win', 'extra_time']
    
    frames = list()
    for cols in [home_cols, away_cols]:
        df_team = (df.loc[:, cols]
            .rename(columns={
                'home_team': 'team',
                'away_team': 'team',
                'home_win': 'win',
                'away_win': 'win',
            })
            .set_index('team', append=True)
        )
        frames.append(df_team)
    
    df_teams = (pd.concat(frames)
        .assign(points=lambda x: points_calc(x.win, x.extra_time))
        .assign(team_game_id=lambda x: x.groupby('team').cumcount() + 1,
                total_points=lambda x: x.groupby('team')['points'].cumsum())
    )
    return df_teams

def create_df_team_games(df_teams):
    df_team_games = (df_teams.reset_index()
        .set_index(['team_game_id', 'team'])
        .loc[:, 'total_points']
        .rename(columns={'total_points': 'points'})
        .unstack('team')
    )
    return df_team_games

def create_results(df_team_games):
    results = list()
    for i, row in df_team_games.iterrows():
        df_temp = pd.DataFrame(row).reset_index()
        df_temp.columns = ['team', 'points']
        team_points = df_temp.to_dict(orient='records')
        [(lambda d: d.update({'game_number': i}) or d)(x) for x in team_points]
        entry = {
            'game_number': i,
            'teams': team_points,
        }
        results.append(entry)
    return results

if __name__ == '__main__':
    main()
