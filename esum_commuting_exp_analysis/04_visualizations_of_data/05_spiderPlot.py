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

city = "ZH"

dataof = "Data_"+city
path_raw_data_files = os.path.join(path_raw_data_files, dataof)
path_raw_data_files = os.path.join(path_raw_data_files,"for_stat")

os.chdir(path_raw_data_files)

#%% line chart

data_participant = pd.read_csv("event_scl_peak.csv")
#data_participant = pd.read_csv("event_avg_tonicP1.csv")
#data_participant = data_participant.drop(['Unnamed: 0'], axis=1)
#%%
plot = "peak"
Type = "event_"+plot
df = data_participant

# ------- PART 1: Create background
 
# number of variable
categories=list(df)[1:]
N = len(categories)
 
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
 

#define plot condiations
fig, ax = plt.subplots(figsize=(8, 8))
# Initialise the spider plot
ax = plt.subplot(111, polar=True)
 
# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
 
# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories,  fontsize=16)
 
# Draw ylabels
ax.set_rlabel_position(0)
#plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
#plt.ylim(0,40)
 
 
# ------- PART 2: Add plots
 
# Plot each individual = each line of the data
# I don't do a loop, because plotting more than 3 groups makes the chart unreadable


if(plot == "SCL"):
    # SCL
    values=df.loc[3].drop('Participant').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, linestyle='solid', label="Avg. SCL ($\mu$S) per min")
    ax.fill(angles, values, 'b', alpha=0.1)
else:
    # Peak
    values=df.loc[1].drop('Participant').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, linestyle='solid', label="Avg. # peak per min")
    ax.fill(angles, values, 'r', alpha=0.2)

## Ind1
#values=df.loc[0].drop('Participant').values.flatten().tolist()
#values += values[:1]
#ax.plot(angles, values, linewidth=1, linestyle='solid', label="P1")
#ax.fill(angles, values, 'b', alpha=0.1)
# 
## Ind2
#values=df.loc[1].drop('Participant').values.flatten().tolist()
#values += values[:1]
#ax.plot(angles, values, linewidth=1, linestyle='solid', label="P2")
#ax.fill(angles, values, 'r', alpha=0.1)
#
## Ind3
#values=df.loc[2].drop('Participant').values.flatten().tolist()
#values += values[:1]
#ax.plot(angles, values, linewidth=1, linestyle='solid', label="P3")
#ax.fill(angles, values, 'r', alpha=0.1)
#
## Ind4
#values=df.loc[3].drop('Participant').values.flatten().tolist()
#values += values[:1]
#ax.plot(angles, values, linewidth=1, linestyle='solid', label="P4")
#ax.fill(angles, values, 'r', alpha=0.1)
#
#
## Ind5
#values=df.loc[4].drop('Participant').values.flatten().tolist()
#values += values[:1]
#ax.plot(angles, values, linewidth=1, linestyle='solid', label="P5")
#ax.fill(angles, values, 'r', alpha=0.1)
# 
## Ind5
#values=df.loc[5].drop('Participant').values.flatten().tolist()
#values += values[:1]
#ax.plot(angles, values, linewidth=1, linestyle='solid', label="P6")
#ax.fill(angles, values, 'r', alpha=0.1)
#
## Ind5
#values=df.loc[6].drop('Participant').values.flatten().tolist()
#values += values[:1]
#ax.plot(angles, values, linewidth=1, linestyle='solid', label="P7")
#ax.fill(angles, values, 'r', alpha=0.1)
#
## Ind6
#values=df.loc[7].drop('Participant').values.flatten().tolist()
#values += values[:1]
#ax.plot(angles, values, linewidth=1, linestyle='solid', label="P8")
#ax.fill(angles, values, 'r', alpha=0.1)

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 0), fontsize=12)

fig.savefig(city+"_"+Type+".pdf",bbox_inches='tight')
fig.savefig(city+"_"+Type+".jpg",bbox_inches='tight')
plt.show()
plt.close(fig)
