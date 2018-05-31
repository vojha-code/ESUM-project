# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 13:00:16 2018

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
from time import mktime
#%%
def make_timestamnp(timedata):
    return mktime(timedata.timetuple())

def convert_from_timestamp(date_in_some_format):
    date_as_string = datetime.datetime.fromtimestamp(date_in_some_format)
    # 10 for ML and 6 for CN
    date_as_string = date_as_string + timedelta(hours=+int(6)) # correction for UTC time difference
    return date_as_string
#%% Processing experiemnt slicing Slicing based on eda tags files labeling journey
def sliceTagsBasedEDAdata(files_sensor, data_eda):
    tag_file =  os.path.join(files_sensor,'tags.csv')
    tag_data = pd.DataFrame.from_csv(tag_file,header=None)
    
    from datetime import datetime
    tag1 = datetime.fromtimestamp(tag_data.index[0]) #t1
    tag2 = datetime.fromtimestamp(tag_data.index[1]) #t2
    tag3 = datetime.fromtimestamp(tag_data.index[2])  #t3
   # tag4= datetime.fromtimestamp(tag_data.index[3])  #t4
   # tag5 = datetime.fromtimestamp(tag_data.index[4])  #t5
   
    #these correction not required for Zurich data for SG +7 and for mellborne +10, for CN 6
    tag1 = tag1 + timedelta(hours=+10)
    tag2 = tag2 + timedelta(hours=+10)
    tag3 = tag3 + timedelta(hours=+10)
   # tag4 = tag4 + timedelta(hours=+7)
    
    timeDiff = 8#+8 for SG data correction for mal +11, 8 SG
    str_eda_date = dateutil.parser.parse(data_eda.index[0].strftime('%Y-%m-%d %H:%M:%S.%f'))
    time_eda_date_str_start = str_eda_date + timedelta(hours=+int(timeDiff))#+8 for SG data correction for mal +11, 8 SG

    str_eda_date = dateutil.parser.parse(data_eda.index[len(data_eda)-1].strftime('%Y-%m-%d %H:%M:%S.%f'))
    time_eda_date_str_end = str_eda_date + timedelta(hours=+int(timeDiff))#+8 for SG data correction +1 for Zh data correction for ml +11
    
    #print for ZH data
#    print("EDA   ",time_eda_date_str_start)
#    print("On    ",tag1,"          ", (tag1 - time_eda_date_str_start))
#    print("Story ",tag2,"          ", (tag2 - tag1))
#    print("Wait  ",tag3,"          ", (tag3 - tag2))
#    print("Walk  ",tag4,"          ", (tag4 - tag3))
#    print("Off   ",tag5,"          ", (tag5- tag4))
#    print("EDA   ",time_eda_date_str_end,"          ", (time_eda_date_str_end- tag5))
    
    #print for SG data
    #print("EDA   ",time_eda_date_str_start)
    #print("On    ",tag1,"          ", (tag1 - time_eda_date_str_start))
    #print("Story ",tag2,"          ", (tag2 - tag1))
    #print("Wait  ",tag3,"          ", (tag3 - tag2))
    #print("Walk  ",tag4,"          ", (tag4- tag3))
    #print("EDA   ",time_eda_date_str_end,"          ", (time_eda_date_str_end- tag4))
    
