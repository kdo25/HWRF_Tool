## This does the same exact thing as NATL_df.py, but sets it for climatology instead. We define climatology from 1965-2016 because this is during the satellite era

import requests
import pandas as pd
import io
import numpy as np
from collections import Counter

# Set target years to be for climatology
startYear=1965
endYear=2016
atlantic_raw = requests.get("http://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2016-041117.txt")
atlantic_raw.raise_for_status()

c = Counter()
for line in io.StringIO(atlantic_raw.text).readlines():
    c[line[:2]] += 1

atlantic_storms_r = []
atlantic_storm_r = {'header': None, 'data': []}

for i, line in enumerate(io.StringIO(atlantic_raw.text).readlines()):
    if line[:2] == 'AL' and int(line[4:8])>=startYear and int(line[4:8])<=endYear:
        atlantic_storms_r.append(atlantic_storm_r.copy())
        atlantic_storm_r['header'] = line
        atlantic_storm_r['data'] = []
    elif line[:2] != 'AL' and int(line[:4])>=startYear and int(line[:4])<=endYear:
        atlantic_storm_r['data'].append(line)

atlantic_storms_r.append(atlantic_storm_r.copy())
atlantic_storms_r = atlantic_storms_r[1:]

atlantic_storm_dfs = []
for storm_dict in atlantic_storms_r:
    storm_id, storm_name, storm_entries_n = storm_dict['header'].split(",")[:3]
    # remove hanging newline ('\n'), split fields
    data = [[entry.strip() for entry in datum[:-1].split(",")] for datum in storm_dict['data']]
    frame = pd.DataFrame(data)
    frame['id'] = storm_id
    frame['name'] = storm_name
    atlantic_storm_dfs.append(frame)
    
atlantic_storms = pd.concat(atlantic_storm_dfs)

cols = atlantic_storms.columns.tolist()
cols = cols[-2:] + cols[:-2]
atlantic_storms = atlantic_storms[cols]

atlantic_storms.columns = [
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
atlantic_storms['Date'] = pd.to_datetime(atlantic_storms['Date'])
