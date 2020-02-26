#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 15:23:27 2020

@author: BFitzpatrick
"""

import os
import numpy as np
import pandas as pd
import requests
import datetime as dt
from bs4 import BeautifulSoup

def main():
    url = 'https://www.hockey-reference.com/leagues/NHL_2020_games.html'
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = str(soup.find('table', {'id': 'games'}))
    df = pd.read_html(table)[0]
     
    colmap = {
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
    df = (df.rename(columns=colmap)
        .pipe(filter_unplayed_games)
        .set_index('date', append=True)
        .rename_axis(["game_id", "date"])
        .assign(home_win=lambda x: (x.home_goals > x.away_goals),
                away_win=lambda x: (x.home_goals < x.away_goals))
    )
        
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
    )
    df_teams['team_game_id'] = df_teams.groupby('team').cumcount() + 1
    df_teams['total_points'] = df_teams.groupby('team')['points'].cumsum()
    
    ds= dt.datetime.today().strftime('%y%m%d')
    fout = os.path.join(
        'data',
        f"nhl_results_{ds}.csv",
    )
    df_teams.to_csv(fout)
    print(f"NHL Point Data Scrape Successful!\nSee file located at {fout}")

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

if __name__ == '__main__':
    main()
