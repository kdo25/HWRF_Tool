## Calls both the NATL_recurve.py and NATL_climo_recurve.py scripts to create a bar graph that shows the difference between the two

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

execfile('NATL_recurve.py')

startYear1 = startYear
endYear1 = endYear

## Creates new df of ATL data

recurve_data = {'Storm ID' : id_names, 'Name' : names, 'Recurvature' : recurve}
recurve = pd.DataFrame.from_dict(recurve_data, orient = 'columns', dtype = None)
recurve = recurve[['Storm ID', 'Name', 'Recurvature']]
recurve = recurve.set_index(['Storm ID'])


execfile('NATL_climo_recurve.py')

## Creates new df of climo data

climo_data = {'Storm ID' : id_names, 'Name' : names, 'Recurvature' : climo}
climo = pd.DataFrame.from_dict(climo_data, orient = 'columns', dtype = None)
climo = climo[['Storm ID', 'Name', 'Recurvature']]
climo = climo.set_index(['Storm ID'])

## Creates bar graph

N = 3

## Multiplies by 100 to create a percentage for climo

tot_climo = climo['Recurvature'].describe().loc[['count']]
yes_climo = (climo['Recurvature'].str.count('Recurved').sum()/tot_climo)*100
und_climo = (climo['Recurvature'].str.count('Undefined').sum()/tot_climo)*100
no_climo = (climo['Recurvature'].str.count('Did not Recurve').sum()/tot_climo)*100

## Assigns x and y values and width and plots data

x = np.arange(N)
y = (yes_climo, und_climo, no_climo)
width = 0.25

fig, ax = plt.subplots(figsize=(10,6))
plot1 = ax.bar(x, y, width)

## Multiplies by 100 to create a percentage for target years
tot = recurve['Recurvature'].describe().loc[['count']]
yes = (recurve['Recurvature'].str.count('Recurved').sum()/tot)*100
und = (recurve['Recurvature'].str.count('Undefined').sum()/tot)*100
no = (recurve['Recurvature'].str.count('Did not Recurve').sum()/tot)*100

## Assigns new y values and plots on same graph right next to eachother to allow for easy comparison

y = (yes, und, no)

plot2 = ax.bar(x+width, y, width)

## Set different labels and increase font size for better visualization

plt.xticks(np.arange(min(x), max(x)+1, 1))
ax.set_xticks(x+width/2)
ax.set_xticklabels(('Recurved', 'Undefined', 'Did not Recurve'), fontsize=14)
ax.set_ylabel('Percentage', fontsize=14)
ax.legend((plot1[0], plot2[0]), ('Climatology', '%s-%s' %(startYear1, endYear1)), loc='upper center', fontsize=12)


if startYear == endYear:
    ax.set_title('Percentage of Storms Recurved in the Atlantic Basin during %s vs. Climatology' %(endYear1), fontsize=14)
else:
    ax.set_title('Percentage of Storms Recurved in the Atlantic Basin from %s-%s vs. Climatology' %(startYear1, endYear1), fontsize=14)

## Creates labels of percentages to include above bars    

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        height = float(round(height, 3))
        
        ax.text(rect.get_x() + rect.get_width()/2., 1.0*height,
                '%s%%' % float(height),
                ha='center', va='bottom')

autolabel(plot1)
autolabel(plot2)

plt.show()

