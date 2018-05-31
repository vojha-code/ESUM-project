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

import seaborn.apionly as sns
import matplotlib.pyplot as plt
from scipy import stats
#%% Path setting to the folder wher the raw files are 
city = "HK"

path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_"+city)
path_raw_data_files = os.path.join(path_raw_data_files,"for_stat")

os.chdir(path_raw_data_files)
#%%
np.random.seed(1)
data_participant = pd.read_csv("merged_data.csv")
data_participant = data_participant.drop(['Unnamed: 0'], axis=1)

#data_participant = pd.read_csv("data_corr_diff.csv")
# Generate a random dataset
#cols = [s*4 for s in list("ABCD")]
#df = pd.DataFrame(data=np.random.rayleigh(scale=5, size=(100, 4)), columns=cols)

# Compute the correlation matrix
#corr = df.corr()
#print(corr)

data_participant_cut = data_participant
#data_participant_cut = data_participant[data_participant['EvenName'].str.startswith('walk')]
if (city == "ZH"):
    df_col_sel = data_participant_cut[['Temp','RH','Sound','Lux','peakSCR_0p05','phasicSCR_0p05','tonicSCL_0p05']]    
    new_names = ['Temp','RH','Sound','Lux','nSCR','SCR', 'SCL']
if (city == "ZH"):
    df_col_sel = data_participant_cut[['Temp','RH','Sound','Lux','peakSCR_0p05','phasicSCR_0p05','tonicSCL_0p05']]    
    new_names = ['Temp','RH','Sound','Lux','nSCR','SCR', 'SCL']    
else:
    df_col_sel = data_participant_cut[['HSTemp','HSRH','Wind','Sound','Lux','peakSCR_0p05','phasicSCR_0p05','tonicSCL_0p05']] 
    new_names = ['Temp','RH','Wind','Sound','Lux','nSCR', 'SCR','SCL']

df_col_sel = df_col_sel.copy(deep=True)
old_names = df_col_sel.columns
df_col_sel.rename(columns=dict(zip(old_names, new_names)), inplace=True)
df_col_sel.to_csv('data_corr.csv',index = False, header=True)

corr = df_col_sel.corr()
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(8.5, 7.5))

# Draw the heatmap with the mask and correct aspect ratio
vmax = np.abs(corr.values[~mask]).max()
sns.heatmap(corr, mask=mask, cmap=plt.cm.BuGn, vmin=vmax, vmax=vmax,
            square=True, linecolor="lightgray", linewidths=1, ax=ax)

for i in range(len(corr)):
    #ax.text(i+0.5,len(corr)-(i+0.5), corr.columns[i], 
            #ha="center", va="center", rotation=45)
    for j in range(i+1, len(corr)):
        s = "{:.2f}".format(corr.values[i,j])
        ax.text(j+0.5,(i+0.5),s, ha="center", va="center", fontsize=12)
#ax.axis("off")
plt.show()

fig.savefig(city+"_corre_abs.pdf")
fig.savefig(city+"_corre_abs.jpg")
#corr.to_csv("correlation_matrix.csv")

