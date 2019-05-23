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
# Create green Bars #b5ffb9
plt.bar(r, greenBars, color='green', edgecolor='white', width=barWidth, label="IME Ind 0")
# Create orange Bars #f9bc86
plt.bar(r, orangeBars, bottom=greenBars, color='orange', edgecolor='white', width=barWidth, label="IME Ind 1")
# Create blue Bars #a3acff
plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color='blue', edgecolor='white', width=barWidth, label="IME Ind Unk")

# Custom x axis
plt.xticks(r, names)
plt.xlabel("group")
plt.xticks(rotation=70)

# Add a legend
plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)

 
# Show graphic
plt.show()

### grouped bars

# set width of bar
barWidth = 0.25

# Set position of bar on X axis
r1 = np.arange(len(greenBars))
r2 = [x + barWidth/3 for x in r1] #[x + barWidth/2 for x in r1]
r3 = [x + barWidth/3 for x in r2]
 
# Make the plot - #7f6d5f, #557f2d, #2d7f5e
plt.bar(r1, greenBars, color=(0.0, 0.5, 0.0, 0.2), width=barWidth, edgecolor='white', label='var1')
plt.bar(r2, orangeBars, color=(0.5, 0.0, 0.0, 0.2), width=barWidth, edgecolor='white', label='var2')
plt.bar(r3, blueBars, color=(0.0, 0.3, 0.7, 0.2), width=barWidth, edgecolor='white', label='var3')
 
# Add xticks on the middle of the group bars
plt.xlabel('group', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(greenBars))], ['A', 'B', 'C', 'D', 'E'])
 
# Create legend & Show graphic
plt.legend()
plt.show()
 