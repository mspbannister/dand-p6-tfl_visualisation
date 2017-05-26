# coding: utf-8

"""
Script to clean TfL March cycle data and summarise it by start station.
Data files sourced from http://cycling.data.tfl.gov.uk/.
Note: assumes data files are located in 'Hire_data' subfolder.
Author: Mark Bannister (mspbannister@gmail.com)
"""

import requests
import json
import pandas as pd
from datetime import datetime

# Get all bike points from TfL API
app_id = "insert app_id"
app_key = "insert app_key"
params = {'app_id': app_id, 'app_key': app_key}
r = requests.get('https://api.tfl.gov.uk/BikePoint', params=params)
bike_points = r.json()

# Clean results and load into DataFrame
res = []
for point in bike_points:
    row = {}
    row['name'] = point['commonName']
    row['id'] = point['id'][(point['id'].find('_')+1):]
    row['lat'] = point['lat']
    row['lon'] = point['lon']
    res.append(row)
res_df = pd.DataFrame(res)

# Import and merge hire data CSVs
hire_df1 = pd.read_csv('Hire_data/'+ \
    '47JourneyDataExtract01Mar2017-07Mar2017.csv').dropna(axis=0, how='any')
hire_df2 = pd.read_csv('Hire_data/'+ \
    '48JourneyDataExtract08Mar2017-14Mar2017.csv').dropna(axis=0, how='any')
hire_df3 = pd.read_csv('Hire_data/'+ \
    '49JourneyDataExtract15Mar2017-21Mar2017.csv').dropna(axis=0, how='any')
hire_df4 = pd.read_csv('Hire_data/'+ \
    '50 Journey Data Extract 22Mar2017-28Mar2017.csv').dropna(axis=0, how='any')
hire_df = pd.concat([hire_df1, hire_df2, hire_df3, hire_df4], ignore_index=True)

# Convert station ids into strings to match API keys
hire_df['StartStation Id'] = hire_df['StartStation Id'].apply(int).apply(str)
hire_df['EndStation Id'] = hire_df['EndStation Id'].apply(int).apply(str)

# Merge with start station locations
loc_df = res_df[['id', 'lat', 'lon']]
hire_df_merged = pd.merge(hire_df, loc_df, left_on='StartStation Id', 
                          right_on='id', how ='left')\
                   .rename(columns={'Rental Id': 'Rental_Id', 
                                    'Bike Id': 'Bike_Id', 
                                    'End Date': 'End_Date', 
                                    'EndStation Id': 'EndStation_Id',
                                    'EndStation Name': 'EndStation_Name', 
                                    'Start Date': 'Start_Date', 
                                    'StartStation Id': 'StartStation_Id', 
                                    'StartStation Name': 'StartStation_Name', 
                                    'id': 'Start_Id', 
                                    'lat': 'StartStation_Lat', 
                                    'lon': 'StartStation_Lon'})

# Merge with end station locations (ultimately not used for this analysis)
hire_df_merged = pd.merge(hire_df_merged, loc_df, 
                          left_on='EndStation_Id', right_on='id', how ='left')\
                   .rename(columns={'id': 'End_Id', 'lat': 'EndStation_Lat', 
                                    'lon': 'EndStation_Lon'})

# Remove missing values
hire_df_merged = hire_df_merged.dropna(axis=0, how='any')

# Convert start date to datetime
def clean_date(x):
    pos = x.find('/17')
    if pos > 0:
        x = x[:pos] + '/2017' + x[(pos + 3):]
    return x
    
hire_df_merged['Start_Date'] = hire_df_merged['Start_Date'].apply(clean_date)
hire_df_merged['Start_Date'] = hire_df_merged['Start_Date'].apply(lambda x: \
                                  datetime.strptime(x, '%d/%m/%Y %H:%M'))

# Add Weekday and Weekend columns
hire_df_merged['Weekday'] = hire_df_merged['Start_Date']\
                                .apply(datetime.isoweekday)
hire_df_merged['Weekend'] = hire_df_merged['Start_Date']\
                                .apply(datetime.isoweekday)
def weekday(x):
    if x < 6:
        return 1
    else:
        return 0
    
def weekend(x):
    if x >= 6:
        return 1
    else:
        return 0
    
hire_df_merged['Weekday'] = hire_df_merged['Weekday'].apply(weekday)
hire_df_merged['Weekend'] = hire_df_merged['Weekend'].apply(weekend)

# Create summary data by station
gb_start = hire_df_merged.groupby('StartStation_Id', as_index=False)
gb_station = pd.concat([gb_start.count()[['StartStation_Id', 'Rental_Id']],
                        gb_start.sum()[['Weekday', 'Weekend']]], axis=1)\
             .rename(columns={'Rental_Id': 'Total'})

# Convert to daily averages
gb_station['Total'] = gb_station['Total'] / 28
gb_station['Weekday'] = gb_station['Weekday'] / 20
gb_station['Weekend'] = gb_station['Weekend'] / 8

# Merge with location data and drop surplus columns
loc_df = res_df[['id', 'lat', 'lon', 'name']]
gb_station = pd.merge(gb_station, loc_df, left_on='StartStation_Id', 
                      right_on='id', how ='left')\
               .drop('id', 1)\
               .rename(columns={'StartStation_Id': 'Station_Id',
                                'lat': 'Station_Lat',
                                'lon': 'Station_Lon',
                                'name': 'Station_Name'})
gb_station = gb_station[['Station_Id', 'Station_Name', 'Station_Lat', 
                         'Station_Lon', 'Total', 'Weekday', 'Weekend']]

# Remove spaces before commas in station names
def clean_station_names(x):
    pos = x.find(' ,')
    if pos > 0:
        x = x[:pos] + ',' + x[(pos+2):]
    return x

gb_station['Station_Name'] = gb_station['Station_Name']\
    .apply(clean_station_names)

# Export to CSV
gb_station.to_csv('March_Cycle_Hire_Summary.csv', index=False, 
                     encoding="utf-8")