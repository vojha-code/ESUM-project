# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 13:00:16 2018

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



#from IPython import get_ipython
#def __reset__(): get_ipython().magic('reset -sf')
#def clear_all():
#    """Clears all the variables from the workspace of the spyder application."""
#    gl = globals().copy()
#    for var in gl:
#        if var[0] == '_': continue
#        if 'func' in str(globals()[var]): continue
#        if 'module' in str(globals()[var]): continue
#
#        del globals()[var]
##%%        
##if __name__ == "__main__":
#clear_all()
#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
city = ""
#path_raw_data_files = os.path.join(path_raw_data_files, "Data_ZH")
#path_raw_data_files = os.path.join(path_raw_data_files, "Data_SG")
#path_raw_data_files = os.path.join(path_raw_data_files, "Data_ML")
#path_raw_data_files = os.path.join(path_raw_data_files, "Data_CN")
path_raw_data_files = os.path.join(path_raw_data_files, "Data_HK")
# set participant

# for 8 time is miss be few seconds in this algorithms
participant_int = 4

if (participant_int<10):
    participant = "0"+str(participant_int)
else:
    participant = ""+str(participant_int)
    
path_all_sensor_files = os.path.join(path_raw_data_files, participant) # looking specific participant folders
file_all_sensors = os.path.join(path_all_sensor_files,"processed")

#Check Sensor file working? and ghave to be proceesed
sensor_EDA = "Yes"
sensor_hobo = "No"
sensor_heat = "Yes"
sensor_sound = "No"
sensor_dust = "NO"
sensor_gps = "Yes"
#%% #GPS data retirvel
# Hobo
if(sensor_hobo == "Yes"):
    file_hobo_sensor =  os.path.join(file_all_sensors,'hobo.csv')# fetching sensor  file path
    data_hobo_sesnor = pd.read_csv(file_hobo_sensor)
    data_hobo_sesnor = data_hobo_sesnor.drop(['Unnamed: 0'], axis=1)
    print("OK: Hobo ")

# heat
if(sensor_heat == "Yes"):
    file_heat_sensor = os.path.join(file_all_sensors,'heat.csv')# fetching sensor  file path
    data_heat_sesnor = pd.read_csv(file_heat_sensor) #retiriving the data as dataframe
    data_heat_sesnor = data_heat_sesnor.drop(['Unnamed: 0'], axis=1)
    print("OK: Heat ")
# Sound
if(sensor_sound == "Yes"):
    file_sound_sensor =  os.path.join(file_all_sensors,'sound.csv')# fetching sensor  file path
    data_sound_sesnor = pd.read_csv(file_sound_sensor) #retiriving the data as dataframe
    data_sound_sesnor = data_sound_sesnor.drop(['NO'], axis=1)
    print("OK: Sound ")
# Dust
if(sensor_dust == "Yes"):
    file_dust_sensor = os.path.join(file_all_sensors,'dust.csv')# fetching sensor  file path
    data_dust_sesnor = pd.read_csv(file_dust_sensor) #retiriving the data as dataframe
    data_dust_sesnor = data_dust_sesnor.drop(['Unnamed: 0'], axis=1)
    print("OK: Dust ")

# GPS
if(sensor_gps == "Yes"):
    file_gps_sensor =  os.path.join(file_all_sensors,'gps.csv')# fetching sensor  file path
    data_gps_sensor = pd.read_csv(file_gps_sensor)
    data_gps_sensor = data_gps_sensor.drop(['Unnamed: 0'], axis=1)
    print("OK: GPS ")

#EDA file
if(sensor_EDA == "Yes"):
    file_eda_marked =  os.path.join(file_all_sensors,'EDA_data_5s_marked.csv')# fetching sensor  file path
    data_eda_marked = pd.read_csv(file_eda_marked)
    data_eda_marked.rename(columns={'Unnamed: 0': 'Timestamp'}, inplace=True)
    print("OK: EDA ")
else:
    print("Missing: EDA :  Now forward if EDA data missing!")
#%% ledalab proces data
path_ledalab_files = os.path.join(path_raw_data_files, "ledalab_data_0p01ms")
#path_ledalab_files =  os.path.join(path_ledalab_files, "5seconds")
nscr_file_name = "Results_exp_"+str(participant_int)+".xls"
file_ledalab_files =  os.path.join(path_ledalab_files,nscr_file_name)# fetching sensor  file path
data_leda_nscr0p01 = pd.read_excel(file_ledalab_files,sheetname='ERA')

