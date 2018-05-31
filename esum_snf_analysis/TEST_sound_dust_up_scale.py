# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import scipy.signal as scisig
import os
from datetime import datetime
from datetime import timedelta
from calendar import timegm
import dateutil.parser


import matplotlib.pyplot as plt
import numpy as np
from random import randint

#%%
participant_data_path = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\Participant_Data"
filepath_gps_data = participant_data_path+"\\all_participants"

i = 6
gps_file_name = "data_all_"+str(i)+".csv"
gps_file =  os.path.join(filepath_gps_data,gps_file_name)


gps_data = pd.DataFrame.from_csv(gps_file,header=None)
gps_data = gps_data.iloc[:,[i+4 for i in range(8)]]
del gps_data[10]

sound = gps_data[5].tolist()
dust = gps_data[6].tolist()
#temp = gps_data[7].tolist()
#rh = gps_data[8].tolist()
#light = gps_data[9].tolist()

#sound interpolation
i = 0
while(i < len(gps_data)):
    j = i +1
    try:
        while(True):
            if(sound[i] == sound[j]):
                sound[j] = np.NaN
                j += 1
            else:
                i = j
                break
    except IndexError:
        break
            
            
gps_data[0] =  sound   
gps_data = gps_data.interpolate(method='linear')

#dust interpolation
i = 0
while(i < len(gps_data)):
    j = i +1
    try:
        while(True):
            if(dust[i] == dust[j]):
                dust[j] = np.NaN
                j += 1
            else:
                i = j
                break
    except IndexError:
        break        
gps_data[1] =  dust          
gps_data = gps_data.interpolate(method='linear')


##temp interpolation
#i = 0
#while(i < len(gps_data)):
#    j = i +1
#    try:
#        while(True):
#            if(temp[i] == temp[j]):
#                temp[j] = np.NaN
#                j += 1
#            else:
#                i = j
#                break
#    except IndexError:
#        break        
#gps_data[2] =  temp          
#gps_data = gps_data.interpolate(method='linear')
#
##rh interpolation
#i = 0
#while(i < len(gps_data)):
#    j = i +1
#    try:
#        while(True):
#            if(rh[i] == rh[j]):
#                rh[j] = np.NaN
#                j += 1
#            else:
#                i = j
#                break
#    except IndexError:
#        break        
#gps_data[3] =  rh          
#gps_data = gps_data.interpolate(method='linear')
#
##light interpolation
#i = 0
#while(i < len(gps_data)):
#    j = i +1
#    try:
#        while(True):
#            if(light[i] == light[j]):
#                light[j] = np.NaN
#                j += 1
#            else:
#                i = j
#                break
#    except IndexError:
#        break        
#gps_data[4] =  light          
#gps_data = gps_data.interpolate(method='linear')

#df = gps_data[[5, 4]].copy()
#df1 = gps_data[[6, 3]].copy()

del gps_data[5]
del gps_data[6]
#del gps_data[7]
#del gps_data[8]
#del gps_data[9]

gps_data = gps_data.rename(columns={0: 5, 1: 6})
gps_data = gps_data.sort_index(axis=1)
