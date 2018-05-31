
"""
 Programe:Swiss national grid coordinates (CH1903) to WGS1984 (World Geodetic System )
"""
#%% imports

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
from scipy import stats


from __future__ import division # for conversion


participant_data_path = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\Participant_Data"
directory_norm_sensor_data = participant_data_path+"\\gps_sensor_data\\5s\\smoot_signals\\corrected_normalized"
file_list_sensors = os.listdir(directory_norm_sensor_data)

for sensor in file_list_sensors:
    print(sensor)
    sensor_data = pd.read_csv(os.path.join(directory_norm_sensor_data, sensor))
    del sensor_data["Unnamed: 0"]
    del sensor_data["Unnamed: 0.1"]
    chy = np.asarray(sensor_data['X'].tolist()) #This should go to A input
    chx = np.asarray(sensor_data['Y'].tolist()) #This should go B input
    WGS_x,WGS_y = CH1903toWGS1984(chx, chy)
    sensor_data["wgs_x"] = WGS_x.tolist()
    sensor_data["wgs_y"] = WGS_y.tolist()
    #sensor_data.plot(kind='scatter', x='wgs_x', y='wgs_y')# just to check is it works
    #sensor_data.to_csv(os.path.join(directory_norm_sensor_data, sensor), index = False, header = False)
    sensor_data.to_csv(os.path.join(directory_norm_sensor_data, sensor), index = False)
    

#%%renaming and removing header
directory_norm_sensor_data = "C:\\Users\\vojha\\Dropbox\\0_Programming\\07_Processing\\Sketchbook\\esum_data\\data\\raw_gps_norm"
file_list_sensors = os.listdir(directory_norm_sensor_data)

i = 1
for sensor in file_list_sensors:
    print(sensor)
    sensor_data = pd.read_csv(os.path.join(directory_norm_sensor_data, sensor), index_col = False)
    name = str(i)+".csv"
    sensor_data.to_csv(os.path.join(directory_norm_sensor_data, sensor), index = False, header = False)
    i = i + 1
    

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