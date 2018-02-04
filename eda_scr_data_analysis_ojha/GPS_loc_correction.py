# -*- coding: utf-8 -*-
"""
author@ Vatrun Ojha

GPS location correction
"""
#%% imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
from scipy import stats
#%% retrive data
participant_data_path = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\Participant_Data"
#diretory_eda_gps_sensor = participant_data_path+"\\gps_sensor_data\\5s\\raw_eda_5s"
diretory_eda_gps_sensor = participant_data_path+"\\gps_sensor_data\\5s\\smoot_signals"
file_list_sensors = os.listdir(diretory_eda_gps_sensor)


diretory_gps_loc = participant_data_path+"\\gps_locations\\Isovist"
file_list_gps_loc = os.listdir(diretory_gps_loc)



#Clean list
del file_list_sensors[25:30]
del file_list_sensors[0:5]
#del file_list_sensors[1]
#del file_list_sensors[3]

#del file_list_gps_loc[1]
del file_list_gps_loc[20:23]
#del file_list_gps_loc[3]

for sensor, gps in zip(file_list_sensors, file_list_gps_loc):
    print(sensor+ " - "+gps)
    sensor_data = pd.read_csv(os.path.join(diretory_eda_gps_sensor, sensor))
    gps_data = pd.read_csv(os.path.join(diretory_gps_loc, gps))
    
    if(len(gps_data) != len(sensor_data)):
        if(len(gps_data) > len(sensor_data)):
            minus = len(gps_data)-len(sensor_data)-1
            gps_data = gps_data.drop(gps_data.index[len(gps_data)-len(gps_data)-len(sensor_data)])
        else:
            minus = len(sensor_data)-len(gps_data)-1
            sensor_data = sensor_data.drop(sensor_data.index[len(sensor_data)-minus])
    sensor_data["ID"] = gps_data["ID"].tolist()
    sensor_data["X"] = gps_data["X.coordinate"].tolist()
    sensor_data["Y"] = gps_data["Y.coordinate"].tolist()
    sensor_data["Area"] = gps_data["X2D.180iso.Area"].tolist()
    sensor_data["Perimeter"] = gps_data["X2D.180iso.Perimeter"].tolist()
    sensor_data["Occlusivity"] = gps_data["X2D.180iso.Occlusivity"].tolist()
    sensor_data["Compactness"] = gps_data["X2D.180iso.Compactness"].tolist()
    			
    #del sensor_data["Unnamed: 0"]
    list_of_columns = ['participant','ID','X', 'Y', 'Sound', 'Dust', 'TempEN', 'RH', 'Light', 'Area', 'Perimeter', 'Occlusivity', 'Compactness', 'EDA_peaks', 'EDA_phase','EDA_label']
    sensor_data = sensor_data.reindex(columns=list_of_columns)
    sensor_data.to_csv(os.path.join(diretory_eda_gps_sensor, sensor), index=False)
    

#%%merging data
#diretory_eda_gps_sensor = participant_data_path+"\\gps_sensor_data\\5s\\raw_eda_5s"
diretory_eda_gps_sensor = participant_data_path+"\\gps_sensor_data\\5s\\smoot_signals"
file_list_sensors = os.listdir(diretory_eda_gps_sensor)

del file_list_sensors[25:30]
del file_list_sensors[0:5]

merge_all_files_rowwise(diretory_eda_gps_sensor,file_list_sensors)


#%%normalizing data
sensor_data = pd.read_csv(os.path.join(diretory_eda_gps_sensor, "merged_data.csv"))

cols_to_norm = ["Sound","Dust","TempEN","RH","Light","EDA_peaks"]
sensor_data[cols_to_norm] = sensor_data[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

#break the file participants_wise
d = {}
for i in [6,7,8,9,10,11,13,16,23,24,25,26,27,28,29,30,31,32,34,35]:
    d[i] = sensor_data[sensor_data["participant"] == i]

#spliting participants and saving files
for i in [6,7,8,9,10,11,13,16,23,24,25,26,27,28,29,30,31,32,34,35]:
    df = d[i]
    file_name = "eda_gps_norm_"+str(i)+".csv"
    df.to_csv(file_name)

#%%merging code
def merge_all_files_rowwise(diractory,file_list):
    for i in range(len(file_list)):
        if i > 15:
            participant = file_list[i][9:10]
        else:
            participant = file_list[i][9:11]
        
        print(participant)
        
        file_abs_path = os.path.join(diractory, file_list[i])
        if(i == 0):
            #result = pd.DataFrame.from_csv(file_abs_path)
            result = pd.read_csv(file_abs_path,  index_col = False)
        else:
            #temp = pd.DataFrame.from_csv(file_abs_path)
            temp = pd.read_csv(file_abs_path,  index_col = False)
            result = result.append(temp)
            
    gps_merged_file = os.path.join(diractory, "complied_data.csv")
    result.to_csv(gps_merged_file)







