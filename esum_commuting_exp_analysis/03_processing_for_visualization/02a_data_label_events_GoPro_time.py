# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 17:12:33 2018

@author: vojha
"""
#importing packages
import pandas as pd
import os
from datetime import datetime
#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_SG")
path_raw_data_files = os.path.join(path_raw_data_files,"compiled_data")

os.chdir(path_raw_data_files)

#%%

SG = [1,2,3,4,5,6,7,8,9]

for participant_int in SG:
    #participant_int = 1
    if(participant_int <4):
        file_label_to_read = "round_label_01.csv"
    elif(participant_int >3 and participant_int < 7):
        file_label_to_read = "round_label_02.csv"
    else:
        file_label_to_read = "round_label_03.csv"

    print("file_label_to_read: ",participant_int, file_label_to_read)        
    file_data_to_read = "fused_data_zScore"+str(participant_int)+".csv"
    
    data_label = pd.read_csv(file_label_to_read)
    data_label = data_label.drop(['Unnamed: 0'], axis=1)
    
    data_participant = pd.read_csv(file_data_to_read)
    data_participant = data_participant.drop(['Unnamed: 0'], axis=1)
    
    #check time
    time_Lstart = datetime.fromtimestamp(int(data_label["Timestamp"][0]))
    time_Lendtm = datetime.fromtimestamp(int(data_label["Timestamp"][len(data_label)-1]))
    time_Estart = datetime.fromtimestamp(int(data_participant["Time"][0]))
    time_Eendtm = datetime.fromtimestamp(int(data_participant["Time"][len(data_participant)-1]))
    print("Label Start  ",time_Lstart) 
    print("Eabel Start  ",time_Estart, "   dif  ",time_Lstart-time_Estart) 
    #print("Eabel Start  ",time_Estart, "   dif  ",time_Estart-time_Lstart) 
    print("Label End    ",time_Lendtm) 
    #print("Eabel End    ",time_Eendtm, "   dif  ",time_Lendtm-time_Eendtm) 
    print("Eabel End    ",time_Eendtm, "   dif  ",time_Eendtm-time_Lendtm) 
    
    
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
    print("Saved")