# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 17:01:13 2018

@author: vojha
"""
#Reset all varables
%reset -f
%clear

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
#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
city = "ZH"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_"+city)
path_raw_data_files = os.path.join(path_raw_data_files,"compiled_data")

os.chdir(path_raw_data_files)
#%%
ZH = [2,3,4,5,6,7,8,9,10]
CN = [3,6]
HK = [4]
ML = [1,4]

if(city == "ZH"):
    labelcity = ZH # change it
elif(city == "CN"):
    labelcity = CN # change it
elif(city == "HK"):
    labelcity = HK # change it
else:
    labelcity = ML # change it

    
for pid in labelcity:
    #pid = 1
    participant_int = pid
    
    #read data
    file_label_to_read = "l"+str(participant_int)+".csv"
    #file_data_to_read = "fused_data_"+str(participant_int)+".csv"
    file_data_to_read = "fused_data_zScore"+str(participant_int)+".csv"
    
    data_label = pd.read_csv(file_label_to_read,header=None)
    data_label.columns = ['Date', 'Time','EventTime','Event'] # renaming the columns
    data_participant = pd.read_csv(file_data_to_read)
    data_participant = data_participant.drop(['Unnamed: 0'], axis=1)
    # Compare time
    import datetime, time
    EvenTimeStamp = []
    for i in range(len(data_label)):
        datePlusTimePlusEvent = data_label["Date"][i] +" " + data_label["Time"][i]
        datePlusTimePlusEvent = dateutil.parser.parse(datePlusTimePlusEvent)
        datePlusTimePlusEvent =  datePlusTimePlusEvent + timedelta(minutes=+data_label["EventTime"][i])
        EvenTimeStamp.append(time.mktime(datePlusTimePlusEvent.timetuple()))
    
    data_label["Timestamp"] =  EvenTimeStamp

    #create labels for time
    labellist = []
    j = 0
    for i in range(len(data_participant)):
        if(data_participant["Time"][i] < data_label["Timestamp"][j]):
            print(i," :",data_label["Event"][j])
            labellist.append(data_label["Event"][j])
        else:
            if(j < len(data_label)-1):
                print(j)    
                print(i," :",data_label["Event"][j])
                labellist.append(data_label["Event"][j])
                
                j = j + 1#increase pointer of label dataframe
                #i = i - 1#decrease pointer of i to came back to previous palce
            else:
                print(i," : unknown")
                labellist.append("unknown")
    
    data_participant["EvenName"]  = labellist
    
    data_participant.to_csv(file_data_to_read)
