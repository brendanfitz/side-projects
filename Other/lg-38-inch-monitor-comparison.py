# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

MONITOR_URIS = {
    '38GL950G-B': '/lg-38GL950G-B-gaming-monitor',
    '38WN95C-W': '/lg-38wn95c-w-ultrawide-monitor',
    '38WP85C-W': '/lg-38wp85c-w-ultrawide-monitor',
    '38UC99-W': '/lg-38UC99-W-ultrawide-monitor',
    '38WK95C-W': '/lg-38WK95C-W-ultrawide-monitor',
    '38WN75C-B': '/lg-38wn75c-b-ultrawide-monitor',
}


class MonitorScraper:
    COLUMN_NAMES = ('monitor_name', 'section', 'spec_name', 'spec_value')
    BASE = 'https://www.lg.com/us/monitors'
    
    def __init__(self, monitor_uris):
        self.monitor_uris = monitor_uris
        
    def scrape(self, clean=True):
        frames = [self._scrape_monitor_specs(name, uri)
                  for name, uri in self.monitor_uris.items()]
        self.df = pd.concat(frames)
        
        if clean:
            self.clean() 
            
        return self.df

    def _scrape_monitor_specs(self, name, uri):
        url = self.BASE + uri
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        data = list()
        divs = soup.find_all('div', class_='tech-spacs')
        for div in divs:
            h2 = div.find('h2', class_='tech-spacs-title')
            section = h2.text.title()
            for ul in div.find_all('ul', class_='dl_box'):
                lis = ul.find_all('li')
                assert len(lis) == 2
                k, v = (li.text.strip() for li in lis)
                data.append((name, section, k, v))
    
    
        price = soup.find('div', class_='price ga-price').text
        # price = float(price.replace('$', '').replace(',', ''))
        data.append((name, 'Price', 'Price', price))
        data.append((name, 'URL', 'URL', url))
    
        df = pd.DataFrame(data, columns=self.COLUMN_NAMES)
        
        return df
    
    def clean(self):
        self.df.spec_name = (self.df.spec_name
                             .str.replace('™', '')
                             .str.replace('Display Port', 'DisplayPort')
                            )
        self.df.section = (self.df.section
                           .str.replace('Inputs/Outputs', 'Input/Output')
                           .str.replace('Warranty/Upc', 'Warranty')
                           .str.replace('Warranty/Upc', 'Warranty')
                           .str.replace('Panel Specifications', 'Picture Quality')
                          )
        

def main():
    df = MonitorScraper(MONITOR_URIS).scrape()
    
    pivot_kwargs = dict(index=['section', 'spec_name',],
                        columns='monitor_name',
                        values='spec_value',)
    df_pivot = df.pivot(**pivot_kwargs).sort_index()
    
    columns_price_orders = (df_pivot.loc[slice('Price', 'Price'), ]
                            .T
                            .Price.Price
                            .map(lambda price: float(price.replace('$', '').replace(',', '')))
                            .sort_values()
                            .index.tolist()
                            )
    
    df_pivot = df_pivot.loc[:, columns_price_orders]
    
    df_pivot_price = df_pivot.xs('Price', axis=0)
    df_pivot_url = df_pivot.xs('URL', axis=0)
    with pd.ExcelWriter('LG 38 Inch Monitor Specs.xlsx') as writer:
        sections = df_pivot.index.get_level_values('section').unique().tolist()
        for section in sections:
            if section in ('Price', 'URL'):
                continue
            
            df_pivot_section = pd.concat((df_pivot_price, 
                                          df_pivot_url,
                                          df_pivot.xs(section, axis=0)))
            df_pivot_section.to_excel(writer, sheet_name=section.replace('/', '-'))
            
            
if __name__ == '__main__':
    main()
