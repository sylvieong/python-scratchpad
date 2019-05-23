# -*- coding: utf-8 -*-
"""
Created on Thu May 23 06:27:33 2019

@author: SylvieOng
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd

#%% 
# Data
r = [0,1,2,3,4]
raw_data = {'greenBars': [20, 1.5, 7, 10, 5], 'orangeBars': [5, 15, 5, 10, 15],'blueBars': [2, 15, 18, 5, 10]}
df = pd.DataFrame(raw_data)
#%%

#TODO: ie. emulate code above, get df where rows are cities, columns are ime ind 0 and 1
#entries are counts for city, and each ime ind

#TODO: add total column to the df
#TODO: sort rows of df by the total column (descending order)
#TODO: sum up each column, get row for "all"
#TODO: then do the following to get percentages
 
# From raw value to percentage
totals = [i+j+k for i,j,k in zip(df['greenBars'], df['orangeBars'], df['blueBars'])]
greenBars = [i / j * 100 for i,j in zip(df['greenBars'], totals)]
orangeBars = [i / j * 100 for i,j in zip(df['orangeBars'], totals)]
blueBars = [i / j * 100 for i,j in zip(df['blueBars'], totals)]
 

# plot
barWidth = 0.85
names = ('City L','City M','City N','City O','City P')
# Create green Bars
plt.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth, label="IME Ind 0")
# Create orange Bars
plt.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth, label="IME Ind 1")
# Create blue Bars
plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color='#a3acff', edgecolor='white', width=barWidth, label="IME Ind Unk")

# Custom x axis
plt.xticks(r, names)
plt.xlabel("group")
plt.xticks(rotation=70)

# Add a legend
plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)

 
# Show graphic
plt.show()
 