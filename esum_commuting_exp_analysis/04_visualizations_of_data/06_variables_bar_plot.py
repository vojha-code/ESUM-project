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
from math import pi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md # for date in x axis
import datetime as dt
from scipy import stats

#%% Path setting to the folder wher the raw files are 
path_raw_data_files = "C:/Users/vojha/Documents/ETH_project_data/BusStopProjectData"
city = "SG"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_"+city)
path_raw_data_files = os.path.join(path_raw_data_files,"for_stat")

os.chdir(path_raw_data_files)
#%% line chart

data_participant = pd.read_csv("event_scl_peak.csv")
#data_participant = pd.read_csv("event_avg_tonicP1.csv")
#data_participant = data_participant.drop(['Unnamed: 0'], axis=1)

column = data_participant["Participant"].tolist()
del data_participant["Participant"]
data_participant = data_participant.transpose()
data_participant.columns = column

#%% setting variable and bar plot
    
scl =  data_participant["SCL"]
peak =  data_participant["Peak"]

time = data_participant["Time"]

temp = data_participant["Temp"]
rh = data_participant["RH"]
sound = data_participant["Sound"]
lux = data_participant["Lux"]

#time = time.sort_values(ascending=False)
#temp = temp.sort_values(ascending=False)
#rh = rh.sort_values(ascending=False)
#sound = sound.sort_values(ascending=False)
#lux = lux.sort_values(ascending=False)




variable = "time"
x = time.index.tolist()
y = time.sort_values(ascending=False)

#variable = "temp"
#x = temp.index.tolist()
#y = temp

#variable = "rh"
#x = rh.index.tolist()
#y = rh
#
#variable = "sound"
#x = sound.index.tolist()
#y = sound
#
#variable = "lux"
#x = lux.index.tolist()
#y = lux



# Need correction i thsi code
#plt.rcdefaults()
#fig, ax = plt.subplots(figsize=(2, 4))
#width = 0.5 # the width of the bars
#
#ax.barh(x, y, width, align='center', color='blue', alpha = 0.3)
#ax.set_yticks(x)
#ax.set_yticklabels(x, minor=False)
#ax.invert_yaxis()  # labels read top-to-bottom
##ax.set_xlabel()
#ax.set_title('Time (in minutes)')
#for i, v in enumerate(y):
#    #ax.text(v + 0.5, i + .15, str(round(v)), color='gray', fontweight='bold')
#    ax.text(v + 1, i + .25, str(round(v,2)), color='gray', fontweight='bold')
##ax.axis("off")
#
## To hide the frame
#ax.set_frame_on(False)
#
## To hide ticks    
#cur_axes = plt.gca()
#cur_axes.axes.get_xaxis().set_ticks([])
##cur_axes.axes.get_yaxis().set_ticks([])
#
##cur_axes.axes.get_xaxis().set_visible(False)
##cur_axes.axes.get_yaxis().set_visible(False)
#
#plt.show()
#fig.savefig(city+"_barh_"+variable+".pdf",bbox_inches='tight')
#fig.savefig(city+"_barh_"+variable+".jpg",bbox_inches='tight')
#%%
from matplotlib.pyplot import cm 

n =9
color = iter(cm.rainbow(np.linspace(0,1,n)))
colors = []
for i in range(n):
    colors.append(next(color))

x = temp.index.tolist()
width = 0.5


fig, ax = plt.subplots(figsize=(3, 8))

axTime = plt.subplot(511)    
plt.bar(x, time, width, color = colors[0], alpha = 0.5)
plt.setp(axTime.get_xticklabels(), visible=False)
axTime.set_ylabel("Time (min)",fontsize=12)
ymin, ymax = axTime.get_ylim()
axTime.set_ylim(2, ymax)
  
axTemp = plt.subplot(512, sharex=axTime)    
plt.bar(x, temp, width, color = colors[8], alpha = 0.5)
plt.setp(axTemp.get_xticklabels(), visible=False)
axTemp.set_ylabel("Temp ($^o$C)",fontsize=12)
ymin, ymax = axTemp.get_ylim()
ymin = 25 #10#XH
axTemp.set_ylim(ymin, ymax)

axRh = plt.subplot(513, sharex=axTime)    
plt.bar(x, rh, width, color = colors[2], alpha = 0.6)
plt.setp(axRh.get_xticklabels(), visible=False)
axRh.set_ylabel("RH (%)",fontsize=12)
ymin, ymax = axRh.get_ylim()
ymin = 40
axRh.set_ylim(ymin, ymax)

axSound = plt.subplot(514, sharex=axTime)    
plt.bar(x, sound, width, color = colors[4], alpha = 0.8)
plt.setp(axSound.get_xticklabels(), visible=False)
axSound.set_ylabel("Sound (dB)",fontsize=12)
ymin, ymax = axSound.get_ylim()
ymin = 55
axSound.set_ylim(ymin, ymax)

axLux = plt.subplot(515, sharex=axTime)
plt.bar(x, lux, width, color = colors[6], alpha = 0.8)
plt.setp(axLux.get_xticklabels(), visible=True,fontsize=12)
axLux.set_ylabel("Light (lux)",fontsize=12)
ymin, ymax = axLux.get_ylim()
ymin = 0
axLux.set_ylim(ymin, ymax)
plt.xticks(rotation=90 )


plt.show()
fig.savefig(city+"_barh_all.pdf",bbox_inches='tight')
fig.savefig(city+"_barh_all.jpg",bbox_inches='tight')
#%%
#data_env["xticxs"] = data_env.index.tolist()
#data_env.index.tolist()
##fig = plt.figure(figsize=(9, 7))
#plot = data_env.plot( kind='area', alpha = 0.5)
##plot.set_title("Event wise average SCR")
##plot.set_xlabel("Event Type (E-Electric bus, H-Hybrid bus)")
#plot.set_xticks(data_env.index)
#plot.set_xticklabels(data_env.xticxs, rotation=45)
#plot.set_ylabel("SCR")
#plot.get_figure().savefig('ZH_env_area.pdf', format='pdf')
#plot.get_figure().savefig('ZH_env_area.jpg', format='jpg')
#

data_env = data_participant
del data_env["SCL"]
del data_env["Peak"]
del data_env["Lux"]

#%%
ax = data_env.plot()
ax.xticks(rotation=45)

# --- FORMAT 1
 
# Your x and y axis
x = data_participant.index 
# Basic stacked area chart.
plt.stackplot(x,time, temp, rh,sound, labels=['Time','Temp','RH', 'Sound'], alpha = 0.6)
plt.xticks(rotation=45)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

 














