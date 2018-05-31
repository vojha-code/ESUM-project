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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md # for date in x axis
import datetime as dt
from scipy import stats

#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
path_raw_data_files_zh = os.path.join(path_raw_data_files, "Data_ZH")
path_raw_data_files_sg = os.path.join(path_raw_data_files, "Data_SG")
path_raw_data_files_ml = os.path.join(path_raw_data_files, "Data_ML")
path_raw_data_files_cn = os.path.join(path_raw_data_files, "Data_CN")
path_raw_data_files_hk = os.path.join(path_raw_data_files, "Data_HK")

path_raw_data_files_zh = os.path.join(path_raw_data_files_zh,"for_stat")
path_raw_data_files_sg = os.path.join(path_raw_data_files_sg,"for_stat")
path_raw_data_files_ml = os.path.join(path_raw_data_files_ml,"for_stat")
path_raw_data_files_cn = os.path.join(path_raw_data_files_cn,"for_stat")
path_raw_data_files_hk = os.path.join(path_raw_data_files_hk,"for_stat")

os.chdir(path_raw_data_files)
#%% line chart

data_participant_zh = pd.read_csv(os.path.join(path_raw_data_files_zh,"event_scl_peak_z.csv"))
data_participant_sg = pd.read_csv(os.path.join(path_raw_data_files_sg,"event_scl_peak.csv"))
data_participant_ml = pd.read_csv(os.path.join(path_raw_data_files_ml,"event_scl_peak.csv"))
data_participant_cn = pd.read_csv(os.path.join(path_raw_data_files_cn,"event_scl_peak.csv"))
data_participant_hk = pd.read_csv(os.path.join(path_raw_data_files_hk,"event_scl_peak.csv"))

#data_participant = data_participant.drop(['Unnamed: 0'], axis=1)

#%% ZH
column = data_participant_zh["Participant"].tolist()
del data_participant_zh["Participant"]
data_participant_zh = data_participant_zh.transpose()
data_participant_zh.columns = column
##data_participant_zh["Events"] = data_participant_zh.index.values.tolist()
data_participant_zh = data_participant_zh.reset_index()

#SG
column = data_participant_sg["Participant"].tolist()
del data_participant_sg["Participant"]
data_participant_sg = data_participant_sg.transpose()
data_participant_sg.columns = column
data_participant_sg = data_participant_sg.reset_index()

#ML
column = data_participant_ml["Participant"].tolist()
del data_participant_ml["Participant"]
data_participant_ml = data_participant_ml.transpose()
data_participant_ml.columns = column
data_participant_ml = data_participant_ml.reset_index()

#CN
column = data_participant_cn["Participant"].tolist()
del data_participant_cn["Participant"]
data_participant_cn = data_participant_cn.transpose()
data_participant_cn.columns = column
data_participant_cn = data_participant_cn.reset_index()

#HK
column = data_participant_hk["Participant"].tolist()
del data_participant_hk["Participant"]
data_participant_hk = data_participant_hk.transpose()
data_participant_hk.columns = column
data_participant_hk = data_participant_hk.reset_index()
#%%
events = ["Ride","Wait","Walk"]

df = data_participant_zh

ride_bool = []    
wait_bool = []
walk_bool = []

count_ride = 0
count_wait = 0
count_walk = 0

for i  in range(len(df)):
    if (df['index'][i].startswith('Ride')):
        ride_bool.append(True)
        count_ride = count_ride + 1
    else:
        ride_bool.append(False)
        
    if (df['index'][i].startswith('Wait')):
        wait_bool.append(True)
        count_wait = count_wait + 1
    else:
        wait_bool.append(False)

    if (df['index'][i].startswith('Walk')):
        walk_bool.append(True)
        count_walk = count_walk + 1
    else:
        walk_bool.append(False)
            
df_ride_sum = df.groupby(ride_bool).mean().reset_index()
df_ride_sum = df_ride_sum.drop(df.index[0]).reset_index(drop=True)

df_wait_sum = df.groupby(wait_bool).mean().reset_index()
df_wait_sum = df_wait_sum.drop(df.index[0]).reset_index(drop=True)

