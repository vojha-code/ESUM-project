""""
Last Modifed: 01 June 2017: 16:12 
@author: Varun Ojha 
This program marke process EDA signal.
It works on EDA dat was taken from Empatica output
EDA singal works on 4 Hz frequency

:::Inputs files:::
    EDA.csv marked in t seconds
    tag.csv
    status.csv
    data_all_par#.csv

:::Outputs files:::
    merged_data.csv

"""
#%% imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
#%% collect_regular_results
def collect_regular_results(diretory,file_list):
    list_of_nSCR = []
    list_of_nPhase = []
    participants_name = []
    length_list = []
    for i in range(len(file_list)):
        result_file = os.path.join(diretory, file_list[i])
        result_data = pd.read_excel(result_file,sheetname='ERA')
        print(i," ",file_list[i],":", len(result_data["Event"]))
        participant = ""
        if i > 15:
            participant = file_list[i][12:13]# for taking eda marker results
            #participant = file_list[i][20:21]
        else:
            participant = file_list[i][12:14]# for taking eda marker results
            #participant = file_list[i][20:22]
            
        print(participant)
        
        ithlistnSCR = result_data["CDA.nSCR"].tolist()
        list_of_nSCR.append(ithlistnSCR)
        
        ithlistPahse = result_data["CDA.PhasicMax"].tolist()
        list_of_nPhase.append(ithlistPahse)
        
        length_list.append(len(ithlistnSCR))
        participants_name.append(participant)

    event_data = pd.DataFrame(list_of_nSCR)
    event_data = event_data.transpose()
    event_data.columns = participants_name
    
    phase_data = pd.DataFrame(list_of_nPhase)
    phase_data = phase_data.transpose()
    phase_data.columns = participants_name
    
    return event_data,phase_data,length_list
#%% input to gps data
def eda_label_in_gpd_data(diretory,event_data,phase_data,length_list,file_list,file_list_gps):
    for i in range(len(file_list)):
        if i > 15:
            participant_eda = file_list[i][12:13]
            participant_gps = file_list_gps[i][9:10]
            #participant_gps = file_list_gps[i][8:9]
        else:
            participant_eda = file_list[i][12:14]
            participant_gps = file_list_gps[i][9:11]
            #participant_gps = file_list_gps[i][8:10]
    
        if(participant_eda == participant_gps):
            print(participant_eda)
        else:
            print("File missmatch", participant_eda," !=",participant_gps)
    
        diretory = diretory_data
        gps_file = os.path.join(diretory, file_list_gps[i])
        gps_sensor_data = pd.DataFrame.from_csv(gps_file)
        
        particiapnt_number = []
        eda_peaks = []
        eda_label = []
        pahe_max = []
        for j in range(len(gps_sensor_data)):
            label = 0
            if(event_data[participant_eda][j]>0):
                label = 1 
            
            eda_peaks.append(event_data[participant_eda][j])
            eda_label.append(label)
            pahe_max.append(phase_data[participant_eda][j])
            particiapnt_number.append(int(float(participant_gps)))
        
        gps_sensor_data["participant"] = particiapnt_number
        gps_sensor_data["EDA_peaks"] = eda_peaks
        gps_sensor_data["EDA_label"] = eda_label
        gps_sensor_data["EDA_phase"] = pahe_max
        if("time" in gps_sensor_data.columns):
            del gps_sensor_data['time']
        
        gps_sensor_data.to_csv(gps_file)
    return True
#%%merege file row wise
def merge_all_files_rowwise(diractory,file_list_gps):
    for i in range(len(file_list_gps)):
        if i > 15:
            participant_gps = file_list_gps[i][9:10]
            #participant = file_list_gps[i][8:9]
        else:
            participant_gps = file_list_gps[i][9:11]
            #participant = file_list_gps[i][8:10]
        
        print(participant)
        gps_file = os.path.join(diractory, file_list_gps[i])
        if(i == 0):
            result = pd.DataFrame.from_csv(gps_file)
        else:
            temp = pd.DataFrame.from_csv(gps_file)
            result = result.append(temp)
    result.interpolate()
    
    gps_merged_file = os.path.join(diractory, "merged_data.csv")
    result.to_csv(gps_merged_file)

