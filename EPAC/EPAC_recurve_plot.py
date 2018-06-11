## Creates plot comparing EPAC recurve data from seleceted years and climatology

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

execfile('EPAC_recurve.py')

startYear1 = startYear
endYear1 = endYear
recurve_data = {'Storm ID' : id_names, 'Name' : names, 'Recurvature' : recurve}
recurve = pd.DataFrame.from_dict(recurve_data, orient = 'columns', dtype = None)
recurve = recurve[['Storm ID', 'Name', 'Recurvature']]
recurve = recurve.set_index(['Storm ID'])


execfile('EPAC_climo_recurve.py')
climo_data = {'Storm ID' : id_names, 'Name' : names, 'Recurvature' : climo}
climo = pd.DataFrame.from_dict(climo_data, orient = 'columns', dtype = None)
climo = climo[['Storm ID', 'Name', 'Recurvature']]
climo = climo.set_index(['Storm ID'])

#creates bar graph
N = 3
#multiplies by 100 to create a percentage for climo
tot_climo = climo['Recurvature'].describe().loc[['count']]
yes_climo = (climo['Recurvature'].str.count('Recurved').sum()/tot_climo)*100
und_climo = (climo['Recurvature'].str.count('Undefined').sum()/tot_climo)*100
no_climo = (climo['Recurvature'].str.count('Did not Recurve').sum()/tot_climo)*100

#assigns x and y values and width and plots data
x = np.arange(N)
y = (yes_climo, und_climo, no_climo)
width = 0.25

fig, ax = plt.subplots(figsize=(10,6))
plot1 = ax.bar(x, y, width)

#multiplies by 100 to create a percentage for target years
tot = recurve['Recurvature'].describe().loc[['count']]
yes = (recurve['Recurvature'].str.count('Recurved').sum()/tot)*100
und = (recurve['Recurvature'].str.count('Undefined').sum()/tot)*100
no = (recurve['Recurvature'].str.count('Did not Recurve').sum()/tot)*100

#assigns new y values and plots on same graph right next to eachother to allow for easy comparison
y = (yes, und, no)

plot2 = ax.bar(x+width, y, width)

#set different labels and increase font size for better visualization
plt.xticks(np.arange(min(x), max(x)+1, 1))
ax.set_xticks(x+width/2)
ax.set_xticklabels(('Recurved', 'Undefined', 'Did not Recurve'), fontsize=14)
ax.set_ylabel('Percentage', fontsize=14)
ax.legend((plot1[0], plot2[0]), ('Climatology', '%s-%s' %(startYear1, endYear1)), loc='upper center', fontsize=12)


if startYear == endYear:
    ax.set_title('Percentage of Storms Recurved in the EPAC Basin during %s vs. Climatology' %(endYear1), fontsize=14)
else:
    ax.set_title('Percentage of Storms Recurved in the EPAC Basin from %s-%s vs. Climatology' %(startYear1, endYear1), fontsize=14)

#creates labels of percentages to include above bars    
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

