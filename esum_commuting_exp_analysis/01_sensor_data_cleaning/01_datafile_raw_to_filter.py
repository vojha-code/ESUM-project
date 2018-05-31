# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 13:19:01 2018

@author: vojha
"""
#%%importing packages
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
from io import StringIO
#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"

timeof = 'CN' # Singapore, Hong Kong, and Shenzhen have the same time 
city = 'ML'
daylightSavingDiff = 2 #1 for winder (dayLisght saving) is on 2 for  summer

files_all_sensor = path_raw_data_files+"/Data_"+city
#%%
if( city == 'ZH'):
    #for ZH data only
    timeDiff = 1 #correction for UTC data
    timeDelta = 0 #correction for UTC data
else:
    # for singapore
    timeDiff = 8 #correction for UTC data
    timeDelta = timeDiff - daylightSavingDiff  #correction for UTC data
    if (city == 'ML'):
        timeDiff = 11 #correction for UTC data to mallbone time
        timeDelta = timeDiff - daylightSavingDiff  #correction for UTC data  
        if(timeof == 'CN'):
            timeDiff = 8  #correction for UTC data
            timeDelta = timeDiff - daylightSavingDiff  #correction for UTC data
            

#%% set participant
participant = "04"
filepath_sensors = os.path.join(files_all_sensor, participant) # looking specific participant folders
#Check Sensor file working? and ghave to be proceesed
sensor_EDA = "Yes"
sensor_hobo = "No"
sensor_heat = "Yes"
sensor_sound = "No"
sensor_dust = "NO"
sensor_gps = "Yes"
#%% hobo sensor data reading
if(sensor_hobo == "Yes"):
    file_hobo_sensor =  os.path.join(filepath_sensors,'hobo.csv')# fetching sensor  file path
    if( city == 'ZH'):
        #for ZH data only
        data_hobo_sesnor = pd.read_csv(file_hobo_sensor,  index_col=[0], skiprows=1)
    else:
        #for SG data only
        data_hobo_sesnor = pd.read_csv(file_hobo_sensor,  index_col=[0], skiprows=1)
        hobo_old_names = (data_hobo_sesnor.columns).tolist()#for SG data only
        data_hobo_sesnor = data_hobo_sesnor.drop([hobo_old_names[4]], axis=1)#for SG data only
        data_hobo_sesnor = data_hobo_sesnor.drop([hobo_old_names[5]], axis=1)#for SG data only
        if( city == 'ML' and timeof == 'ML'):
            data_hobo_sesnor = data_hobo_sesnor.drop([hobo_old_names[6]], axis=1)#for ML data only
        
    data_hobo_sesnor.columns = ['Timestamp', 'Temp','RH','Lux'] # renaming the columns
    print("OK: Hobo ")
else:
    print("Missing: Hobo")    
    
# Sound sensor
if(sensor_sound == "Yes"):
    file_sound_sensor =  os.path.join(filepath_sensors,'sound.xls')# fetching sensor  file path
    data_sound_sesnor = pd.read_csv(file_sound_sensor, sep = '	', index_col=[0], skiprows=range(0, 5), error_bad_lines=False) #retiriving the data as dataframe
    data_sound_sesnor.columns = ['Sound', 'Unit','Timestamp','Other'] # renaming the columns
    data_sound_sesnor = data_sound_sesnor[['Timestamp', 'Sound']]#featching columns
    print("OK: Sound ")
else:
    print("Missing: sound")
    
# GPS sensor
if(sensor_gps == "Yes"):
    file_gps_sensor =  os.path.join(filepath_sensors,'GPS.csv')# fetching sensor  file path
    if(city == 'ML'):
        data_gps_sesnor = pd.read_csv(file_gps_sensor,  index_col= None, skiprows=1, header= None, usecols = [16,17,21],  error_bad_lines=False) #retiriving the data as dataframe    
        data_gps_sesnor = data_gps_sesnor.dropna(axis=0, how='all')
    else:
        data_gps_sesnor = pd.read_csv(file_gps_sensor,  index_col= None, skiprows=0, header= None, usecols = [0,13,15],  error_bad_lines=False) #retiriving the data as dataframe    
    
    data_gps_sesnor.columns =['LAT', 'LON','Timestamp']
    data_gps_sesnor = data_gps_sesnor.fillna(0)
    print("OK: GPS ")
else:
    print("Missing: GPS")

# dust sensor file filterining
if(sensor_dust == "Yes"):
    file_dust_sensor =  os.path.join(filepath_sensors,'dust.csv')# fetching sensor  file path
    data_dust_sesnor = pd.read_csv(file_dust_sensor, skiprows=range(0, 19), error_bad_lines=False) #retiriving the data as dataframe
    data_dust_sesnor = data_dust_sesnor[['OADateTime', 'PM1(ug/m3)', 'PM2.5(ug/m3)', 'PM10(ug/m3)', 'RollMean_PM1', 'RollMean_PM2.5', 'RollMean_PM10']]#featching columns
    data_dust_sesnor.columns = ['Timestamp', 'PM1', 'PM2p5', 'PM10', 'RollMean_PM1', 'RollMean_PM2p5', 'RollMean_PM10']#featching columns
    print("OK: Dust ")
else:
    print("Missing: Dust ")
    
# heat sensor file filterining ONLY for SG data
if(sensor_heat == "Yes"):
    file_heat_sensor =  os.path.join(filepath_sensors,'heat.csv')# fetching sensor  file path
    cols = [i for i in range(0,9) if i not in [1,3,4,7]]
    data_heat_sesnor = pd.read_csv(file_heat_sensor,  index_col=None, skiprows=[0,1,2,4], usecols = cols, error_bad_lines=False) #retiriving the data as dataframe
    heat_old_names = (data_heat_sesnor.columns).tolist()
    data_heat_sesnor.rename(columns={heat_old_names[0]: 'Timestamp'}, inplace=True)
    heat_new_names = (data_heat_sesnor.columns).tolist()
    data_heat_sesnor[heat_new_names] = data_heat_sesnor[heat_new_names].replace("***", np.nan)
    data_heat_sesnor = data_heat_sesnor.fillna(0)
    print("OK: Heat ")
else:
    print("Missing: Heat ")
    
#EDA file
if(sensor_EDA == "Yes"):
    # retiving EDA file
    file_eda =  os.path.join(filepath_sensors,'EDA.csv')
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
    print("OK: EDA ")
else:
    print("Missing: EDA :  Now forward if EDA data missing!")
#%% data time parsers
def convert_from_timestamp(date_in_some_format):
    date_as_string = datetime.datetime.fromtimestamp(date_in_some_format)
    # 10 for ML and 6 for CN
    date_as_string = date_as_string + timedelta(hours=+int(timeDelta)) # correction for UTC time difference
    return date_as_string

#data time parsers with correction of time
def convert_to_timestamp_correction(date_in_some_format):
    date_as_string = dateutil.parser.parse(date_in_some_format)
    date_as_string = date_as_string + timedelta(hours=+int(3)) # correction for UTC time difference 3 here was 
    return date_as_string

# data time parsers
def convert_to_timestamp(date_in_some_format):
    date_as_string = dateutil.parser.parse(date_in_some_format)
    return date_as_string

# correction for time
import datetime
OLE_TIME_ZERO = datetime.datetime(1899, 12, 30, 0, 0, 0)
def ole2datetime(oledt):
    return OLE_TIME_ZERO + datetime.timedelta(days=float(oledt)) 

# gps time correction
def gps_time_correction(gps_time):
    gps_sesnor_str = gps_time.replace("_","-")
    index = 10
    char = ' '
    gps_sesnor_str = gps_sesnor_str[:index] + char + gps_sesnor_str[index + 1:]
    char = ':'
    gps_sesnor_str = gps_sesnor_str[:13] + char + gps_sesnor_str[13 + 1:]
    gps_sesnor_str = gps_sesnor_str[:16] + char + gps_sesnor_str[16 + 1:]
    gps_sesnor_str = gps_sesnor_str[:19] + '.' + gps_sesnor_str[19 + 1:]
    correct_gps_time = dateutil.parser.parse(gps_sesnor_str)
    #correct_gps_time = correct_gps_time + timedelta(hours=-1)
    return correct_gps_time
#%% Timestap unifier
# Hobo
if(sensor_hobo == "Yes"):
    data_hobo_sesnor['Timestamp'] = data_hobo_sesnor['Timestamp'].apply(convert_to_timestamp)

# Heat
if(sensor_heat == "Yes"):
    # heat only ZH and heat only SG
    data_heat_sesnor['Timestamp'] = data_heat_sesnor['Timestamp'].apply(convert_to_timestamp)
    #data_heat_sesnor['Timestamp'] = data_heat_sesnor['Timestamp'].apply(convert_to_timestamp_correction)

# Sound    
if(sensor_sound == "Yes"):
    data_sound_sesnor['Timestamp'] = data_sound_sesnor['Timestamp'].apply(convert_to_timestamp)

# Dust
if(sensor_dust == "Yes"):
    data_dust_sesnor['Timestamp'] = data_dust_sesnor['Timestamp'].apply(ole2datetime)

# GPS
if(sensor_gps == "Yes"):
    if(city == 'ML'):
        data_gps_sesnor['Timestamp'] = data_gps_sesnor['Timestamp'].apply(convert_from_timestamp)
    else:
        data_gps_sesnor['Timestamp'] = data_gps_sesnor['Timestamp'].apply(gps_time_correction)
#%% Check time: raw times of the seor recording
print("Sensor recording time:")
if(sensor_EDA == "Yes"):
    # +1 for ZH and +8 for SG
    time_eda_date_str = dateutil.parser.parse(data_eda.index[0].strftime('%Y-%m-%d %H:%M:%S.%f'))
    time_eda_date_str_start = time_eda_date_str + timedelta(hours=+int(timeDiff)) # correction for UK time difference
    eda_timetuple = time_eda_date_str_start.timetuple()
    
    # +1 for ZH and +8 for SG
    time_eda_date_str = dateutil.parser.parse(data_eda.index[len(data_eda)-1].strftime('%Y-%m-%d %H:%M:%S.%f'))
    time_eda_date_str_end = time_eda_date_str + timedelta(hours=+int(timeDiff)) # correction for UK time difference
    eda_timetuple = time_eda_date_str_end.timetuple()
    print("EDA:   ",time_eda_date_str_start, time_eda_date_str_end)
    
# Hobo
if(sensor_hobo == "Yes"):
    time_hobo_date_str_start = data_hobo_sesnor['Timestamp'].iloc[0]
    time_hobo_date_str_end = data_hobo_sesnor['Timestamp'].iloc[len(data_hobo_sesnor)-1]
    print("Hobo:  ",time_hobo_date_str_start, time_hobo_date_str_end)
# heat
if(sensor_heat == "Yes"):
    time_heat_date_str_start = data_heat_sesnor['Timestamp'].iloc[0]
    time_heat_date_str_end = data_heat_sesnor['Timestamp'].iloc[len(data_heat_sesnor)-1]
    print("Heat:  ",time_heat_date_str_start, time_heat_date_str_end)
# Sound
if(sensor_sound == "Yes"):
    time_sound_date_str_start = data_sound_sesnor['Timestamp'].iloc[0]
    time_sound_date_str_end = data_sound_sesnor['Timestamp'].iloc[len(data_sound_sesnor)-1]
    print("Sound: ",time_sound_date_str_start, time_sound_date_str_end)
# Dust
if(sensor_dust == "Yes"):
    time_dust_date_str_start = data_dust_sesnor['Timestamp'].iloc[0]
    time_dust_date_str_end = data_dust_sesnor['Timestamp'].iloc[len(data_dust_sesnor)-1]
    print("Dust:  ",time_dust_date_str_start, time_dust_date_str_end)

# GPS
if(sensor_gps == "Yes"):
    time_gps_date_str_start = data_gps_sesnor['Timestamp'].iloc[0]
    time_gps_date_str_end = data_gps_sesnor['Timestamp'].iloc[len(data_gps_sesnor)-1]
    print("GPS:   ",time_gps_date_str_start, time_gps_date_str_end)
    
#%% Slicing data based on EDA time Stamp information only processed files
# Hobo
if(sensor_hobo == "Yes"):
    data_sliced_hobo = data_hobo_sesnor[(data_hobo_sesnor['Timestamp'] >= time_eda_date_str_start) & (data_hobo_sesnor['Timestamp'] <= time_eda_date_str_end)]

# heat
if(sensor_heat == "Yes"):
    data_sliced_heat = data_heat_sesnor[(data_heat_sesnor['Timestamp'] >= time_eda_date_str_start) & (data_heat_sesnor['Timestamp'] <= time_eda_date_str_end)]    

# Sound
if(sensor_sound == "Yes"):
    data_sliced_sound = data_sound_sesnor[(data_sound_sesnor['Timestamp'] >= time_eda_date_str_start) & (data_sound_sesnor['Timestamp'] <= time_eda_date_str_end)]    

# Dust
if(sensor_dust == "Yes"):
    data_sliced_dust = data_dust_sesnor[(data_dust_sesnor['Timestamp'] >= time_eda_date_str_start) & (data_dust_sesnor['Timestamp'] <= time_eda_date_str_end)]    

# GPS
if(sensor_gps == "Yes"):
    data_sliced_gps = data_gps_sesnor[(data_gps_sesnor['Timestamp'] >= time_eda_date_str_start) & (data_gps_sesnor['Timestamp'] <= time_eda_date_str_end)]    
    #print("Check Seros IN gps",len(data_sliced_gps[data_sliced_gps["LAT"]==0]))
#%% Saving only cleaned files
#save_filepath_clean = os.path.join(filepath_sensors,"cleaned")
#if not os.path.exists(save_filepath_clean):
#    os.makedirs(save_filepath_clean)
#
#data_sliced_hobo.to_csv(os.path.join(save_filepath_clean,"hobo.csv"))
#data_sliced_sound.to_csv(os.path.join(save_filepath_clean,"sound.csv"))
##data_sliced_dust.to_csv(os.path.join(save_filepath_clean,"dust.csv"))
#data_sliced_gps.to_csv(os.path.join(save_filepath_clean,"gps.csv"))
#data_sliced_heat.to_csv(os.path.join(save_filepath_clean,"heat.csv"))
#%% Check time of the data files again
print("Actual EDA recording time:")
#EDA file
if(sensor_EDA == "Yes"):
    print("EDA:   ",time_eda_date_str_start, time_eda_date_str_end)
    
# Hobo
if(sensor_hobo == "Yes"):
    time_hobo_date_str_start = data_sliced_hobo['Timestamp'].iloc[0]
    time_hobo_date_str_end = data_sliced_hobo['Timestamp'].iloc[len(data_sliced_hobo)-1]
    print("Hobo:  ",time_hobo_date_str_start, time_hobo_date_str_end)
    
# heat
if(sensor_heat == "Yes"):
    time_heat_date_str_start = data_sliced_heat['Timestamp'].iloc[0]
    time_heat_date_str_end = data_sliced_heat['Timestamp'].iloc[len(data_sliced_heat)-1]
    print("Heat:  ",time_heat_date_str_start, time_heat_date_str_end)
    
# Sound
if(sensor_sound == "Yes"):
    time_sound_date_str_start = data_sliced_sound['Timestamp'].iloc[0]
    time_sound_date_str_end = data_sliced_sound['Timestamp'].iloc[len(data_sliced_sound)-1]
    print("Sound: ",time_sound_date_str_start, time_sound_date_str_end)

# Dust
if(sensor_dust == "Yes"):
    time_dust_date_str_start = data_sliced_dust['Timestamp'].iloc[0]
    time_dust_date_str_end = data_sliced_dust['Timestamp'].iloc[len(data_sliced_dust)-1]
    print("Dust:  ",time_dust_date_str_start, time_dust_date_str_end)    
# GPS
if(sensor_gps == "Yes"):
    time_gps_date_str_start = data_sliced_gps['Timestamp'].iloc[0]
    time_gps_date_str_end = data_sliced_gps['Timestamp'].iloc[len(data_sliced_gps)-1]
    print("GPS:   ",time_gps_date_str_start, time_gps_date_str_end)
#%% Processing experiemnt slicing Slicing based on eda tags files labeling journey
tag_file =  os.path.join(filepath_sensors,'tags.csv')
tag_data = pd.DataFrame.from_csv(tag_file,header=None)

from datetime import datetime

tag1 = datetime.fromtimestamp(tag_data.index[0])  #t1
tag2 = datetime.fromtimestamp(tag_data.index[1])  #t2
tag3 = datetime.fromtimestamp(tag_data.index[2])  #t3
if( city == 'ML'):
    print('tag: Men Not at work')
else:    
    tag4 = datetime.fromtimestamp(tag_data.index[3])  #t4
if( city == 'ZH'):
    #tag 5 is not avialble in SG data do I make it off
    tag5 = datetime.fromtimestamp(tag_data.index[4])  #t5

# time delta for ZH is 1 and SG data is 7
tag1 = tag1 + timedelta(hours=+int(timeDelta))
tag2 = tag2 + timedelta(hours=+int(timeDelta))
tag3 = tag3 + timedelta(hours=+int(timeDelta))
if( city == 'ML'):
    print('tag: Men Not at work')
else:    
    tag4 = tag4 + timedelta(hours=+int(timeDelta))
if( city == 'ZH'):
    #tag 5 is not avialble in SG data do I make it off
    tag5 = tag5 + timedelta(hours=+int(timeDelta))
    

if( city == 'ZH'):
    #print for ZH data
    print("EDA   ",time_eda_date_str_start)
    print("On    ",tag1,"          ", (tag1 - time_eda_date_str_start))
    print("Story ",tag2,"          ", (tag2 - tag1))
    print("wait  ",tag3,"          ", (tag3 - tag2))
    print("walk  ",tag4,"          ", (tag4- tag3))
    print("Off   ",tag5,"          ", (tag5- tag4))
    print("EDA   ",time_eda_date_str_end,"          ", (time_eda_date_str_end- tag5))
if( city == 'SG'):
    #print for SG data
    print("EDA   ",time_eda_date_str_start)
    print("On    ",tag1,"          ", (tag1 - time_eda_date_str_start))
    print("Story ",tag2,"          ", (tag2 - tag1))
    print("Wait  ",tag3,"          ", (tag3 - tag2))
    print("Walk  ",tag4,"          ", (tag4- tag3))
    print("EDA   ",time_eda_date_str_end,"          ", (time_eda_date_str_end- tag4))
else:    
    #print for ML data 
    print("EDA   ",time_eda_date_str_start)
    print("On    ",tag1,"          ", (tag1 - time_eda_date_str_start))
    print("Story ",tag2,"          ", (tag2 - tag1))
    print("Wait  ",tag3,"          ", (tag3 - tag2))
    print("EDA   ",time_eda_date_str_end,"          ", (time_eda_date_str_end- tag3))    
#%% Slicing data based on EDA time Stamp information only processed files
if( city == 'ML'):
    if ((participant == "03") or (participant == "04")  or (participant == "05")):
        tag4 = time_eda_date_str_end
        tag3 = tag2
    else:
        tag3 = tag1
        tag4 = tag2

if(timeof == "CN"):
    tag3 = data_sliced_gps['Timestamp'].iloc[0]
    tag4 = data_sliced_gps['Timestamp'].iloc[len(data_sliced_gps)-1]

# Hobo
if(sensor_hobo == "Yes"):
    data_sliced_hobo = data_hobo_sesnor[(data_hobo_sesnor['Timestamp'] >= tag3) & (data_hobo_sesnor['Timestamp'] <= tag4)]
# heat
if(sensor_heat == "Yes"):
    data_sliced_heat = data_sliced_heat[(data_sliced_heat['Timestamp'] >= tag3) & (data_sliced_heat['Timestamp'] <= tag4)]    
# Sound
if(sensor_sound == "Yes"):
    data_sliced_sound = data_sound_sesnor[(data_sound_sesnor['Timestamp'] >= tag3) & (data_sound_sesnor['Timestamp'] <= tag4)]    
# Dust
if(sensor_dust == "Yes"):
    data_sliced_dust = data_dust_sesnor[(data_dust_sesnor['Timestamp'] >= tag3) & (data_dust_sesnor['Timestamp'] <= tag4)]    
# GPS
if(sensor_gps == "Yes"):
    data_sliced_gps = data_gps_sesnor[(data_gps_sesnor['Timestamp'] >= tag3) & (data_gps_sesnor['Timestamp'] <= tag4)]    
#%% Check time of the data files again
print("Actual experiment time:")
if(sensor_EDA == "Yes"):
    # +1 for ZH and +8 for SG
    print("EDA:   ",tag3, tag4)
        
# Hobo
if(sensor_hobo == "Yes"):
    time_hobo_date_str_start = data_sliced_hobo['Timestamp'].iloc[0]
    time_hobo_date_str_end = data_sliced_hobo['Timestamp'].iloc[len(data_sliced_hobo)-1]
    print("Hobo:  ",time_hobo_date_str_start, time_hobo_date_str_end)
# heat
if(sensor_heat == "Yes"):
    time_heat_date_str_start = data_sliced_heat['Timestamp'].iloc[0]
    time_heat_date_str_end = data_sliced_heat['Timestamp'].iloc[len(data_sliced_heat)-1]
    print("Heat:  ",time_heat_date_str_start, time_heat_date_str_end)
# Sound
if(sensor_sound == "Yes"):
    time_sound_date_str_start = data_sliced_sound['Timestamp'].iloc[0]
    time_sound_date_str_end = data_sliced_sound['Timestamp'].iloc[len(data_sliced_sound)-1]
    print("Sound: ",time_sound_date_str_start, time_sound_date_str_end)
# Dust
if(sensor_dust == "Yes"):
    time_dust_date_str_start = data_sliced_dust['Timestamp'].iloc[0]
    time_dust_date_str_end = data_sliced_dust['Timestamp'].iloc[len(data_sliced_dust)-1]
    print("Dust:  ",time_dust_date_str_start,time_dust_date_str_end)
# GPS
if(sensor_gps == "Yes"):
    time_gps_date_str_start = data_sliced_gps['Timestamp'].iloc[0]
    time_gps_date_str_end = data_sliced_gps['Timestamp'].iloc[len(data_sliced_gps)-1]
    print("GPS:   ",time_gps_date_str_start, time_gps_date_str_end)
#%% Saving only processed files
save_filepath_proccesed = os.path.join(filepath_sensors,"processed")
if not os.path.exists(save_filepath_proccesed):
    os.makedirs(save_filepath_proccesed)

#EDA file
if(sensor_EDA == "Yes"):
    (pd.DataFrame.from_csv(os.path.join(filepath_sensors,'EDA.csv'))).to_csv(os.path.join(save_filepath_proccesed,"EDA.csv"))
    (pd.DataFrame.from_csv(os.path.join(filepath_sensors,'tags.csv'))).to_csv(os.path.join(save_filepath_proccesed,"tags.csv"))

# Hobo
if(sensor_hobo == "Yes"):
    data_sliced_hobo = data_sliced_hobo.reset_index(drop=True)
    data_sliced_hobo.to_csv(os.path.join(save_filepath_proccesed,"hobo.csv"))

# heat
if(sensor_heat == "Yes"):
    data_sliced_heat.to_csv(os.path.join(save_filepath_proccesed,"heat.csv"))
# Sound
if(sensor_sound == "Yes"):
    data_sliced_sound.to_csv(os.path.join(save_filepath_proccesed,"sound.csv"))
# Dust
if(sensor_dust == "Yes"):
    data_sliced_dust.to_csv(os.path.join(save_filepath_proccesed,"dust.csv"))
# GPS
if(sensor_gps == "Yes"):
    data_sliced_gps.to_csv(os.path.join(save_filepath_proccesed,"gps.csv"))
#%%
print("End of file")