df_walk_sum = df.groupby(walk_bool).mean().reset_index()
df_walk_sum = df_walk_sum.drop(df.index[0]).reset_index(drop=True)

data_zh = [df_ride_sum, df_wait_sum, df_walk_sum]
data_zh = pd.concat(data_zh)
data_zh = data_zh.reset_index(drop=True)
del data_zh["index"]
data_zh["Event"] = events



# SG
df = data_participant_sg

ride_bool = []    
wait_bool = []
walk_bool = []

count_ride = 0
count_wait = 0
count_walk = 0

for i  in range(len(df)):
    if (df['index'][i].startswith('Ride')):
        ride_bool.append(True)
        count_ride = count_ride + 1
    else:
        ride_bool.append(False)
        
    if (df['index'][i].startswith('Wait')):
        wait_bool.append(True)
        count_wait = count_wait + 1
    else:
        wait_bool.append(False)

    if (df['index'][i].startswith('Walk')):
        walk_bool.append(True)
        count_walk = count_walk + 1
    else:
        walk_bool.append(False)
            
df_ride_sum = df.groupby(ride_bool).mean().reset_index()
df_ride_sum = df_ride_sum.drop(df.index[0]).reset_index(drop=True)

df_wait_sum = df.groupby(wait_bool).mean().reset_index()
df_wait_sum = df_wait_sum.drop(df.index[0]).reset_index(drop=True)

df_walk_sum = df.groupby(walk_bool).mean().reset_index()
df_walk_sum = df_walk_sum.drop(df.index[0]).reset_index(drop=True)

data_sg = [df_ride_sum, df_wait_sum, df_walk_sum]
data_sg = pd.concat(data_sg)
data_sg = data_sg.reset_index(drop=True)
del data_sg["index"]
data_sg["Event"] = events


# Ml
df = data_participant_ml

ride_bool = []    
wait_bool = []
walk_bool = []

count_ride = 0
count_wait = 0
count_walk = 0

for i  in range(len(df)):
    if (df['index'][i].startswith('Ride')):
        ride_bool.append(True)
        count_ride = count_ride + 1
    else:
        ride_bool.append(False)
        
    if (df['index'][i].startswith('Wait')):
        wait_bool.append(True)
        count_wait = count_wait + 1
    else:
        wait_bool.append(False)

    if (df['index'][i].startswith('Walk')):
        walk_bool.append(True)
        count_walk = count_walk + 1
    else:
        walk_bool.append(False)
            
df_ride_sum = df.groupby(ride_bool).mean().reset_index()
df_ride_sum = df_ride_sum.drop(df.index[0]).reset_index(drop=True)

df_wait_sum = df.groupby(wait_bool).mean().reset_index()
df_wait_sum = df_wait_sum.drop(df.index[0]).reset_index(drop=True)

df_walk_sum = df.groupby(walk_bool).mean().reset_index()
df_walk_sum = df_walk_sum.drop(df.index[0]).reset_index(drop=True)

data_ml = [df_ride_sum, df_wait_sum, df_walk_sum]
data_ml = pd.concat(data_ml)
data_ml = data_ml.reset_index(drop=True)
del data_ml["index"]

data_ml["Event"] = events

# CN
df = data_participant_cn

ride_bool = []    
wait_bool = []
walk_bool = []

count_ride = 0
count_wait = 0
count_walk = 0

for i  in range(len(df)):
    if (df['index'][i].startswith('Ride')):
        ride_bool.append(True)
        count_ride = count_ride + 1
    else:
        ride_bool.append(False)
        
    if (df['index'][i].startswith('Wait')):
        wait_bool.append(True)
        count_wait = count_wait + 1
    else:
        wait_bool.append(False)

    if (df['index'][i].startswith('Walk')):
        walk_bool.append(True)
        count_walk = count_walk + 1
    else:
        walk_bool.append(False)
            
df_ride_sum = df.groupby(ride_bool).mean().reset_index()
df_ride_sum = df_ride_sum.drop(df.index[0]).reset_index(drop=True)

