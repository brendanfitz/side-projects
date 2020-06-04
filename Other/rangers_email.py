# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 20:17:11 2020

@author: Brendan Non-Admin
"""

import argparse
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_config import sender_email, sender_email_password, receiver_email
from jinja2 import Template
import pandas as pd
import datetime as dt

_rangers = 'New York Rangers'

def scrape_rangers_schedule_df():
    url = 'https://www.hockey-reference.com/teams/NYR/2020_games.html'
    df = pd.read_html(url)[0]

    """ filter out rows that are column header rows within the table """
    mask = df.loc[:, 'GP'] != 'GP'
    df = (df.loc[mask, ]
        .assign(Date=lambda x: pd.to_datetime(x.Date))
        .rename(columns={'Unnamed: 3': 'Home/Away'})
    )
    assert(df.shape[0] == 82)

    return df

def filter_game_data(df, testing=False):
    date_val = dt.datetime(2020, 4, 2) if testing else dt.datetime.today()

    dt_mask = df.Date == date_val
    df_date_filtered = df.loc[dt_mask, ]

    if not df_date_filtered.empty:
        game_data = df_date_filtered.to_dict(orient='record')[0]
        return game_data

def scrape_team_data(opponent):
    url = 'https://www.hockey-reference.com/leagues/NHL_2020_standings.html#all_standings'
    df = (pd.read_html(url, attrs = {'id': 'standings'})[0]
        .rename(columns={'Unnamed: 1': 'Team'})
        .loc[:, ['Team', 'Overall']]
        .set_index('Team')
    )
    teams = [_rangers, opponent]
    team_records = (df.loc[teams, ]
        .to_dict()
        ['Overall']
    )

    return team_records

def main(argv):
    args = argv[1]
    testing = args.testing

    port = 465
    smtp_server = "smtp.gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Rangers Game Tonight!"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text_template_str = open('rangers_email.txt').read()
    text_template = Template(text_template_str)
    html_template_str = open('rangers_email.html').read()
    html_template = Template(html_template_str)

    df = scrape_rangers_schedule_df()

    game_data = filter_game_data(df, testing=testing)
    if game_data is None:
        return
    opponent = game_data['Opponent']

    team_records = scrape_team_data(opponent)

    template_kwargs = dict(
        opponent=opponent,
        time=game_data['Time'],
        rangers_record=team_records[_rangers],
        opponent_record=team_records[opponent],
    )
    text = text_template.render(**template_kwargs)
    html = html_template.render(**template_kwargs)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_email_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

if __name__ == '__main__':
    description = 'Send email informing whether there is a Rangers game today'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--testing", action="store_true",
        help="run in testing mode (Penguins game on 2020-04-02)"
    )
    args = parser.parse_args()
    argv = [__name__, args]
    main(argv)