#    print("EDA   ",time_eda_date_str_start)
#    print("On    ",tag1,"          ", (tag1 - time_eda_date_str_start))
#    print("Story ",tag2,"          ", (tag2 - tag1))
#    print("Wait  ",tag3,"          ", (tag3 - tag2))
#    print("EDA   ",time_eda_date_str_end,"          ", (time_eda_date_str_end- tag3))  
    
    ml = True
    if (ml == True):
        tag3 = tag1
        tag4 = tag2
    
    # correction of data    
    data_gps =  os.path.join(files_sensor,'gps.csv')
    data_gps = pd.DataFrame.from_csv(data_gps)
    tag3 =  datetime.strptime(data_gps['Timestamp'].iloc[0],'%Y-%m-%d %H:%M:%S.%f' )
    tag4 =  datetime.strptime(data_gps['Timestamp'].iloc[len(data_gps)-1],'%Y-%m-%d %H:%M:%S.%f' )

    print("Before")
    print("", time_eda_date_str_start, tag3)
    print("", time_eda_date_str_end, tag4)
        
    
    eda_TimeBoolList = []
    for i in range(len(data_eda)):
        time_str = dateutil.parser.parse(data_eda.index[i].strftime('%Y-%m-%d %H:%M:%S.%f'))
        time_str = time_str + timedelta(hours=+int(timeDiff)) #+8 fro SG data and +1 for ZH data
        if  ((time_str >= tag3) & (time_str <= tag4)):
            booleanTime  = True
        else:
            booleanTime  = False
        eda_TimeBoolList.append(booleanTime)
    
    eda_TimeBoolList.count(False)
    slicedEDAdata = data_eda[eda_TimeBoolList]   
    
    print("After")
    str_eda_date = dateutil.parser.parse(slicedEDAdata.index[0].strftime('%Y-%m-%d %H:%M:%S.%f'))
    time_eda_date_str_start = str_eda_date + timedelta(hours=+int(timeDiff))#+8 for SG data correction for mal +11, 8 SG
    str_eda_date = dateutil.parser.parse(slicedEDAdata.index[len(slicedEDAdata)-1].strftime('%Y-%m-%d %H:%M:%S.%f'))
    time_eda_date_str_end = str_eda_date + timedelta(hours=+int(timeDiff))#+8 for SG data correction +1 for Zh data correction for ml +11
    print("", time_eda_date_str_start, tag3)
    print("", time_eda_date_str_end, tag4)
    
    return slicedEDAdata
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
    if(seconds < (slice_time_window-0.50)):
        sliced_data.loc[sliced_data['event_marker_regular'] == event, 'event_marker_regular'] = 0.0
        #sliced_eda_data.loc[sliced_eda_data['event_marker_regular'] == event, 'EDA'].iloc[0] #only for retriving value
    else:
        event_duration_regular.append(seconds) #appending last event  
        
    if (len(event_duration_regular)==event):
        print('Perfect: ',len(event_duration_regular)," = ",(event))
    else:
        print('Fall short: ',len(event_duration_regular)," != ",(event))
    return sliced_data,event_duration_regular

#%% save regular daya
def save_regular_results(sliced_eda_data,event_duration):
    eda_out_file = os.path.join("EDA_data_"+str(time_window)+"s_marked.csv")
    eda_out_file1 =  os.path.join("Marker_"+str(time_window)+"s_"+str(participant)+".txt")
    eda_out_file2 =  os.path.join("Event_duration_"+str(time_window)+"s_"+str(participant)+".txt")

    list1 = sliced_eda_data["regular_time"].tolist()
    list2 = sliced_eda_data["EDA"].tolist()
    list3 = sliced_eda_data["event_marker_regular"].tolist()
    eda_data_out = list(zip(list1,list2,list3))
    
    sliced_eda_data.to_csv(eda_out_file)
    np.savetxt(eda_out_file1, eda_data_out, delimiter="\t", fmt='%s')
    np.savetxt(eda_out_file2, event_duration, delimiter="\n", fmt='%s')

#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
#path_raw_data_files = os.path.join(path_raw_data_files, "Data_ZH")#Data_ZH
#path_raw_data_files = os.path.join(path_raw_data_files, "Data_SG")#Data_ZH
#path_raw_data_files = os.path.join(path_raw_data_files, "Data_ML")#
#path_raw_data_files = os.path.join(path_raw_data_files, "Data_CN")#
path_raw_data_files = os.path.join(path_raw_data_files, "Data_HK")#

# set participant
participant = "04"
filepath_sensors = os.path.join(path_raw_data_files, participant) # looking specific participant folders
files_sensor = os.path.join(filepath_sensors,"processed")

os.chdir(files_sensor)

file_eda =  os.path.join(files_sensor,'EDA.csv')

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

#%%slice experimed time of the eda data
data_eda = sliceTagsBasedEDAdata(files_sensor, data_eda)

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
    
save_regular_results(marked_eda_data,event_duration_regular)

#%%
print("End of slicing data")