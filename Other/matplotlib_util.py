# -*- coding: utf-8 -*-
"""
Created on Thu May  9 23:05:45 2019

@author: Brendan Non-Admin
"""

import matplotlib.pyplot as plt

def rotate_xticklabels(ax, rot):
    for item in ax.get_xticklabels():
        item.set_rotation(rot)