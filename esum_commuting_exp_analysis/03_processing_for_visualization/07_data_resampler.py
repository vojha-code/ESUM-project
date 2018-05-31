# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 13:27:23 2018

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
import math
from scipy import stats

import datetime
from datetime import timedelta
from calendar import timegm
import dateutil.parser
from time import mktime

#%% processing time data 
def make_timestamnp(timedata):
    return mktime(timedata.timetuple())
    

def convert_from_timestamp(date_in_some_format):
    date_as_string = datetime.datetime.fromtimestamp(date_in_some_format)
    date_as_string = date_as_string + timedelta(hours=+int(0)) # correction for UTC time difference
    return date_as_string

def convert_to_timestamp(date_in_some_format):
    date_as_string = dateutil.parser.parse(date_in_some_format)
    return date_as_string

# data time parsers with correction of time
def convert_to_timestamp_correction(date_in_some_format):
    date_as_string = dateutil.parser.parse(date_in_some_format)
    date_as_string = date_as_string + timedelta(hours=+int(2)) # correction for UTC time difference
    return date_as_string 
#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
city = "ZH"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_"+city)
path_raw_data_files = os.path.join(path_raw_data_files,"for_stat")

os.chdir(path_raw_data_files)

#%%
data_participant = pd.read_csv("merged_data_zscore.csv")


dictionary = {} 
if(city == "ZH"):
    rageList = [2,3,4,5,6,7,8,9,10]  # ZH
    dictionary[2] = data_participant[data_participant['PID'] == 2]
    dictionary[3] = data_participant[data_participant['PID'] == 3]
    dictionary[4] = data_participant[data_participant['PID'] == 4]
    dictionary[5] = data_participant[data_participant['PID'] == 5]
    dictionary[6] = data_participant[data_participant['PID'] == 6]
    dictionary[7] = data_participant[data_participant['PID'] == 7]
    dictionary[8] = data_participant[data_participant['PID'] == 8]
    dictionary[9] = data_participant[data_participant['PID'] == 9]
    dictionary[10] = data_participant[data_participant['PID'] == 10]    
elif(city == "SG"):
    rageList = [1,2,3,4,5,6,7,8,9]  # SG
    dictionary[1] = data_participant[data_participant['PID'] == 1]   
    dictionary[2] = data_participant[data_participant['PID'] == 2]
    dictionary[3] = data_participant[data_participant['PID'] == 3]
    dictionary[4] = data_participant[data_participant['PID'] == 4]
    dictionary[5] = data_participant[data_participant['PID'] == 5]
    dictionary[6] = data_participant[data_participant['PID'] == 6]
    dictionary[7] = data_participant[data_participant['PID'] == 7]
    dictionary[8] = data_participant[data_participant['PID'] == 8]
    dictionary[9] = data_participant[data_participant['PID'] == 9] 
    
elif(city == "HK"):
    rageList = [4]  # HK  
    dictionary[4] = data_participant[data_participant['PID'] == 4]    
elif(city == "CN"):
    rageList = [3,6]  # CN
    dictionary[1] = data_participant[data_participant['PID'] == 1]
    dictionary[6] = data_participant[data_participant['PID'] == 6]
else:
    rageList = [1,4]  # ML
    dictionary[1] = data_participant[data_participant['PID'] == 1]
    dictionary[4] = data_participant[data_participant['PID'] == 4]


data_diff_dictionary = {}    
for i in rageList:  
    #i = 4
    print(i)
    participant = i
    data_pid = dictionary[i]
    if(city == "ZH"):
        listcolumn = ['PID','Time','Temp','RH','Lux','Sound','Peak','Amp','EvenName']
        #listcolumn = ['PID','Time','Temp','RH','Lux','Sound','TTP_peak','TTP_AmpUs','CDA_TonicUs','EvenName']
        data_resamples = data_pid[listcolumn]            
    else:
        data_resamples = data_pid[['PID','Time','HSTemp','HSRH','Sound','Lux','Wind','TTP_peak','TTP_AmpUs','CDA_TonicUs','EvenName']] 
        
    data_resamples["Timestamp"] = data_resamples["Time"].apply(convert_from_timestamp)
    data_resamples = data_resamples.set_index(pd.DatetimeIndex(data_resamples['Timestamp']))
    del data_resamples["Timestamp"] 
    from statistics import mode
    mode = lambda x: stats.mode(x)[0] if len(x) > 0 else 'unknown'
    if(city == "ZH"):
        data_resamples_out = data_resamples.resample('60S', how={'PID': 'mean','Time': 'mean','Temp': 'mean','RH': 'mean','Lux': 'mean','Sound': 'mean','Peak': 'sum','Amp': 'mean','EvenName': mode}) 
        #data_resamples_out = data_resamples.resample('60S', how={'PID': 'mean','Time': 'mean','Temp': 'mean','RH': 'mean','Lux': 'mean','Sound': 'mean','TTP_peak': 'sum','TTP_AmpUs': 'mean','CDA_TonicUs': 'mean','EvenName': mode}) 
    else:
        data_resamples_out = data_resamples.resample('60S', how={'PID': 'mean','Time': 'mean','HSTemp': 'mean','HSRH': 'mean','Lux': 'mean','Sound': 'mean','TTP_peak': 'sum','TTP_AmpUs': 'mean','CDA_TonicUs': 'mean','EvenName': mode})       
    
    data_diff_dictionary[i] = data_resamples_out

frames = [data_diff_dictionary[d] for d in data_diff_dictionary]
result = pd.concat(frames)
result.to_csv('merged_data_resample_zscore'+city+'.csv',index = False, header=True)


print('File end')