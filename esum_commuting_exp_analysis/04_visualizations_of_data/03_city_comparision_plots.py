# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 09:03:51 2018

@author: vojha
"""
#Reset all varables
%reset -f
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

path_ZH_data_files = os.path.join(path_raw_data_files, "Data_ZH")
path_ZH_data_files = os.path.join(path_ZH_data_files,"for_stat")

path_SG_data_files = os.path.join(path_raw_data_files, "Data_SG")
path_SG_data_files = os.path.join(path_SG_data_files,"for_stat")

os.chdir(path_raw_data_files)
#%%

data_participant_zh = pd.read_csv(os.path.join(path_ZH_data_files,"merged_data.csv"))
data_participant_zh = data_participant_zh.drop(['Unnamed: 0'], axis=1)

# eventwise EDA peak data preparation 
data_grouped_event_zh = data_participant_zh.groupby(['EvenName'])
df_mean_zh = data_grouped_event_zh.mean()
#removing unknun data
df_mean_zh = df_mean_zh[df_mean_zh.index != "unknown"] #removing unknun data
df_mean_zh = df_mean_zh[df_mean_zh.index != "S"] #removing unknun data
eventnames_zh = df_mean_zh.index.tolist()
data_eda_peak_zh = []
for i in range(len(eventnames_zh)):
    data_eda_peak_zh.append (data_participant_zh[data_participant_zh["EvenName"] == eventnames_zh[i]]["Temp"].tolist())

#
data_participant_sg = pd.read_csv(os.path.join(path_SG_data_files,"merged_data.csv"))
data_participant_sg = data_participant_sg.drop(['Unnamed: 0'], axis=1)

# eventwise EDA peak data preparation 
data_grouped_event_sg = data_participant_sg.groupby(['EvenName'])
df_mean_sg = data_grouped_event_sg.mean()
#removing unknun data
df_mean_sg = df_mean_sg[df_mean_sg.index != "unknown"] #removing unknun data
df_mean_sg = df_mean_sg[df_mean_sg.index != "S"] #removing unknun data
eventnames_sg = df_mean_sg.index.tolist()
data_eda_peak_sg = []
for i in range(len(eventnames_sg)):
    data_eda_peak_sg.append (data_participant_sg[data_participant_sg["EvenName"] == eventnames_sg[i]]["HSTemp"].tolist())


#%%PLOT
a = data_eda_peak_zh[0] + data_eda_peak_zh[1] + data_eda_peak_zh[2] + data_eda_peak_zh[3]
b = data_eda_peak_sg[0] + data_eda_peak_sg[1] + data_eda_peak_sg[2]
c = data_eda_peak_zh[4] + data_eda_peak_zh[5] + data_eda_peak_zh[6] + data_eda_peak_zh[7]
d = data_eda_peak_sg[3] + data_eda_peak_sg[4] + data_eda_peak_sg[5]
e = data_eda_peak_zh[8]
f = data_eda_peak_sg[6]


#t2, p2 = stats.ttest_ind(a,b, equal_var = False)
#print("t = " + str(t2))
#print("p = " + str(2*p2))

ma = np.mean(a)
mb = np.mean(b)
mc = np.mean(c)
md = np.mean(d)
me = np.mean(e)
mf = np.mean(f)


listlength = [len(a),len(b),len(c),len(d),len(e),len(f)]
print(listlength)
listforbarname = ["Ride ZH", "Ride SG", "Wait ZH", "Wait SG", "Walk ZH", "Walk SG"]
listforbar = [ma,mb,mc,md,me,mf]
print(listforbar)

#from sklearn import preprocessing
#
#ride = [len(a),len(b)]
#ride = [float(i)/sum(ride) for i in ride]
#
#wait = [len(c),len(d)]
#wait = [float(i)/sum(wait) for i in wait]
#
#walk = [len(c),len(d)]
#walk = [float(i)/sum(walk) for i in walk]

#listNormVal = [ride[0],ride[1],wait[0],wait[1],walk[0],walk[1]]
#print(listNormVal)
#
#ma = ma/(ride[0])
#mb = mb/(ride[1])
#mc = mc/(wait[0])
#md = md/(wait[1])
#me = me/(walk[0])
#mf = mf/(walk[1])
#
#listforbarN = [ma,mb,mc,md,me,mf]
#print(listforbarN)
#
#listpercengtage = [(z*100)/y   for y,z in zip(listforbarN,listforbar)]
#print(listpercengtage)
#

n = len(listforbar)
import matplotlib.pyplot as plt; plt.rcdefaults()
from matplotlib.pyplot import cm 
color = iter(cm.rainbow(np.linspace(0,1,n)))
colors = []
for i in range(n):
    colors.append(next(color))


listforbarname = ["Ride ZH", "Ride SG", "Wait ZH", "Wait SG", "Walk ZH", "Walk SG"]
#p = df_mean['peak'].plot(kind="bar",yerr=df_std['peak'])
#fig = plt.figure(figsize=(9, 7))
fig, ax = plt.subplots(figsize=(9, 7))
plt.bar(listforbarname,listforbar,color = colors)
#plt.show()
ax.set_title("Average temperature per time window")
ax.set_xlabel("\n Events: SG-Singapore and ZH-Zurich")
ax.set_ylabel("Average  temperature")
plt.show()
fig.savefig('temp_ZH_SG.pdf')
fig.savefig('temp_ZH_SG.jpg')
plt.close(fig)

#%%
fig = plt.figure(figsize=(9, 7))
p = df_mean_sg["Sound"].plot(kind="bar")
p.set_title("Event wise average SCR")
p.set_xlabel("Event Type (E-Electric bus, H-Hybrid bus)")
p.set_ylabel("SCR")
fig.savefig('Sound_sg.pdf')
fig.savefig('Sound_sg.jpg')
plt.close(fig)
fig.clear

import pylab
df2 = df_mean_zh
del df2["PID"]
del df2["Time"]
del df2["Lux"]

df2 = df2[["Temp","peak"]]
df2.plot.bar();
pylab.show()
#%%

data_participant_zh = pd.read_csv(os.path.join(path_ZH_data_files,"merged_data_evn_div.csv"))
data_participant_zh = data_participant_zh.drop(['Unnamed: 0'], axis=1)

data_participant_zh = data_participant_zh[['Temp','RH','Lux','Sound','peak','phase','EvenName']]
data_participant_zh = data_participant_zh[data_participant_zh['EvenName'] != 'S']
data_participant_zh = data_participant_zh[data_participant_zh['EvenName'] != 'unknown']
data_participant_zh.to_csv("fileter_all_zh.csv")