# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 17:31:40 2020

@author: Brendan Non-Admin
"""


from scipy.stats import gamma
import matplotlib.pyplot as plt
import numpy as np

lw = 4

# changing the shape parameter k
fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(18, 7))
x = np.linspace(0, 10, 100)
for i in range(1, 10, 2):
    k = i
    theta = 1
    a = k * theta
    rv = gamma(a=a)
    
    ax[0].plot(x, rv.pdf(x), lw=lw, alpha=0.6, label=f"k: {k}, theta: {theta}")
ax[0].legend()

# changing the scale parameter theta
for i in range(1, 10, 2):
    k = 1
    theta = i
    a = k * theta
    rv = gamma(a)
    
    ax[1].plot(x, rv.pdf(x), lw=lw, alpha=0.6, label=f"k: {k}, theta: {theta}")
ax[1].legend()