df_wait_sum = df.groupby(wait_bool).mean().reset_index()
df_wait_sum = df_wait_sum.drop(df.index[0]).reset_index(drop=True)

df_walk_sum = df.groupby(walk_bool).mean().reset_index()
df_walk_sum = df_walk_sum.drop(df.index[0]).reset_index(drop=True)

data_cn = [df_ride_sum, df_wait_sum, df_walk_sum]
data_cn = pd.concat(data_cn)
data_cn = data_cn.reset_index(drop=True)
del data_cn["index"]

data_cn["Event"] = events


# HK
df = data_participant_hk

ride_bool = []    
wait_bool = []
walk_bool = []

count_ride = 0
count_wait = 0
count_walk = 0

for i  in range(len(df)):
    if (df['index'][i].startswith('Ride')):
        ride_bool.append(True)
        count_ride = count_ride + 1
    else:
        ride_bool.append(False)
        
    if (df['index'][i].startswith('Wait')):
        wait_bool.append(True)
        count_wait = count_wait + 1
    else:
        wait_bool.append(False)

    if (df['index'][i].startswith('Walk')):
        walk_bool.append(True)
        count_walk = count_walk + 1
    else:
        walk_bool.append(False)
            
df_ride_sum = df.groupby(ride_bool).mean().reset_index()
df_ride_sum = df_ride_sum.drop(df.index[0]).reset_index(drop=True)

df_wait_sum = df.groupby(wait_bool).mean().reset_index()
df_wait_sum = df_wait_sum.drop(df.index[0]).reset_index(drop=True)

df_walk_sum = df.groupby(walk_bool).mean().reset_index()
df_walk_sum = df_walk_sum.drop(df.index[0]).reset_index(drop=True)

data_hk = [df_ride_sum, df_wait_sum, df_walk_sum]
data_hk = pd.concat(data_hk)
data_hk = data_hk.reset_index(drop=True)
del data_hk["index"]

data_cn["Event"] = events
#%% setting variable for plot
time_zh = data_zh["Time"]
scl_zh =  data_zh["SCL"]
peak_zh =  data_zh["Peak"]
temp_zh = data_zh["Temp"]
rh_zh = data_zh["RH"]
sound_zh = data_zh["Sound"]
lux_zh = data_zh["Lux"]

time_sg = data_sg["Time"]
scl_sg =  data_sg["SCL"]
peak_sg =  data_sg["Peak"]
temp_sg = data_sg["Temp"]
rh_sg = data_sg["RH"]
sound_sg = data_sg["Sound"]
lux_sg = data_sg["Lux"]


time_ml = data_ml["Time"]
scl_ml =  data_ml["SCL"]
peak_ml =  data_ml["Peak"]
temp_ml = data_ml["Temp"]
rh_ml = data_ml["RH"]
sound_ml = data_ml["Sound"]
lux_ml = data_ml["Lux"]

time_cn = data_cn["Time"]
scl_cn =  data_cn["SCL"]
peak_cn =  data_cn["Peak"]
temp_cn = data_cn["Temp"]
rh_cn = data_cn["RH"]
sound_cn = data_cn["Sound"]
lux_cn = data_cn["Lux"]