path_ledalab_files = os.path.join(path_raw_data_files, "ledalab_data_0p05ms")
#path_ledalab_files =  os.path.join(path_ledalab_files, "5seconds")
#nscr_file_name = "Results_exp_"+str(participant_int)+".xls"
file_ledalab_files =  os.path.join(path_ledalab_files,nscr_file_name)# fetching sensor  file path
data_leda_nscr0p05 = pd.read_excel(file_ledalab_files,sheetname='ERA')


path_ledalab_files = os.path.join(path_raw_data_files, "ledalab_data_0p1ms")
#path_ledalab_files =  os.path.join(path_ledalab_files, "5seconds")
#nscr_file_name = "Results_exp_"+str(participant_int)+".xls"
file_ledalab_files =  os.path.join(path_ledalab_files,nscr_file_name)# fetching sensor  file path
data_leda_nscr0p1 = pd.read_excel(file_ledalab_files,sheetname='ERA')
#%% Compute for every 5 second
data_eda_marked = data_eda_marked.set_index(pd.DatetimeIndex(data_eda_marked['Timestamp']))
#print(data_eda_marked.index[0])
#print(data_eda_marked.index+pd.to_timedelta(1, unit='h'))

'''
 1  for ZH 
 8  for SG,CN  
 11 for ML

'''
data_eda_marked.index = data_eda_marked.index+pd.to_timedelta(8, unit='h') 

#%%
#EDA file
if(sensor_EDA == "Yes"):
    data_interval_eda = data_eda_marked.resample('5S', how='sum')    
    print("Resample - 5S: EDA")

# Hobo
if(sensor_hobo == "Yes"):
    data_hobo_sesnor = data_hobo_sesnor.set_index(pd.DatetimeIndex(data_hobo_sesnor['Timestamp']))
    data_mean_hobo = data_hobo_sesnor.resample('5S', how='mean')
    print("Resample - 5S: Hobo")
# heat
if(sensor_heat == "Yes"):
    data_heat_sesnor = data_heat_sesnor.set_index(pd.DatetimeIndex(data_heat_sesnor['Timestamp']))
    data_mean_heat = data_heat_sesnor.resample('5S', how='mean')
    print("Resample - 5S: Heat")
# Sound
if(sensor_sound == "Yes"):
    data_sound_sesnor = data_sound_sesnor.set_index(pd.DatetimeIndex(data_sound_sesnor['Timestamp']))
    data_mean_sound = data_sound_sesnor.resample('5S', how='mean')
    print("Resample - 5S: Sound")
# Dust
if(sensor_dust == "Yes"):
    data_dust_sesnor = data_dust_sesnor.set_index(pd.DatetimeIndex(data_dust_sesnor['Timestamp']))
    data_mean_dust = data_dust_sesnor.resample('5S', how='mean')
    print("Resample - 5S: Dust")
# GPS
if(sensor_gps == "Yes"):
    data_gps_sensor = data_gps_sensor.set_index(pd.DatetimeIndex(data_gps_sensor['Timestamp']))
    data_mean_gps = data_gps_sensor.resample('5S', how='mean')
    data_mean_gps = data_mean_gps.interpolate(method="linear", axis=0)
    print("Resample - 5S: GPS")

#%%
from scipy import stats
if(False):    
    cutoff = 2.0 # this may varry form case to case for 3 use 0.4;
    #df = data_mean_gps[(np.abs(stats.zscore(data_mean_gps)) < cutoff).all(axis=1)]
    #data_mean_gps["CutXY"] = (np.abs(stats.zscore(data_mean_gps['wgs_x'])) < cutoff).tolist()
    data_mean_gps["CutXY"] = (np.abs(stats.zscore(data_mean_gps['LAT'])) < cutoff).tolist()
    #data_mean_gps["CutXY"] = ~np.array((data_mean_gps['wgs_x'] < 1.2).tolist())
else:
    cutoff = 10.0 # this may varry form case to case for 3 use 0.4;
    data_mean_gps["CutXY"] = (np.abs(stats.zscore(data_mean_gps['LAT'])) < cutoff).tolist()

#%% check time
#EDA file
if(sensor_EDA == "Yes"):
    print("EDA   start ", data_eda_marked.index[0], data_eda_marked.index[len(data_eda_marked)-1])
