# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 14:38:41 2018

@author: vojha
"""
%reset -f
%clear

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
#%%
def eda_data_processing(file_eda, str_pid):
    # EDA Variables 
    list_of_columns_eda = ["EDA"]
    #expected_sample_rate_eda = 4
    #freq_eda = "250L"
    
    #Feteching data
    # Load data
    data_eda = pd.DataFrame.from_csv(file_eda)
    data_eda.reset_index(inplace=True)
    
    # Get the startTime and sample rate
    startTime = pd.to_datetime(float(data_eda.columns.values[0]),unit="s")
    sampleRate = float(data_eda.iloc[0][0]) #retriving sample rate
    data_eda = data_eda[data_eda.index!=0] #reindexing eda dataframe
    data_eda.index = data_eda.index-1 #reindexing eda dataframe
    
    
    # Reset the data frame assuming expected_sample_rate
    data_eda.columns = list_of_columns_eda # Changing column Name 
    #perform upsampling
    data_eda.index = pd.DatetimeIndex(start=startTime,periods = len(data_eda),freq='250L')
    #data_eda["timestamp"] = data_eda.index 
    
    #creating only seconds list
    secondslist = np.zeros(len(data_eda))
    seconds = 0.000
    for i in range(len(secondslist)):
        secondslist[i] = seconds
        seconds += 0.250 # for 4Hz  
    data_eda["time"] = secondslist
    
    #initializing marker
    marker = np.empty(len(data_eda))
    marker.fill(-1)
    
    data_eda["event_marker_regular"] = np.zeros(len(data_eda))
    
    slice_time_window = 5.000 # rate of windo slicing for pattern analysis
    
    time_window = int(slice_time_window)
    marked_eda_data,event_duration_regular =  create_regular_marker(data_eda,slice_time_window)

    #creating only seconds list
    secondslist = np.zeros(len(marked_eda_data))
    seconds = 0.000
    for j in range(len(secondslist)):
        secondslist[j] = seconds
        seconds += 0.250 # for 4Hz  
    marked_eda_data["regular_time"] = secondslist
        
    save_regular_results(str_pid,marked_eda_data,event_duration_regular,time_window)
#%% marke regular interval
def create_regular_marker(sliced_data,interval):    
    event = 1
    event_duration_regular = []
    sliced_data["event_marker_regular"][0] = event
    seconds = 0.000
    for i in range(len(sliced_data)):
        if (seconds == interval):
            event_duration_regular.append(seconds)
            event += 1
            sliced_data["event_marker_regular"][i]= event
            seconds = 0.000   
        seconds += 0.250 # for 4Hz 
    
    # append last even only if it is about "seconds == slice_time_window"   
    if(seconds < (interval-0.50)):
        sliced_data.loc[sliced_data['event_marker_regular'] == event, 'event_marker_regular'] = 0.0
        #sliced_eda_data.loc[sliced_eda_data['event_marker_regular'] == event, 'EDA'].iloc[0] #only for retriving value
    else:
        event_duration_regular.append(seconds) #appending last event  
        
    if (len(event_duration_regular)==event):
        print('Perfect: ',len(event_duration_regular)," = ",(event))
    else:
        print('Fall short: ',len(event_duration_regular)," != ",(event))
    return sliced_data,event_duration_regular
#%% Saving data
def save_regular_results(pid,sliced_eda_data,event_duration,time_window):
    eda_out_file0 = os.path.join("EDA_data_"+str(time_window)+"s_marked_"+str(pid)+".csv")
    eda_out_file1 =  os.path.join("Marker_"+str(time_window)+"s_"+str(pid)+".txt")
    eda_out_file2 =  os.path.join("Event_duration_"+str(time_window)+"s_"+str(pid)+".txt")

    list1 = sliced_eda_data["regular_time"].tolist()
    list2 = sliced_eda_data["EDA"].tolist()
    list3 = sliced_eda_data["event_marker_regular"].tolist()
    eda_data_out = list(zip(list1,list2,list3))
    
    sliced_eda_data.to_csv(eda_out_file0)
    np.savetxt(eda_out_file1, eda_data_out, delimiter="\t", fmt='%s')
    np.savetxt(eda_out_file2, event_duration, delimiter="\n", fmt='%s')

#%% retrive data
#EDA = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_Block\processed","EDA")
#markedEDA = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_Block\processed","markedEDA")

EDA = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_Block\processed","EDA")
markedEDA = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_Block\processed","markedEDA")
#%% porcessing
os.chdir(markedEDA)
listEDAs = os.listdir(EDA)

pid = 1
for files in listEDAs:
    if(pid < 10):
        str_pid = "0"+str(pid)
    else:
        str_pid = str(pid)
    print("",str_pid,files)
    
    #data_eda = pd.DataFrame.from_csv(os.path.join(EDA,files))
    eda_data_processing(os.path.join(EDA,files), str_pid)
    pid = pid + 1