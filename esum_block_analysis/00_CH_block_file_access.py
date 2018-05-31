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
Zurich = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_Block","recording")
EDA = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_Block\processed","EDA")
Video = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_Block\processed","Video")
#%%
FLOC = Zurich
folder_dates = os.listdir(FLOC)
pid = 1
for f_dates in range(len(folder_dates)-1):
    print(" ",f_dates,folder_dates[f_dates])

    data_path = os.path.join(FLOC,folder_dates[f_dates])
    folder_data = os.listdir(data_path)
    
    #path to eda and video files
    path_eda_data = os.path.join(data_path,"E4_data")
    path_video_data = os.path.join(data_path,"Video_data")
    
    
    #list of files in directory
    data_eda = os.listdir(path_eda_data)
    data_Video = os.listdir(path_video_data)
    
    #files name
    file_eda = [x for x in data_eda if "EDA.csv" in x][0]
    file_video_q = data_Video[0]
    file_video_t = data_Video[1]
    print("                 ",file_eda)
    print("                 ",file_video_q)
    print("                 ",file_video_t)
    
    if(pid < 10):
        str_pid = "0"+str(pid)
    else:
        str_pid = str(pid)
        
    pd.DataFrame.from_csv(os.path.join(path_eda_data,file_eda)).to_csv(os.path.join(EDA,"EDA_"+str_pid+".csv"))
    pd.DataFrame.from_csv(os.path.join(path_video_data,file_video_q)).to_csv(os.path.join(Video,"VQ_"+str_pid+".csv"))
    pd.DataFrame.from_csv(os.path.join(path_video_data,file_video_t)).to_csv(os.path.join(Video,"VT_"+str_pid+".csv"))   
       
    #increasing pid
    pid = pid + 1

print(folder_dates[len(folder_dates)-1])



