# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 18:12:10 2020

@author: Brendan Non-Admin
"""

formula = "=(OFFSET($K4, 0, $C$2) {}\n) / $C$2"
formula_aggregator = ""
formula_line_template = "+ IF($C$2-{i}>0, OFFSET($K4, {i}, $C$2-{i}), 0)\n"

for i in range(1, 36):
    formula_aggregator += formula_line_template.format(i=i)


formula = formula.format(formula_aggregator)

print(formula)