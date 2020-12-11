# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:52:56 2019

@author: brendan.fitzpatrick
"""

import os
import sys
from selenium import webdriver
import pandas as pd
import re
import time
import datetime as dt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def main(argv):
    fname = argv[1]
    executable_path = r'%s\Documents\chromedriver.exe' % os.path.expanduser('~')
    browser = webdriver.Chrome(executable_path=executable_path)
    dl_dir = r'%s\Downloads' % os.path.expanduser('~')
    df_cords = (pd.read_excel(fname)
                .drop_duplicates())
    coordinate_list = get_coordinate_list(df_cords)
    try:
        for coordinates in coordinate_list:
            latitude, longitude, radius = coordinates
            url = r'http://mcdc.missouri.edu/applications/capsACS.html'
            browser.get(url)
            (browser.find_element_by_xpath('//*[@id="latitude"]')
             .send_keys(str(latitude)))
            time.sleep(1)
            (browser.find_element_by_xpath('//*[@id="longitude"]')
             .send_keys(str(longitude)))
            time.sleep(1)
            (browser.find_element_by_xpath('//*[@id="radii"]')
             .send_keys(str(radius)))
            time.sleep(1)
            (browser.find_element_by_xpath('//*[@id="body"]/div/form/div/input[1]')
             .click())
            time.sleep(5)
            (browser.find_element_by_xpath('//*[@id="body"]/p[1]/a')
             .click())
            time.sleep(10)
    finally:
        csv_pat = re.compile(r'^capsACS.*\.csv$')
        files = [dl_dir + r'\%s' % x for x in os.listdir(dl_dir) if csv_pat.match(x)]
        df_scrape = (pd.concat([pd.read_csv(x) for x in files])
                     .pipe(split_cords)
                     .rename(columns={'radius': 'Radius'})
                     .set_index(['Longitude', 'Latitude', 'Radius']))       
        #df = (df_cords.set_index(['Longitude', 'Latitude', 'Radius'])
        #      .join(df_cords.unstack('Radius'), how='left'))
        timestamp = dt.datetime.now().isoformat()[0:-7].replace(':', '.')
        out_fname = dl_dir + r'\CAPS Data_%s.xlsx' % timestamp
        df_scrape.to_excel(out_fname, merge_cells=False)
        for file in files:
            os.remove(file)
        print('See file located at {:s}'.format(out_fname))

def get_coordinate_list(df):
    return (df.loc[:, ['Latitude', 'Longitude', 'Radius']]
            .values
            .tolist())
    
def split_cords(input_df):
    df = input_df.copy()
    col_dict = {0: 'Longitude',
                1: 'Latitude'}
    df[['Longitude', 'Latitude']] = (df.sitename.str.replace('(', '')
                                     .str.replace(')', '')
                                     .str.strip()
                                     .str.split(', ', expand=True)
                                     .rename(columns=col_dict)
                                     .astype('float64'))
    return df

if __name__ == '__main__':
    main(sys.argv)