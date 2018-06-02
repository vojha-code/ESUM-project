# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 13:27:23 2018

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

from scipy import stats
#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
city = "ZH"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_"+city)
path_raw_data_files = os.path.join(path_raw_data_files,"for_stat")

os.chdir(path_raw_data_files)
#%%
data_participant = pd.read_csv("merged_data_zscore.csv")
data_participant = data_participant.drop(['Unnamed: 0'], axis=1)
#%% plots
listEnventName = []

##for ZH data
for i in range(len(data_participant)):
    if (data_participant['EvenName'][i].startswith('ride')):
        listEnventName.append('Ride')
    elif (data_participant['EvenName'][i].startswith('wait')):
        listEnventName.append('Wait')
    elif (data_participant['EvenName'][i].startswith('walk')):
        listEnventName.append('Walk')   
    else:
        listEnventName.append(data_participant['EvenName'][i])        

data_participant['Gen_Event_Name'] = listEnventName    

group = False
if(group == True):
    data_grouped_event = data_participant.groupby(['Gen_Event_Name'])
else:
    data_grouped_event = data_participant.groupby(['EvenName'])
#data_grouped_event = data_participant.groupby(['PID'])
##data_grouped_event = data_participant.groupby(['X', 'Y'])
#%%
df_mean = data_grouped_event.mean()


#df_mean.to_csv("xymean.csv")
df_count = data_grouped_event.count()
df_std = data_grouped_event.std()
df_descrive = data_grouped_event.describe()
#%%removing unknun data
df_mean = df_mean[df_mean.index != "unknown"] #removing unknun data
df_count = df_count[df_count.index != "unknown"] #removing unknun data
df_std = df_mean[df_mean.index != "unknown"] #removing unknun data


#removing start data
df_mean = df_mean[df_mean.index != "S"] #removing unknun data
df_count = df_count[df_count.index != "S"] #removing unknun data
df_std = df_std[df_std.index != "S"] #removing unknun data
#%%rename index
####for ZH data

listforbarname = ['Ride', 'Wait','Walk']

listforbarname = ['Ride the TrollyBus-1', 'Ride the TrollyBus-2', 'Ride the HybridBus-1', 'Ride the HybridBus-2', 
'Wait for the TrollyBus-1', 'Wait for the TrollyBus-2', 'Wait for the HybridBus-1', 'Wait for the HybridBus-2', 
'Walk to the Finish point', 'Walk to the TrollyBus-1', 'Walk to the TrollyBus-2', 'Walk to the HybridBus-1', 'Walk to the HybridBus-2']

df_mean["envetname"] = listforbarname
df_mean = df_mean.set_index('envetname')

print(df_mean["Peak"])
print(df_mean["Amp"])

df_std["envetname"] = listforbarname
df_std = df_std.set_index('envetname')

df_mean.drop(["Time","PID","X","Y"],axis=1, inplace=True)
df_mean.transpose().to_csv("event_data_"+city+".csv")
#%%
df_trans = df_mean.transpose()

listforbarname = ['Walk to the HybridBus-1', 
                  'Wait for the HybridBus-1', 
                  'Ride the HybridBus-1',
                  
                  'Walk to the TrollyBus-1', 
                  'Wait for the TrollyBus-1', 
                  'Ride the TrollyBus-1', 
                  
                  'Walk to the TrollyBus-2',
                  'Wait for the TrollyBus-2', 
                  'Ride the TrollyBus-2', 
                  
                  'Walk to the HybridBus-2',
                  'Wait for the HybridBus-2',
                  'Ride the HybridBus-2', 
                  
                  'Walk to the Finish point']


df_sorted = df_trans[listforbarname]
df_sorted = df_sorted.transpose()

import numpy as np; np.random.seed(1)
import pandas as pd
import seaborn.apionly as sns
import matplotlib.pyplot as plt

#list_colors = ['g','b','y','g','b','y','g','b','y','g','b','y','r']
list_colors = ['g','b','gold','g','b','gold','g','b','gold','g','b','gold','r']


fig = plt.figure(figsize=(8,3))
p = df_sorted['Peak'].plot(kind="bar", width = 0.8, color=list_colors, alpha = 0.6, fontsize=12)
p.set_title("Average of all rounds", fontsize=12)
p.set_xlabel(" ")
p.set_ylabel("Number of SCR / minute", fontsize=12)
fig.savefig("EventArousals_"+city+".pdf",bbox_inches='tight')
fig.savefig("EventArousals_"+city+".jpg",bbox_inches='tight')
plt.show()
plt.close(fig)
fig.clear
