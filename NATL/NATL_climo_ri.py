#Does same as NATL_ri.py, but for climatology

import pandas as pd
import numpy as np

execfile('NATL_climatology_df.py')


## Create new df for climatology of RI

intense = atlantic_storms[['Storm ID', 'Name', 'Maximum Sustained Wind Knots']].copy()

intense = intense.convert_objects(convert_numeric=True)

id_names = pd.unique(intense['Storm ID'])
names = []
ri_difference = []
tot_difference = []
for id_name in id_names:
    sub_df = intense.loc[intense['Storm ID'] == id_name]
    names.append(sub_df['Name'][0])
    rapid_intense_diff = sub_df['Maximum Sustained Wind Knots'].diff()
    rapid_intense_diff = rapid_intense_diff[rapid_intense_diff >= 10].count()
    ri_difference.append(rapid_intense_diff)

    tot_intense_diff = sub_df['Maximum Sustained Wind Knots'].diff()
    tot_intense_diff = tot_intense_diff[tot_intense_diff > 0].count()
    tot_difference.append(tot_intense_diff)

    
ri_difference = np.array(ri_difference)
ri_difference = ri_difference*0.25

tot_difference = np.array(tot_difference)
tot_difference = tot_difference*0.25

