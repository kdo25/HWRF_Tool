## See comments in NATL_recurve.py. (Similar script but for EPAC)

import pandas as pd
import numpy as np


execfile('EPAC_df.py')

long = pacific_storms[['Storm ID', 'Name', 'Status of System', 'Longitude']].copy()
long['Longitude']= long['Longitude'].map(lambda long: long[:-1] if long[-1] == "E" else "-" + long[:-1])
long = long.convert_objects(convert_numeric=True)
long['Status of System'].astype(str)

id_names = pd.unique(long['Storm ID'])
names = []
recurve = []

for id_name in id_names:
    sub_df = long.loc[long['Storm ID'] == id_name]
    names.append(sub_df['Name'][0])
    sub_df = sub_df.loc[sub_df['Status of System'].isin(['TD', 'TS', 'HU'])]   #only looks at data that is a TD, TS, or HU
    long_diff = sub_df['Longitude'].diff()    #takes differences of change in longitude
    long_diff = long_diff.as_matrix()       #converts into a matrix
    long_diff = long_diff[~np.isnan(long_diff)] #ignores NaN data
    #print(long_diff)
    
    sums=[]
    total = 0
    sign = -1 
    for i, val in enumerate(long_diff):
        newtotal = total + sign*val
        if newtotal < total:
            sums.append(total)
            total = val
            sign= -1*sign
        else:
            total = total+val
    sums.append(total)
    
    indW = [i for i in range(len(sums)) if sums [i] <=-1]
    indE = [i for i in range(len(sums)) if sums [i] >= 1]
    
     
    if len(indW) > 1 and len(indE) > 1:
        if indW[0] < indE[0]:
            result = "Yes"
            recurve.append(result)
        elif indW[0] < indE[1]:
            result = "Yes"
            recurve.append(result)
        elif indW[1] < indE[0]:
            result = "Yes"
            recurve.append(result)
        else:
            result = "Und"
            recurve.append(result)
    elif len(indW) > 1 and len(indE) == 1:
        if indW[0] < indE[0]:
            result = "Yes"
            recurve.append(result)
        elif indW[1] < indE[0]:
            result = "Yes"
            recurve.append(result)
        else:
            result = "Und"
            recurve.append(result)
    elif len(indE) > 1 and len(indW) == 1:
        if indW[0] < indE[1]:
            result = "Yes"
            recurve.append(result)
        else:
            result = "Und"
            recurve.append(result)
    elif len(indW) > 1 and len(indE) == 0:
        result = "No"
        recurve.append(result)
    elif len(indE) > 1 and len(indW) == 0:
        result = "Und"
        recurve.append(result)
    elif len(indE) == 0:
        result = "No"
        recurve.append(result)
    elif len(indW) == 0 and len(indE) == 1:
        result = "Und"
        recurve.append(result)
    elif indW[0] < indE[0]:
        result = "Yes"
        recurve.append(result)
    else:
        result = "Und"
        recurve.append(result)