#%%reorder columns
def reorder_columns(diretory,list_of_columns):
    gps_merged_file = os.path.join(diretory, "merged_data.csv")
    result = pd.DataFrame.from_csv(gps_merged_file)
    #list_of_columns = result.columns
    result = result.reindex(columns=list_of_columns)
    #result.to_csv(gps_merged_file)
#%% retrive data
diretory_eda = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\eda_Ledalab_analysis\\regular_5s_smooth\\results"
file_list = os.listdir(diretory_eda)
#fetch the eda_marked_results
event_data,phase_data,length_list = collect_regular_results(diretory_eda,file_list)
#event_data.to_csv("interval_10s_combined_data.csv")
#phase_data.to_csv("interval_10s_pahse_data.csv")

#
diretory_gps_data = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\Participant_Data\\gps_sensor_data\\5s"
#diretory_isovist_data = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\Participant_Data\\gps_locations\\Isovist"

diretory_data = diretory_gps_data
file_list_gps = os.listdir(diretory_data)
del file_list_gps[4]
del file_list_gps[20]
val = eda_label_in_gpd_data(diretory_data,event_data,phase_data,length_list,file_list,file_list_gps)

val = merge_all_files_rowwise(diretory_data,file_list_gps)

list_of_columns = ['participant','X', 'Y', 'Sound', 'Dust', 'TempEN', 'RH', 'Light','EDA_peaks', 'EDA_phase','EDA_label']
#
#list_of_columns = ["ID",
#"X.coordinate",
#"Y.coordinate",
#"Z.coordinate",
#"participant",
#"Sphere.subdivision",
#"Ray.count",
#"Horizontal.angle",
#"Vertical.up.angle",
#"Vertical.down.angle",
#"Eye.level",
#"Visibility.threshold",
#"Metric.Choice..SLW.",
#"Metric.Choice..SLW..R800.metric",
#"Metric.Choice..SLW..R1600.metric",
#"Metric.Total.Depth",
#"Metric.Total.Depth.R800.metric",
#"Metric.Total.Depth.R1600.metric",
#"T1024.Choice..Segment.Length.Wgt.",
#"T1024.Choice..Segment.Length.Wgt..R800.metric",
#"T1024.Choice..Segment.Length.Wgt..R1600.metric",
#"T1024.Integration..Segment.Length.Wgt.",
#"T1024.Integration..Segment.Length.Wgt..R800.metric",
#"T1024.Integration..Segment.Length.Wgt..R1600.metric",
#"VRay.min",
#"VRay.max",
#"VRay.mean",
#"VRay.median",
#"VRay.std",
#"VRay.sum",
#"VHRay.min",
#"VHRay.max",
#"VHRay.mean",
#"VHRay.median",
#"VHRay.std",
#"VHRay.sum",
#"Volume",
#"Ray.horizontal",
#"Ray.vertical",
#"Ray.sky",
#"LRay.length",
#"RRay.length",
#"FRay.length",
#"LRay.angle",
#"RRay.angle",
#"FRay.angle",
#"X2D.180iso.Area",
#"X2D.180iso.Perimeter",
#"X2D.180iso.Occlusivity",
#"X2D.180iso.Compactness",
#"EDA_peaks",
#"EDA_label",
#"EDA_phase"]

val = reorder_columns(diretory_data,list_of_columns)


#gps_merged_file = os.path.join(diretory_data, "merged_data.csv")
#all_data_gps = pd.DataFrame.from_csv(gps_merged_file)
#list_of_columns = [
#"participant",
#"X.coordinate",
#"Y.coordinate",
#"X2D.180iso.Area",
#"X2D.180iso.Perimeter",
#"X2D.180iso.Occlusivity",
#"X2D.180iso.Compactness",
#"EDA_peaks",
#"EDA_label",
#"EDA_phase"]
#
#only2D = all_data_gps[list_of_columns]
#only2D.to_csv(os.path.join(diretory_data, "merged_data_2Donly.csv"))


