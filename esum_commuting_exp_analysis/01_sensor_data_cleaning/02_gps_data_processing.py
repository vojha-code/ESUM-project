# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 13:19:01 2018

@author: vojha
"""
#%%importing packages
import pandas as pd
import numpy as np
import scipy.signal as scisig
import os
from datetime import datetime
from datetime import timedelta
from calendar import timegm
import dateutil.parser
import math
#%%

# Convert WGS lat/long (� dec) to CH x
def WGStoCHx(lat, lng):
    # Converts decimal degrees to sexagecimal seconds
    #lat = DECtoSEX(lat)
    #lng = DECtoSEX(lng)
    
    lat = ToSexAngle(lat)
    lng = ToSexAngle(lng)

    # Auxiliary values (% Bern)
    lat_aux = (lat - 169028.66) / 10000
    lng_aux = (lng - 26782.5) / 10000

	# Process X
    x = ((200147.07 \
			+ (308807.95 * lat_aux) \
			+ (3745.25 * pow(lng_aux, 2)) \
			+ (76.63 * pow(lat_aux, 2))) \
			- (194.56 * pow(lng_aux, 2) * lat_aux))\
			+ (119.79 * pow(lat_aux, 3))

    return x

def WGStoCHy(lat, lng):

    # Converts decimal degrees to sexagecimal seconds
    #lat = DECtoSEX(lat)
    #lng = DECtoSEX(lng)
    
    lat = ToSexAngle(lat)
    lng = ToSexAngle(lng)

    
    # Auxiliary values (% Berne)
    lat_aux = (lat - 169028.66) / 10000
    lng_aux = (lng - 26782.5) / 10000

    # Process Y
    y = (600072.37 \
			+ (211455.93 * lng_aux)) \
			- (10938.51 * lng_aux * lat_aux) \
			- (0.36 * lng_aux * pow(lat_aux, 2)) \
			- (44.54 * pow(lng_aux, 3))

    return y
#%% CH to WGS conversion definations
def CHtoWGSlat(x,y):
    """
    Convert CH1903 system to WGS1984 system (latitude)
 
    :param x: northing
    :param y: easting
    :return: latitude in WGS1984 system
 
    """
    x_aux = (x - 200000) / 1000000
    y_aux = (y - 600000) / 1000000
 
    lat = (16.9023892 + (3.238272 * x_aux)) \
          - (0.270978 * pow(y_aux, 2)) \
          - (0.002528 * pow(x_aux, 2)) \
          - (0.0447 * pow(y_aux, 2) * x_aux) \
          - (0.0140 * pow(x_aux, 3))
 
    lat = (lat * 100) / 36
 
    return lat
 
def CHtoWGSlng(x,y):
    """
    Convert CH1903 system to WGS1984 system (longitude)
 
    :param x: northing
    :param y: easting
    :return: longitude in WGS1984 system
 
    """
    x_aux = (x - 200000) / 1000000
    y_aux = (y - 600000) / 1000000
 
    lng = (2.6779094 + (4.728982 * y_aux) + (0.791484 * y_aux * x_aux) +
           (0.1306 * y_aux * pow(x_aux, 2))) - (0.0436 * pow(y_aux, 3))
 
    lng = (lng * 100) / 36
 
    return lng
 
def CH1903toWGS1984(x, y):
  """Converts coordinates from CH1903_LV03 to WGS1984 adopting the code taken from
     method from http://www.swisstopo.admin.ch/internet/swisstopo/de/home/products/software/products/skripts.html
 
     :param x: x coordinates in degrees in CH1903 (northing)
     :param y: y coordinates in degrees in CH1903 (easting)
     :return: a pair containing the latitude and longitude of the given coordinates, respectively"""
 
  lat = CHtoWGSlat(x, y)
  lng = CHtoWGSlng(x, y)
 
  return lat, lng
#%% Convert decimal angle to sexagesimal seconds
def DECtoSEX(angle):
    # Extract DMS
    deg = angle.astype(int)
    mnt = ((angle-deg)*60).astype(int)
    sec = (((angle-deg)*60)-mnt)*60
    # Result in seconds
    return sec + mnt * 60. + deg * 3600
#%% Convert decimal angle to sexagesimal seconds
def ToSexAngle(val):
    deg = np.floor(val)
    minimum = 100 * (val - deg)
    return minimum*60 + deg*3600
#%% correction of sigapore just a test
def convertNMEASentencesToWGS(x):
    degWhole = np.floor(x/100)
    degDec   = (x - degWhole*100)/60
    deg = degWhole + degDec;
    return deg
#%% Path setting to the folder wher the raw files are 
filespath_raw_data = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
filespath_raw_data = os.path.join(filespath_raw_data, "Data_ZH")
# set participant
participant = "09"
filepath_sensor = os.path.join(filespath_raw_data, participant) # looking specific participant folders
files_sensor = os.path.join(filepath_sensor,"processed1")

#%%GPS reading for general GPRMC data
file_gps_sensor =  os.path.join(files_sensor,'gps.csv')# fetching sensor  file path
data_gps_sensor = pd.read_csv(file_gps_sensor)
data_gps_sensor = data_gps_sensor.drop(['Unnamed: 0'], axis=1)

data_gps_sensor[["LAT_F","LON_F"]] = data_gps_sensor[["LAT","LON"]].apply(convertNMEASentencesToWGS)
data_gps_sensor["wgs_x"] = data_gps_sensor["LAT_F"].tolist()
data_gps_sensor["wgs_y"] = data_gps_sensor["LON_F"].tolist()
data_gps_sensor['wgs_x'] = np.where(data_gps_sensor['LAT']== 0.0, 0.0, data_gps_sensor['wgs_x'])
data_gps_sensor['wgs_y'] = np.where(data_gps_sensor['LAT']== 0.0, 0.0, data_gps_sensor['wgs_y'])

zeros = len(data_gps_sensor[data_gps_sensor['wgs_x']==0])
print(len(data_gps_sensor)," -> ",zeros)

data_gps_sensor.to_csv(file_gps_sensor)

#%% GPS sensor data reading for Swis data
file_gps_sensor =  os.path.join(files_sensor,'gps.csv')# fetching sensor  file path
data_gps_sensor = pd.read_csv(file_gps_sensor)
data_gps_sensor = data_gps_sensor.drop(['Unnamed: 0'], axis=1)

data_gps_sensor[["LAT_F","LON_F"]] = data_gps_sensor[["LAT","LON"]].apply(lambda x: (x) / (100))

x = np.asarray(data_gps_sensor['LAT_F'].tolist()) #This should go to A input
y = np.asarray(data_gps_sensor['LON_F'].tolist()) #This should go B input
 
CHx = WGStoCHx(x, y)
CHy = WGStoCHy(x, y)

WGS_x,WGS_y = CH1903toWGS1984(CHx, CHy)

data_gps_sensor["wgs_x"] = WGS_x.tolist()
data_gps_sensor["wgs_y"] = WGS_y.tolist()

data_gps_sensor["ch_x"] = CHx.tolist()
data_gps_sensor["ch_y"] = CHy.tolist()

data_gps_sensor['wgs_x'] = np.where(data_gps_sensor['LAT']== 0.0, 0.0, data_gps_sensor['wgs_x'])
data_gps_sensor['wgs_y'] = np.where(data_gps_sensor['LAT']== 0.0, 0.0, data_gps_sensor['wgs_y'])
#No CH 
data_gps_sensor['ch_x'] = np.where(data_gps_sensor['LAT']== 0.0, 0.0, data_gps_sensor['ch_x'])
data_gps_sensor['ch_y'] = np.where(data_gps_sensor['LAT']== 0.0, 0.0, data_gps_sensor['ch_y'])

#data_gps_sensor['wgs_x'] = data_gps_sensor['wgs_x'].interpolate(method="linear", axis=0)
#data_gps_sensor['wgs_y'] = data_gps_sensor['wgs_y'].interpolate(method="linear", axis=0)
#data_gps_sensor['ch_x'] = data_gps_sensor['ch_x'].interpolate(method="linear", axis=0)
#data_gps_sensor['ch_y'] = data_gps_sensor['ch_y'].interpolate(method="linear", axis=0)


data_gps_sensor.to_csv(file_gps_sensor)

#x = np.array(47.2223891)
#y = np.array(8.3101669)
#print(WGStoCHx(x, y))
#print(WGStoCHy(x, y))

