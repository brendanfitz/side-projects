# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 21:54:48 2020

@author: Brendan Non-Admin
"""

import pandas as pd

html_kwargs = dict(
    classes="table",
    justify="left",
    border=0,
    index_names=False
)

fin = r'data\FuryWilderFightHistory.xlsx'
df = (pd.read_excel(fin)
      .loc[:, ['name', 'opponent_name', 'opponent_height',]]
      .drop_duplicates()
      .set_index(['name', 'opponent_name',])
     )
print(df.head()
      .to_html(**html_kwargs)
      .replace('class="dataframe ', 'class="')
     )


ft_inches_str = (df.opponent_height.str.split(' / ', expand=True)[0]
                 .rename('opponent_height_ft_and_inches')
                )
print(df.join(ft_inches_str)
 .head()
 .to_html(**html_kwargs)
 .replace('class="dataframe ', 'class="')
)

pat = r'\d+′ \d+\.?\d?″'
mask = ~ft_inches_str.str.match(pat, na=True)
print(df.join(ft_inches_str)
      .loc[mask, ]
      .head()
      .to_html(**html_kwargs)
      .replace('class="dataframe ', 'class="')
     )


ft_inches_str = (df.opponent_height.str.split(' / ', expand=True)[0]
                 .str.strip()
                 .str.replace('½', '.5')
                )
pat = r'\d+′ \d+\.?\d?″'
mask = ~ft_inches_str.str.match(pat, na=True)
print(df.join(ft_inches_str)
      .loc[mask, ]
      .head()
      .to_html(**html_kwargs)
      .replace('class="dataframe ', 'class="')
     )


pat = r'(?P<feet>\d+)′ (?P<inches>\d+\.?\d?)″'
ft_inch_columns = ft_inches_str.str.extract(pat).astype('float64')
print(df.join(ft_inch_columns)
      .head()
      .to_html(**html_kwargs)
      .replace('class="dataframe ', 'class="')
     )

height_in_inches = ((ft_inch_columns.feet * 12 + ft_inch_columns.inches)
                    .rename('opponent_height_in_inches')
                    )
print(df.join(height_in_inches)
      .head()
      .to_html(**html_kwargs)
      .replace('class="dataframe ', 'class="')
     )