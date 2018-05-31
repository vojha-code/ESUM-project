# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 16:44:51 2018

@author: vojha
"""


#Reset all varables
%reset -f
%clear
#importing packages
import pandas as pd
import numpy as np
import scipy.signal as scisig
import os

from datetime import datetime
from datetime import timedelta
from calendar import timegm
import dateutil.parser
import math

import seaborn.apionly as sns
import matplotlib.pyplot as plt
from scipy import stats
#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
city = "HK"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_"+city)
path_raw_data_files = os.path.join(path_raw_data_files,"for_stat")

os.chdir(path_raw_data_files)
#%%
data_participant = pd.read_csv("merged_data.csv")
data_participant = data_participant.drop(['Unnamed: 0'], axis=1)
#%%
if(city == "ML"):
    data_participant = pd.read_csv("data_gps_corrected_mellborne.csv")
if(city == "SG"):
    data_participant = pd.read_csv("data_gps_corrected_singapore.csv")
if(city == "ZH"):
    data_participant = pd.read_csv("merged_data.csv")
    data_participant = data_participant.drop(['Unnamed: 0'], axis=1)
if(city == "CN"):
    data_participant = pd.read_csv("merged_data.csv")
    data_participant = data_participant.drop(['Unnamed: 0'], axis=1)    
if(city == "HK"):
    data_participant = pd.read_csv("merged_data.csv")
    data_participant = data_participant.drop(['Unnamed: 0'], axis=1) 
#%%
data_grouped_location = data_participant.groupby(['X','Y']).mean()

if (city == "ZH"):
    data_grouped_location = data_grouped_location[['Temp','RH','Sound','Lux','peakSCR_0p05','phasicSCR_0p05','tonicSCL_0p05']]    
    new_names = ['Temp','RH','Sound','Lux','nSCR','SCR', 'SCL']
elif(city == "SG"):
    data_grouped_location = data_grouped_location[['HSTemp','HSRH','Wind','Sound','Lux','peakSCR_0p05','phasicSCR_0p05','tonicSCL_0p05']] 
    new_names = ['Temp','RH','Wind','Sound','Lux','nSCR', 'SCR','SCL']
elif(city == "HK"):
    data_grouped_location = data_grouped_location[['Temp','RH','Sound','Lux','peakSCR_0p05','phasicSCR_0p05','tonicSCL_0p05']]
    new_names = ['Temp','RH','Sound','Lux','nSCR','SCR', 'SCL']    
else:    
    data_grouped_location = data_grouped_location[['HSTemp','HSRH','Wind','Lux','peakSCR_0p05','phasicSCR_0p05','tonicSCL_0p05']]     
    new_names = ['Temp','RH','Wind','Lux','nSCR', 'SCR','SCL']
    
old_names = data_grouped_location.columns
data_grouped_location.rename(columns=dict(zip(old_names, new_names)), inplace=True)
        

data_grouped_location.to_csv("data_xymean"+city+".csv")

data_grouped_location = pd.read_csv("data_xymean"+city+".csv")
data_grouped_location.plot.scatter(x = 'X', y = 'Y')

#%%
if(city == "ZH"):
    rageList = [2,3,4,5,6,7,8,9,10]  # ZH
elif(city == "SG"):
    rageList = [1,2,3,4,5,6,7,8,9]  # SG
else:
    rageList = [1,2,3,4,5,6]  # ML
    
for i in rageList:
#for i in range(1,9):
    df = data_participant[data_participant["PID"] == i]
    file_name = str(i)+".csv"
    if (city == "ZH"):
        df = df[['X','Y','Temp','RH','Sound','Lux','peakSCR_0p05','phasicSCR_0p05','tonicSCL_0p05']]    
        new_names = ['X','Y','Temp','RH','Sound','Lux','nSCR','SCR', 'SCL']
    elif(city == "SG"):
        df = df[['X','Y','HSTemp','HSRH','Wind','Sound','Lux','peakSCR_0p05','phasicSCR_0p05','tonicSCL_0p05']] 
        new_names = ['X','Y','Temp','RH','Wind','Sound','Lux','nSCR', 'SCR','SCL']
    else:    
        df = df[['X','Y','HSTemp','HSRH','Wind','Lux','peakSCR_0p05','phasicSCR_0p05','tonicSCL_0p05']]     
        new_names = ['X','Y','Temp','RH','Wind','Lux','nSCR', 'SCR','SCL']

    old_names = df.columns
    df.rename(columns=dict(zip(old_names, new_names)), inplace=True)    
    df.to_csv(file_name, index = False)