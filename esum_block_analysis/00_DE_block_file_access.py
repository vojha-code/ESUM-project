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
#%% retrive data

Wiemar = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_Block","recording")
EDA = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_Block\processed","EDA")
Video = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_Block\processed","Video")
Hobo = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_Block\processed","Hobo")
#%%
FLOC = Wiemar
folder_dates = os.listdir(FLOC)
pid = 1
for f_dates in range(len(folder_dates)-1):
    print(" ",f_dates,folder_dates[f_dates])
    
    folder_ID = os.listdir(os.path.join(FLOC,folder_dates[f_dates]))

    for f_ID in range(len(folder_ID)):
        if("ABBRUCH" in folder_ID[f_ID]):
            print("         ")
        else:
            print("         ",pid,folder_ID[f_ID])          

            data_path = os.path.join(os.path.join(FLOC,folder_dates[f_dates]),folder_ID[f_ID])
            folder_data = os.listdir(data_path)

            #path to eda and video files
            path_eda_data = os.path.join(data_path,"E4_data")
            path_video_data = os.path.join(data_path,"Video_data")
            path_hobo_data = os.path.join(data_path,"Hobo_data")
            
            
            #list of files in directory
            data_eda = os.listdir(path_eda_data)
            
            data_Video = os.listdir(path_video_data)
            # One lavel more for Video
            path_video_data = os.path.join(path_video_data,data_Video[0])
            data_Video = os.listdir(path_video_data)
            
            data_Hobo = os.listdir(path_hobo_data)
            

            #files name
            file_eda = [x for x in data_eda if "EDA.csv" in x][0]
            file_video_q = data_Video[0]
            file_video_t = data_Video[2]
            file_hobo = data_Hobo[0]
            print("                 ",file_eda)
            print("                 ",file_video_q)
            print("                 ",file_video_t)
            print("                 ",file_hobo)
            
            if(pid < 10):
                str_pid = "0"+str(pid)
            else:
                str_pid = str(pid)
                
            pd.DataFrame.from_csv(os.path.join(path_eda_data,file_eda)).to_csv(os.path.join(EDA,"EDA_"+str_pid+".csv"))
            pd.DataFrame.from_csv(os.path.join(path_video_data,file_video_q)).to_csv(os.path.join(Video,"VQ_"+str_pid+".csv"))
            pd.DataFrame.from_csv(os.path.join(path_video_data,file_video_t)).to_csv(os.path.join(Video,"VT_"+str_pid+".csv"))   
            
            ##This will move the file from one folder to another : os.rename(hoboSource, hobodestination)
            os.rename(os.path.join(path_hobo_data,file_hobo),os.path.join(Hobo,"Hobo_"+str_pid+".hobo"))

            
            #increasing pid
            pid = pid + 1

print(folder_dates[len(folder_dates)-1])