time_hk = data_hk["Time"]
scl_hk =  data_hk["SCL"]
peak_hk =  data_hk["Peak"]
temp_hk = data_hk["Temp"]
rh_hk = data_hk["RH"]
sound_hk = data_hk["Sound"]
lux_hk = data_hk["Lux"]
#%% Time norm
if(False):
    norm = " (norm)"
    scl_zh   = scl_zh   / time_zh
    peak_zh  = peak_zh  / time_zh
    temp_zh  = temp_zh  / time_zh
    rh_zh    = rh_zh    / time_zh
    sound_zh = sound_zh / time_zh
    lux_zh   = lux_zh   / time_zh
    
    scl_sg   = scl_sg   / time_sg
    peak_sg  = peak_sg  / time_sg
    temp_sg  = temp_sg  / time_sg
    rh_sg    = rh_sg    / time_sg
    sound_sg = sound_sg / time_sg
    lux_sg   = lux_sg   / time_sg
    
    scl_ml   = scl_ml   / time_ml
    peak_ml  = peak_ml  / time_ml
    temp_ml  = temp_ml  / time_ml
    rh_ml    = rh_ml    / time_ml
    sound_ml = sound_ml / time_ml
    lux_ml   = lux_ml   / time_ml
    
    scl_cn   = scl_cn   / time_cn
    peak_cn  = peak_cn  / time_cn
    temp_cn  = temp_cn  / time_cn
    rh_cn    = rh_cn    / time_cn
    sound_cn = sound_cn / time_cn
    lux_cn   = lux_cn   / time_cn
    
    scl_hk   = scl_hk   / time_hk
    peak_hk  = peak_hk  / time_hk
    temp_hk  = temp_hk  / time_hk
    rh_hk    = rh_hk    / time_hk
    sound_hk = sound_hk / time_hk
    lux_hk   = lux_hk   / time_hk
else:
    norm = ""    
#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

n_groups = len(events)


plotVariable = "Avg. temp ($^O$C)"+norm + " per 5 sec." 
bar_1 = temp_zh
bar_2 = temp_sg
bar_3 = temp_ml
bar_4 = temp_cn
bar_5 = temp_hk
lowY = 10
#
plotVariable = "Avg. RH (%)"+norm + " per 5 sec." 
bar_1 = rh_zh
bar_2 = rh_sg
bar_3 = rh_ml
bar_4 = rh_cn
bar_5 = rh_hk
lowY = 30
#####
plotVariable = "Avg. sound (dB)"+norm + " per 5 sec." 
bar_1 = sound_zh
bar_2 = sound_sg
bar_3 = sound_ml
bar_4 = sound_cn
bar_5 = sound_hk
lowY = 60
######
plotVariable = "Avg. illuminance (lux)"+norm+ " per 5 sec." 
bar_1 = lux_zh
bar_2 = lux_sg
bar_3 = lux_ml
bar_4 = lux_cn
bar_5 = lux_hk
lowY = 0
######
plotVariable = "Avg. # peak (SCR 0.05)"+norm + " per 5 sec." 
bar_1 = peak_zh
bar_2 = peak_sg
bar_3 = peak_ml
bar_4 = peak_cn
bar_5 = peak_hk
lowY = 0
##
plotVariable = "Avg. SCL (tonic)"+norm + " per 5 sec." 
bar_1 = scl_zh
bar_2 = scl_sg
bar_3 = scl_ml
bar_4 = scl_cn
bar_5 = scl_hk
lowY = 0
###
plotVariable = "Avg. time (minutes)" + " per event" 
bar_1 = time_zh
bar_2 = time_sg
bar_3 = time_ml
bar_4 = time_cn
bar_5 = time_hk
lowY = 0



fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.17
opacity = 0.4

rects1 = ax.bar(index, bar_1, bar_width,alpha=opacity, color='b', label='Zurich')
rects2 = ax.bar(index + bar_width, bar_2, bar_width, alpha=opacity, color='r', label='Singapore')
rects3 = ax.bar(index + bar_width*2, bar_3, bar_width, alpha=opacity, color='g', label='Melbourne')
rects4 = ax.bar(index + bar_width*3, bar_4, bar_width, alpha=opacity, color='darkorange', label='Shenzhen')
rects5 = ax.bar(index + bar_width*4, bar_5, bar_width, alpha=opacity, color='dodgerblue', label='Hong Kong')

ymin, ymax = ax.get_ylim()
print(ymax)
ymin = lowY
ax.set_ylim(ymin, ymax)

ax.set_ylabel(plotVariable)
ax.set_xticks(index + bar_width*2)
ax.set_xticklabels(events)
ax.legend()

fig.tight_layout()
plt.show()
fig.savefig("comparison_"+plotVariable+".pdf",bbox_inches='tight')
fig.savefig("comparison_"+plotVariable+".jpg",bbox_inches='tight')