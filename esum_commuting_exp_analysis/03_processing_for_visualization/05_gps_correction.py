# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:47:39 2018

@author: vojha
"""

#Reset all varables
%reset -f
#importing packages
import pandas as pd
import numpy as np
import os
import scipy.signal as scisig

from datetime import datetime
from datetime import timedelta
from calendar import timegm
import dateutil.parser
#%% Path setting to the folder wher the raw files are 
city = "SG"

path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_"+city)
path_raw_data_files = os.path.join(path_raw_data_files,"for_stat")
os.chdir(path_raw_data_files)

#%%
data_participant = pd.read_csv("gps_correction_merged_data.csv")
data_participant = data_participant.drop(['Unnamed: 0'], axis=1)

data_gps_points = pd.read_csv("gps_points.csv")
#retriveing gps point every 5 seconds
#df1 = df[df.index % 3 != 0]  # Excludes every 3rd row starting from 0
#data_gps5sec = data_gps_points[data_gps_points.index % 5 == 0]  # Selects every 3rd raw starting from 0
#%%
data_gps_dictionary = {}   
for i in [1,2,3,4,5,6,7,8,9]:
    data_indvidual = data_participant[data_participant['PID'] == i]

    #convert no_data to nan
    data_indvidual['X'] = np.where(data_indvidual['X'] == 'no_data', np.nan, data_indvidual['X'])
    data_indvidual['Y'] = np.where(data_indvidual['Y'] == 'no_data', np.nan, data_indvidual['Y'])

    data_indvidual['X'] = [float(x) for x in data_indvidual['X'].tolist()]
    data_indvidual['Y'] = [float(x) for x in data_indvidual['Y'].tolist()]

    # interpolation
    data_indvidual['X'] = data_indvidual['X'].interpolate(method="linear", axis=0)
    data_indvidual['Y'] = data_indvidual['Y'].interpolate(method="linear", axis=0)
    
    # filing moving average
    #data_indvidual = data_indvidual.fillna(pd.rolling_mean(data_indvidual, 5, min_periods=1).shift(-3))
    #data_indvidual = data_indvidual.rolling(window=3,min_periods=1,center=True).mean()
    
    if(i > 6):
        from scipy import stats
        cutoff = 1.1 # this may varry form case to case for 3 use 0.4;
        data_indvidual["CutXY"] = (np.abs(stats.zscore(data_indvidual['X'])) < cutoff).tolist()
        data_indvidual = data_indvidual[data_indvidual['CutXY'] == True]
    
    #data_gps_points.plot.scatter(x = 'X', y = 'Y')    
    data_ind = data_indvidual.dropna()
    data_ind.plot.scatter(x = 'X', y = 'Y')
    data_gps_dictionary[i] = data_ind
    print(i)

frames = [data_gps_dictionary[d] for d in data_gps_dictionary]
result = pd.concat(frames)
result.to_csv('data_gps_corrected.csv',index = False, header=True)
