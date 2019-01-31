## This script creates a dataframe of the NIO basin and is used to determine whether or not storms recurved or not as well as
## if the underwent rapid intensification.

import numpy as np
import glob
import pandas as pd

# Select which year you would like to start with
year = 1965

## Creates main df to be used
recurve = []
ri = []
# Select which year you would like to end with
while(year<2015):
    storm_count = 1
    length = len(glob.glob('/homes/metogra/kdoughe1/HWRF_Tool/NIO/data/' + format(year) + 's_bio_full/*'))
    
    while(storm_count<= length):
        filename = glob.glob('/homes/metogra/kdoughe1/HWRF_Tool/NIO/data/' + format(year) + 's_bio_full/bio' + format(storm_count,'02d') + format(year) + '.txt')

        file = open(filename[0],mode='r')
        lines = file.readlines()
        lines = list(map(str.strip,lines))
        nio_storms = {'data': lines}
        
        nio_dfs = []
        for storm_dict in nio_storms['data']:
            storm_dict=storm_dict.split(",")
            df = pd.DataFrame([storm_dict[:9]])
            nio_dfs.append(df)

        nio_storms = pd.concat(nio_dfs).reset_index()

        nio_storms.columns = ["index",
                "Basin",
                "Storm Number",
                "Date",
                " ",
                "BEST",
                " ",
                "Latitude",
                "Longitude",
                "Maximum Sustained Wind Knots"
        ]  

#Determine whether storm recurved or not or was undefined

        long = nio_storms[['Basin', 'Storm Number', 'Date', 'Longitude', 'Maximum Sustained Wind Knots']].copy()
        long['Longitude'] = long['Longitude'].str.replace(r'E$', '')
        long['Longitude'] = long['Longitude'].str.replace(r'W$', '')
        long['Longitude'] = pd.to_numeric(long['Longitude'], downcast='float')
        long['Maximum Sustained Wind Knots'] = pd.to_numeric(long['Maximum Sustained Wind Knots'])
        #long['Longitude'].convert_objects(convert_numeric=True)
        long['Longitude'] = long['Longitude']/10.



        storms = pd.unique(long['Storm Number'])


        for storm in storms:
            sub_df = long.loc[long['Storm Number'] == storm]
            sub_df = sub_df.loc[(sub_df['Maximum Sustained Wind Knots'] > 30)] 
            long_diff = sub_df['Longitude'].diff()    #takes differences of change in longitude
            long_diff = long_diff.as_matrix()       #converts into a matrix
            long_diff = long_diff[~np.isnan(long_diff)] #ignores NaN data



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
                
#Determine if storm underwent RI
        intense = nio_storms[['Basin', 'Storm Number', 'Date', 'Maximum Sustained Wind Knots']].copy()
        intense['Maximum Sustained Wind Knots'] = pd.to_numeric(intense['Maximum Sustained Wind Knots'])
        
        storms = pd.unique(long['Storm Number'])
        ri_difference = []

        for storm in storms:
            sub_df = intense.loc[intense['Storm Number'] == storm]
            rapid_intense_diff = sub_df['Maximum Sustained Wind Knots'].diff()
            rapid_intense_diff = rapid_intense_diff[rapid_intense_diff >= 10].count()
            ri_difference.append(rapid_intense_diff)

        
        N  = 1.0 / 4
        ri_difference = [x*N for x in ri_difference]
        
        ri.append(ri_difference)
        
        

        storm_count = storm_count+1
    year = year+1

## Creates lists to count the number of storms that underwent RI or recurvature and seperates them into percentages
tot_ri = []
for sublist in ri:
    for item in sublist:
        tot_ri.append(item)

RI=[]
for x in tot_ri:
    if x == 0:
        result = 'No'
        RI.append(result)
    else:
        result = 'Yes'
        RI.append(result)
        
total = float(len(RI))
yes = (RI.count('Yes')/total)*100
no = (RI.count('No')/total)*100

print('Total storms: {0}'.format(total))
print('RI: {0}%'.format(round(yes,3)))
print('No RI: {0}%'.format(round(no,3)))
print('')
        

total = float(len(recurve))
rec = (recurve.count('Yes')/total)*100
norec = (recurve.count('No')/total)*100
und = (recurve.count('Und')/total)*100

print('Total: {0}'.format(total))
print('Recurved: {0}%'.format(round(rec,3)))
print('Did not recurve: {0}%'.format(round(norec,3)))
print('Undefined: {0}%'.format(round(und,3)))
