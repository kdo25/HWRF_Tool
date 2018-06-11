## This script is nearly identical to NATL_df.py. It reads in HURDAT2 data
## from the NHC. However, this data includes information from the Central Pacific basin,
## so it was removed from the dataframe to focus soley on EPAC basin.

import requests
import pandas as pd
import io
import numpy as np

## Choose start and end year below

startYear= 2015
endYear= 2016

## Data from NHC website

pacific_raw = requests.get("http://www.nhc.noaa.gov/data/hurdat/hurdat2-nepac-1949-2016-041317.txt")
pacific_raw.raise_for_status()

readswitch = 1      
    
## Minor difference than AL data. Since HURDAT2 data includes 'EP' and 'CP', you have to ignore 'CP' data.    

pacific_storms_r = []
pacific_storm_r = {'header': None, 'data': []}

for i, line in enumerate(io.StringIO(pacific_raw.text).readlines()):
    if line[:2] == 'EP' and int(line[4:8])>=startYear and int(line[4:8])<=endYear:
        readswitch = 1
        pacific_storms_r.append(pacific_storm_r.copy())
        pacific_storm_r['header'] = line
        pacific_storm_r['data'] = []
    elif line [:2] == 'EP' and int(line[4:8])<startYear:
        readswitch = 0
    elif line [:2] == 'EP' and int(line[4:8])>endYear:
        readswitch = 0
    elif line[:2] == 'CP':
        readswitch = 0
    if readswitch == 1 and line[:2] != 'EP':
        pacific_storm_r['data'].append(line)


pacific_storms_r.append(pacific_storm_r.copy())
pacific_storms_r = pacific_storms_r[1:]



pacific_storm_dfs = []
for storm_dict in pacific_storms_r:
    storm_id, storm_name, storm_entries_n = storm_dict['header'].split(",")[:3]
    # remove hanging newline ('\n'), split fields
    data = [[entry.strip() for entry in datum[:-1].split(",")] for datum in storm_dict['data']]
    frame = pd.DataFrame(data)
    frame['id'] = storm_id
    frame['name'] = storm_name
    pacific_storm_dfs.append(frame)
    
   
    
pacific_storms = pd.concat(pacific_storm_dfs)


pacific_storms = pacific_storms.reindex(columns=pacific_storms.columns[-2:] | pacific_storms.columns[:-2])

pacific_storms.columns = [
        "Storm ID",
        "Name",
        "Date",
        "Hour (UTC)",
        "Record Identifier",
        "Status of System",
        "Latitude",
        "Longitude",
        "Maximum Sustained Wind Knots",
        "Maximum Pressure",
        "34 kt NE",
        "34 kt SE",
        "34 kt SW",
        "34 kt NW",
        "50 kt NE",
        "50 kt SE",
        "50 kt SW",
        "50 kt NW",
        "64 kt NE",
        "64 kt SE",
        "64 kt SW",
        "64 kt NW",
        ""
]

pd.set_option("max_columns", None)

pacific_storms['Date'] = pd.to_datetime(pacific_storms['Date']) 
