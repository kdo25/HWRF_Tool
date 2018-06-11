## Creates histogram comparing selected years and climatology.

import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pandas.plotting import table
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from scipy.optimize import curve_fit


execfile('EPAC_ri.py')

intense_data = {'Storm ID' : id_names, 'Name' : names, 'Days of Intensification' : tot_difference, 'Days of RI' : ri_difference}
intense = pd.DataFrame.from_dict(intense_data, orient = 'columns', dtype = None)
intense = intense[['Storm ID', 'Name', 'Days of Intensification', 'Days of RI']]
intense_df = intense.set_index(['Storm ID'])

#Create histogram
x = intense[['Days of Intensification']].copy()
maxbin = x['Days of Intensification'].max() + 0.5
x = x.as_matrix()
binsnew = np.arange(0,maxbin,0.25)

# Plots histogram of 'Days of Intensification' as pmf NOT pdf
n, bins1 = np.histogram(x, bins=binsnew, density=True)
newbins1 = (bins1[1:] + bins1[:-1]) /2.
n = n*0.25

    
# Does same as above, but for 'Days of RI' and plots on same histogram
y = intense[['Days of RI']].copy()
maxbin = y['Days of RI'].max() + 0.5
y = y.as_matrix()
binsnew = np.arange(0,maxbin,0.25)

m, bins2 = np.histogram(y, bins=binsnew, density=True)
newbins = (bins2[1:] + bins2[:-1]) /2.
m= m*0.25

startYear1 = startYear
endYear1 = endYear


execfile('EPAC_climo_ri')

intense_data = {'Storm ID' : id_names, 'Name' : names, 'Days of Intensification' : tot_difference, 'Days of RI' : ri_difference}
intense_climo = pd.DataFrame.from_dict(intense_data, orient = 'columns', dtype = None)
intense_climo = intense_climo[['Storm ID', 'Name', 'Days of Intensification', 'Days of RI']]
intense_climo = intense_climo.set_index(['Storm ID'])


fig, ax = plt.subplots(figsize=(10,6))

x_climo = intense_climo[['Days of Intensification']].copy()
maxbin_climo = x_climo['Days of Intensification'].max() + 0.5
x_climo = x_climo.as_matrix()
binsnew_climo = np.arange(0,maxbin_climo,0.25)

# Plots histogram of 'Days of Intensification' as pmf NOT pdf
n_climo, bins1_climo = np.histogram(x_climo, bins=binsnew_climo, density=True)
newbins_climo1 = (bins1_climo[1:] + bins1_climo[:-1]) /2.
n_climo = n_climo*0.25  

def func(x, a, b):
    return a * np.exp(b*x)
parameter1, covariance_matrix1 = curve_fit(func, newbins_climo1, n_climo)

int_patches = plt.bar(newbins1, n, width=0.25, alpha=0.6)    

plt.plot(newbins_climo1, func(newbins_climo1, *parameter1), 'k--')

    
# Does same as above, but for 'Days of RI' and plots on same histogram
y_climo = intense_climo[['Days of RI']].copy()
maxbin_climo = y_climo['Days of RI'].max() + 0.5
y_climo = y_climo.as_matrix()
binsnew_climo = np.arange(0,maxbin_climo,0.25)

m_climo, bins2_climo = np.histogram(y_climo, bins=binsnew_climo, density=True)
newbins_climo2 = (bins2_climo[1:] + bins2_climo[:-1]) /2.
m_climo= m_climo*0.25

def func(x, a, b):
    return a * np.exp(b*x)
parameter2, covariance_matrix2 = curve_fit(func, newbins_climo2, m_climo)

ri_patches = plt.bar(newbins, m, width=0.25, alpha=0.6)

plt.plot(newbins_climo2, func(newbins_climo2, *parameter2), 'r--')

# Adds labels and data table. Data table is messy so I have commented it out for the plot
ax.set_xlabel('Days', fontsize=14)
ax.set_ylabel('Normalized Frequency', fontsize=14)
plt.rcParams.update({'font.size': 14})
#table_data = intense_df.describe().loc[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]
#table_data = table_data.round(3)
#table(ax, table_data, loc = 'center right', colWidths=[0.2,0.2])

if startYear == endYear:
    ax.set_title('Days EPAC Storms Intensified and Rapidly Intensified during %s' %(endYear1))
else:
    ax.set_title('Days EPAC Storms Intensified and Rapidly Intensified from %s-%s' %(startYear1, endYear1))



# Add legend
int_patches = mpatches.Patch(label='Days of Intensification', alpha=0.6)
ri_patches = mpatches.Patch(color='orange', label='Days of RI')
intense_climo = mlines.Line2D([], [], linestyle='--', color='black', label='Climatology of Intensification')
ri_climo = mlines.Line2D([], [], linestyle='--', color='red',label='Climatology of RI')
plt.legend(handles=[int_patches, ri_patches, intense_climo, ri_climo])

plt.show()


