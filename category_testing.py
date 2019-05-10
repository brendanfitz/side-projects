# -*- coding: utf-8 -*-
"""
Created on Wed May  8 00:45:18 2019

@author: Brendan Non-Admin
"""
import fred_api as fred

root = fred.category()

cat_id = root.query('name == "Prices"').index[0]
df = fred.category(cat_id)

cat_id = root.query('name == "National Accounts"').index[0]
df = fred.category(cat_id)

cat_id = df.query('name == "National Income & Product Accounts"').index[0]
df = fred.category(cat_id)