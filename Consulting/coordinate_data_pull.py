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

class CoordinateDemographicsDataLoader(object):

    executable_path = r'%s\Documents\chromedriver.exe' % os.path.expanduser('~')
    dl_dir = r'%s\Downloads' % os.path.expanduser('~')

    def __init__(self, filename):
        self.filename = filename
        self.browser = webdriver.Chrome(executable_path=self.executable_path)

    def fetch_coodinate_data(self):
        df_cords = (pd.read_excel(self.filename, engine="openpyxl")
                    .drop_duplicates())
    
        coordinate_list = self.get_coordinate_list(df_cords)
        try:
            for coordinates in coordinate_list:
                self.download_coordinate_file(coordinates)
        finally:
            self.compile_coordinate_files()
    
    def compile_coordinate_files(self):
        csv_pat = re.compile(r'^capsACS.*\.csv$')
        files = [self.dl_dir + r'\%s' % x for x in os.listdir(self.dl_dir) if csv_pat.match(x)]
        df_scrape = (pd.concat([pd.read_csv(x) for x in files])
            .pipe(self.split_cords)
            .rename(columns={'radius': 'Radius'})
            .set_index(['Longitude', 'Latitude', 'Radius'])
        )

        timestamp = dt.datetime.now().isoformat()[0:-7].replace(':', '.')
        out_fname = self.dl_dir + r'\CAPS Data_%s.xlsx' % timestamp
        df_scrape.to_excel(out_fname, merge_cells=False)

        for file in files:
            os.remove(file)
        print('See file located at {:s}'.format(out_fname))
    
    def download_coordinate_file(self, coordinates):
        latitude, longitude, radius = coordinates
        url = r'http://mcdc.missouri.edu/applications/capsACS.html'
        self.browser.get(url)
        (self.browser.find_element_by_xpath('//*[@id="latitude"]')
         .send_keys(str(latitude)))
        (self.browser.find_element_by_xpath('//*[@id="longitude"]')
         .send_keys(str(longitude)))
        (self.browser.find_element_by_xpath('//*[@id="radii"]')
         .send_keys(str(radius)))
    
        (self.browser.find_element_by_xpath('//*[@id="body"]/div/form/div/input[1]')
         .click())
        time.sleep(5)
    
        (self.browser.find_element_by_xpath('//*[@id="body"]/p[1]/a')
         .click())
        time.sleep(5)
    
    @staticmethod
    def get_coordinate_list(df):
        coordinates = (df.loc[:, ['Latitude', 'Longitude', 'Radius']]
            .values
            .tolist()
        )
        return coordinates
        
    @staticmethod
    def split_cords(input_df):
        df = input_df.copy()
    
        df[['Longitude', 'Latitude']] = (df.sitename
            .str.replace('(', '')
            .str.replace(')', '')
            .str.strip()
            .str.split(', ', expand=True)
            .rename(columns={0: 'Longitude', 1: 'Latitude'})
            .astype('float64')
        )
        return df

if __name__ == '__main__':
    filename = sys.argv[0]
    loader = CoordinateDemographicsDataLoader(filename)
    loader.fetch_coodinate_data()