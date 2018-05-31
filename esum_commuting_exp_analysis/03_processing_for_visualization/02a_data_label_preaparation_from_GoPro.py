# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:11:09 2018

@author: vojha
"""
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
#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_SG")

Round = "01"
file_to_read = "Round_events_"+Round+".csv"
file_event_label =  os.path.join(path_raw_data_files,file_to_read)# fetching sensor  file path
data_event_label = pd.read_csv(file_event_label, usecols = [0,1,2])
data_event_label.columns = ["Event","Date","Time"]


import datetime, time
EvenTimeStamp = []
for i in range(len(data_event_label)):
    if(data_event_label["Event"][i]== 'GPS'):
        #do timestamp computation
        datePlusTimePlusEvent = data_event_label["Date"][i] +" " + data_event_label["Time"][i]
        datePlusTimePlusEvent = dateutil.parser.parse(datePlusTimePlusEvent)
        EvenTimeStamp.append(time.mktime(datePlusTimePlusEvent.timetuple()))
    else:
        #fill with nan
        EvenTimeStamp.append(np.nan)

data_event_label["Timestamp"] = EvenTimeStamp
data_event_label['Timestamp'] = data_event_label['Timestamp'].interpolate(method="linear", axis=0)

from datetime import datetime
ListEvents = []
ListEventsTime = []
for i in range(len(data_event_label)):
    if(data_event_label["Event"][i] != 'GPS'):
        ListEvents.append(data_event_label["Event"][i])
        ListEventsTime.append(data_event_label["Timestamp"][i])
        timerec = datetime.fromtimestamp(int(data_event_label["Timestamp"][i]))
        print(timerec," -> ",data_event_label["Event"][i])

df_label = pd.DataFrame({'A' : []})
df_label["Timestamp"] = ListEventsTime
df_label["Event"] = ListEvents
del df_label["A"]


countWait = 1
countRide = 1
for i in range(len(df_label)):
    if(df_label["Event"][i] == 'GoPro sync'):
        df_label["Event"][i] = "S"
        
    elif(df_label["Event"][i] == 'Arrival at the bus stop'):
        df_label["Event"][i] = "walk"
        
    elif(df_label["Event"][i] == 'Bus boarding'):
        df_label["Event"][i] = "wait"+str(countWait)
        countWait = countWait + 1 
        
    elif(df_label["Event"][i] == 'Bus alighting'):
        df_label["Event"][i] = "ride"+str(countRide)
        countRide = countRide + 1 

    elif(df_label["Event"][i] == 'Answering the questionnaire'):
        df_label["Event"][i] = "walk"
    
    else:
        df_label["Event"][i] = "ignore"
        
df_label = df_label[df_label["Event"] != 'ignore']
df_label = df_label.reset_index(drop=True)

os.chdir(path_raw_data_files)
df_label.to_csv("round_label_"+Round+".csv",index=True)
