# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:42:12 2020

@author: Brendan Non-Admin
"""

import numpy as np
import cv2

col_pixels = int(640 / 8)
row_pixels = int(640 / 8)
pixel_dimensions = (col_pixels, row_pixels)

black_square = np.full(pixel_dimensions, 0)
white_square = np.full(pixel_dimensions, 255)

rows = list()
for i in range(8):
    if i % 2 == 0:
        block_pairs = (white_square, black_square)
    else: 
        block_pairs = (black_square, white_square)
    
    block_pair_pixels = np.concatenate(block_pairs, axis=1)
    row = np.concatenate((block_pair_pixels , ) * 4, axis=1)
    rows.append(row)

pixels = np.concatenate(rows)

cv2.imwrite("chessboard.png", pixels)