# -*- coding: utf-8 -*-
"""

Created on Tue Feb 13 08:25:09 2018

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
path_raw_data_files = os.path.join(path_raw_data_files, "Data_SG")
path_raw_data_files = os.path.join(path_raw_data_files,"for_stat")

os.chdir(path_raw_data_files)
#%%

data_participant = pd.read_csv("merged_data.csv")
data_participant = data_participant.drop(['Unnamed: 0'], axis=1)

#%% plots
data_grouped_event = data_participant.groupby(['EvenName'])

df_mean = data_grouped_event.mean()
df_count = data_grouped_event.count()
df_std = data_grouped_event.std()
df_descrive = data_grouped_event.describe()



#removing unknun data
df_mean = df_mean[df_mean.index != "unknown"] #removing unknun data
df_count = df_count[df_count.index != "unknown"] #removing unknun data
df_std = df_mean[df_mean.index != "unknown"] #removing unknun data
#removing start data
df_mean = df_mean[df_mean.index != "S"] #removing unknun data
df_count = df_count[df_count.index != "S"] #removing unknun data
df_std = df_std[df_std.index != "S"] #removing unknun data

#rename index
df_mean["envetname"] = ['Ride 1','Ride 2','Ride 3','Wait 1','Wait 2', 'Wait 3','Walk']
df_mean = df_mean.set_index('envetname')

df_std["envetname"] = ['Ride 1','Ride 2','Ride 3','Wait 1','Wait 2', 'Wait 3','Walk']
df_std = df_std.set_index('envetname')

listcount = df_count['peak'].tolist()
print(listcount)
listcountN = [float(i)/sum(listcount) for i in listcount]
print(listcountN)
#percentage of increase in value

listforbarname = ['Ride 1','Ride 2','Ride 3','Wait 1','Wait 2', 'Wait 3','Walk']

listforbar = df_mean['phase'].tolist()
listforbarN = []
for i in range(len(listcountN)):
    listforbarN.append(listforbar[i]/listcountN[i])
print(listforbarN)
#%%
import matplotlib.pyplot as plt; plt.rcdefaults()

n = len(listforbar)
from matplotlib.pyplot import cm 
color = iter(cm.rainbow(np.linspace(0,1,n)))
colors = []
for i in range(n):
    colors.append(next(color))




#fig = plt.figure(figsize=(9, 7))
##p = df_mean['phase'].plot(kind="bar",yerr=df_std['peak'])
#p = df_mean['phase'].plot(kind="bar")
#p.set_title("Event wise average SCR")
#p.set_xlabel("Event Type")
#p.set_ylabel("Skin conductance response (phasic)")
#fig.savefig('EventArousals_wn.pdf')
#fig.savefig('EventArousals_wn.jpg')
#plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 7))
plt.bar(listforbarname,listforbarN,color = colors)
ax.set_title("Average dB per event (normilized for time)")
ax.set_xlabel("\n Events: Singapore")
ax.set_ylabel("Normalized Sound (dB)")
fig.savefig('EventArousals_SG_Sound.pdf')
fig.savefig('EventArousals_SG_Sound.jpg')
plt.close(fig)




#%% eventwise EDA peak data preparation 
data_grouped_event1 = data_participant.groupby(['EvenName'])
df_mean1 = data_grouped_event1.mean()
#removing unknun data
df_mean1 = df_mean1[df_mean1.index != "unknown"] #removing unknun data
df_mean1 = df_mean1[df_mean1.index != "S"] #removing unknun data
eventnames = df_mean1.index.tolist()
data_eda_peak = []
for i in range(len(eventnames)):
    data_eda_peak.append (data_participant[data_participant["EvenName"] == eventnames[i]]["phase"].tolist())
#
#for i in range(len(data_eda_peak)):
#    for j in range(len(data_eda_peak)):
#        if(i != j ):
#            a = data_eda_peak[i]
#            b = data_eda_peak[j]
#            t2, p2 = stats.ttest_ind(a,b)
#            print(eventnames[i],",",eventnames[j]," : t = " + str(t2), " p = " + str(2*p2))
#            
# Cross Checking with the internal scipy function
a = data_eda_peak[0]
b = data_eda_peak[2]

t2, p2 = stats.ttest_ind(a,b, equal_var = False)
print("t = " + str(t2))
print("p = " + str(2*p2))
#Note that we multiply the p value by 2 because its a twp tail t-test
### You can see that after comparing the t statistic with the critical t value (computed internally) 
# we get a good p value of 0.0005 and thus we reject the null hypothesis and 
# thus it proves that the mean of the two distributions are different and statistically significant.

