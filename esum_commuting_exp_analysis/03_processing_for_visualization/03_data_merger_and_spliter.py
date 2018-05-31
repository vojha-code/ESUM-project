# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 13:00:16 2018

@author: vojha
"""
#Reset all varables
%reset -f
%clear

import pandas as pd
import numpy as np
import scipy.signal as scisig
import os
from datetime import datetime
from datetime import timedelta
from calendar import timegm
import dateutil.parser
import math
#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
city = "ZH"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_"+city)
path_raw_data_files = os.path.join(path_raw_data_files,"compiled_data")

os.chdir(path_raw_data_files)
file_list = os.listdir(path_raw_data_files)
#%% cleaning X and Y
correction_required = False
if(correction_required == True):
    for file in file_list:
        data_current = pd.read_csv(file)
        
        data_current['X'] = np.where(data_current['X']== 'no_data', np.nan, data_current['X'])
        data_current['Y'] = np.where(data_current['Y']== 'no_data', np.nan, data_current['Y'])
        
        del data_current["Unnamed: 0"]   
        data_current.to_csv(file, index=False)
        
    for file in file_list:
        data_current = pd.read_csv(file)
        
        data_current['X'] = data_current['X'].interpolate(method="linear", axis=0)
        data_current['Y'] = data_current['Y'].interpolate(method="linear", axis=0)
        
        #del data_current["Unnamed: 0"]   
        data_current.to_csv(file,index=False)   
else:
    print("Correction not required")
#%%    File merger code
i = 0
for file in file_list:
    if(i == 0):
        result = pd.DataFrame.from_csv(file)
        #result = result.drop(['Unnamed: 0'], axis=1)
        i = i+1
    else:
        temp = pd.DataFrame.from_csv(file)
        #temp = temp.drop(['Unnamed: 0'], axis=1)
        result = result.append(temp)
#result.interpolate()
#result1 = result[result["Sound"] != 'no_data']
#result["Sound"].plot()
file_merged_data = os.path.join(path_raw_data_files, "merged_data_zscore.csv")
result.to_csv(file_merged_data)
#%% [Optional] Normalize the data    
#result = pd.DataFrame.from_csv(file_merged_data)
#cols_to_norm = ['peakSCR','phasicSCR', 'tonicSCL']
#result[['peak_norm','phasic_norm','tonic_norm']] = result[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
#result.to_csv("merged_data.csv")
#
##%% Data spliter based on columne catgory 
##result = pd.read_csv("merged_data.csv")
#
#
#data_diff_dictionary = {}    
#if(city == "ZH"):
#    rageList = [2,3,4,5,6,7,8,9,10]  # ZH
#elif(city == "SG"):
#    rageList = [1,2,3,4,5,6,7,8,9]  # SG
#else:
#    rageList = [3,4,5]  # ML
#    
#    
#d = {} #making a dictionary 
#for i in rageList:
##for i in range(1,9):
#    d[i] = result[result["PID"] == i]
#    file_name = str(i)+".csv"
#    cols_to_fetch = ['X','Y','peak','phase','peak_norm','phase_norm']
#    df = d[i][cols_to_fetch] 
#    print(len(df)," ->", len(df[df['X'] != 'no_data']))
#    df = df[df['X'] != 'no_data']#only for SG data
#    df.to_csv(file_name)