# Hobo
if(sensor_hobo == "Yes"):
    print("Hobo  start ", data_hobo_sesnor['Timestamp'].iloc[0], data_hobo_sesnor['Timestamp'].iloc[len(data_hobo_sesnor)-1])
# heat
if(sensor_heat == "Yes"):
    print("Heat  start ", data_heat_sesnor['Timestamp'].iloc[0], data_heat_sesnor['Timestamp'].iloc[len(data_heat_sesnor)-1])
# Sound
if(sensor_sound == "Yes"):
    print("Sound start ", data_sound_sesnor['Timestamp'].iloc[0], data_sound_sesnor['Timestamp'].iloc[len(data_sound_sesnor)-1])
# Dust
if(sensor_dust == "Yes"):
    print("Dust  start ", data_dust_sesnor['Timestamp'].iloc[0], data_dust_sesnor['Timestamp'].iloc[len(data_dust_sesnor)-1])
# GPS
if(sensor_gps == "Yes"):
    print("GPS   start ", data_gps_sensor['Timestamp'].iloc[0], data_gps_sensor['Timestamp'].iloc[len(data_gps_sensor)-1])
#%%
listPID = [] # 1
listTime = [] # 2
listX = [] # 3
listY = [] # 4

listTemp = [] # 6
listRH = [] # 7
listLux = [] # 8
listdB = [] # 9

listHSWind = [] # 10
listHSTemp = [] # 11
listHSTempG = [] # 12
listHSRH = [] # 13

#listPM1 = [] # 10
#listPM2p5 = [] # 11
#listPM10 = [] # 12

listpeak0p01 = [] # 13/14
listSCR0p01 = [] # 14/15
listSCL0p01 = [] # 14/15

listpeak0p05 = [] # 13/14
listSCR0p05 = [] # 14/15
listSCL0p05 = [] # 14/15

listpeak0p1 = [] # 13/14
listSCR0p1 = [] # 14/15
listSCL0p1 = [] # 14/15

import datetime, time


for i in range(len(data_leda_nscr0p01)):
    currentTime = data_interval_eda.index[i]
    
    timeS =  currentTime - datetime.timedelta(seconds=4)# minus 4seconds
    timeE =  currentTime + datetime.timedelta(seconds=4)# plus 4seconds
    
    #Adding data
    listPID.append(participant_int)  # 1
    listTime.append(time.mktime(currentTime.timetuple()))  # 2

    # GPS
    if(sensor_gps == "Yes"):
        #gps: 3,4,5
        if(i < len(data_mean_gps)):
            if((data_mean_gps.index[i] >= timeS) & (data_mean_gps.index[i] <= timeE)):
                if(data_mean_gps['CutXY'][i]==True):
                    listX.append(data_mean_gps['LAT'][i])
                    listY.append(data_mean_gps['LON'][i])
                else:  
                    listX.append(np.nan)
                    listY.append(np.nan)
            else:
                listX.append(np.nan)
                listY.append(np.nan)
        else:
            listX.append(np.nan)
            listY.append(np.nan)
    else:
        listX.append(np.nan)
        listY.append(np.nan)
            
    
    # Hobo
    if(sensor_hobo == "Yes"):        
        #hobo 6,7,8
        if(i < len(data_mean_hobo)):
            #if((data_mean_hobo.index[i] >= timeS) & (data_mean_hobo.index[i] <= timeE)):
            listTemp.append(data_mean_hobo['Temp'][i])
            listRH.append(data_mean_hobo['RH'][i])
            listLux.append(data_mean_hobo['Lux'][i])
            #else:
            #    listTemp.append(np.nan)
            #    listRH.append(np.nan)
            #    listLux.append(np.nan)
        else:
            listTemp.append(np.nan)
            listRH.append(np.nan)
            listLux.append(np.nan)
    else:
        listTemp.append(np.nan)
        listRH.append(np.nan)
        listLux.append(np.nan)    
        
    #Sound 9
    if(sensor_sound == "Yes"):        
        if(i < len(data_mean_sound)):
            #if((data_mean_sound.index[i] >= timeS) & (data_mean_sound.index[i] <= timeE)):
            listdB.append(data_mean_sound['Sound'][i])
            #else:
            #    listdB.append(np.nan)
        else:
            listdB.append(np.nan)
    else:
        listdB.append(np.nan)

    # heat
    if(sensor_heat == "Yes"):        
        #heat 10,11,12,13
        if(i < len(data_mean_heat)):
            #if((data_mean_heat.index[i] >= timeS) & (data_mean_heat.index[i] <= timeE)):
            listHSWind.append(data_mean_heat['Wind Speed'][i])
            listHSTemp.append(data_mean_heat['Temperature'][i])
            listHSTempG.append(data_mean_heat['Globe Temperature'][i])
            listHSRH.append(data_mean_heat['Relative Humidity'][i])
    #       else:
    #            listHSWind.append(np.nan)
    #            listHSTemp.append(np.nan)
    #            listHSTempG.append(np.nan)
    #            listHSRH.append(np.nan)
        else:
            listHSWind.append(np.nan)
            listHSTemp.append(np.nan)
            listHSTempG.append(np.nan)
            listHSRH.append(np.nan)
    else:
        listHSWind.append(np.nan)
        listHSTemp.append(np.nan)
        listHSTempG.append(np.nan)
        listHSRH.append(np.nan)
        
    # Dust
    if(sensor_dust == "Yes"):        
        #dust 10,11,12
        if(i < len(data_mean_dust)):
            if((data_mean_dust.index[i] >= timeS) & (data_mean_dust.index[i] <= timeE)):
                listPM1.append(data_mean_dust['PM1'][i])
                listPM2p5.append(data_mean_dust['PM2p5'][i])
                listPM10.append(data_mean_dust['PM10'][i])
            else:
                listPM1.append(np.nan)
                listPM2p5.append(np.nan)
                listPM10.append(np.nan)
        else:
            listPM1.append(np.nan)
            listPM2p5.append(np.nan)
            listPM10.append(np.nan)
            
    # Store the arousa values
    listpeak0p01.append(data_leda_nscr0p01['CDA.nSCR'][i])  # 13
    listSCR0p01.append(data_leda_nscr0p01['CDA.SCR'][i]) # 14
    listSCL0p01.append(data_leda_nscr0p01['CDA.Tonic'][i]) # 15
    
    listpeak0p05.append(data_leda_nscr0p05['CDA.nSCR'][i])  # 13
    listSCR0p05.append(data_leda_nscr0p05['CDA.SCR'][i]) # 14
    listSCL0p05.append(data_leda_nscr0p05['CDA.Tonic'][i]) # 15
    
    listpeak0p1.append(data_leda_nscr0p1['CDA.nSCR'][i])  # 13
    listSCR0p1.append(data_leda_nscr0p1['CDA.SCR'][i]) # 14
    listSCL0p1.append(data_leda_nscr0p1['CDA.Tonic'][i]) # 15
    

# make the data frome from the collected values
data_fusion = pd.DataFrame({'A' : []})
data_fusion["PID"] = listPID # 1
data_fusion["Time"] = listTime # 2
data_fusion["X"] = listX # 3
data_fusion["Y"] = listY # 4

#data_fusion["Temp"] = listTemp # 6
#data_fusion["RH"] = listRH # 7
#data_fusion["Lux"] = listLux # 8
#data_fusion["Sound"] = listdB # 9


data_fusion["Wind"] = listHSWind # 10
data_fusion["HSTemp"] = listHSTemp # 11
data_fusion["HSTempGlobal"] = listHSTempG # 12
data_fusion["HSRH"] = listHSRH # 13

#data_fusion["PM1"] = listPM1 # 10
#data_fusion["PM2p5"] = listPM2p5 # 11
#data_fusion["PM10"] = listPM10# 12

data_fusion["peakSCR_0p01"] = listpeak0p01# 13/14
data_fusion["phasicSCR_0p01"] = listSCR0p01# 14/15
data_fusion["tonicSCL_0p01"] = listSCL0p01# 14/15

data_fusion["peakSCR_0p05"] = listpeak0p05# 13/14
data_fusion["phasicSCR_0p05"] = listSCR0p05# 14/15
data_fusion["tonicSCL_0p05"] = listSCL0p05# 14/15

data_fusion["peakSCR_0p1"] = listpeak0p1# 13/14
data_fusion["phasicSCR_0p1"] = listSCR0p1# 14/15
data_fusion["tonicSCL_0p1"] = listSCL0p1# 14/15

del data_fusion["A"]    

#%%
fuse_data_file_name = "fused_data_"+str(participant_int)+".csv"
file_ledalab_output =  os.path.join(path_ledalab_files,fuse_data_file_name)# fetching sensor  file path
data_fusion.to_csv(file_ledalab_output)

#%%
print("Enf of file")