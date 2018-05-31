# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 09:57:14 2018

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
city = "ML"
path_raw_data_files = os.path.join(path_raw_data_files, "Data_"+city)
path_raw_data_files = os.path.join(path_raw_data_files,"for_stat")

os.chdir(path_raw_data_files)
#%% line chart
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md # for date in x axis
import datetime as dt
import time

data_participant = pd.read_csv("merged_data.csv")
#data_participant = data_participant.drop(['Unnamed: 0'], axis=1)

dictionary = {}
if(city == "ZH"):
    rageList = [2,3,4,5,6,7,8,9,10]  # ZH
    dictionary[2] = data_participant[data_participant['PID'] == 2]
    dictionary[3] = data_participant[data_participant['PID'] == 3]
    dictionary[4] = data_participant[data_participant['PID'] == 4]
    dictionary[5] = data_participant[data_participant['PID'] == 5]
    dictionary[6] = data_participant[data_participant['PID'] == 6]
    dictionary[7] = data_participant[data_participant['PID'] == 7]
    dictionary[8] = data_participant[data_participant['PID'] == 8]
    dictionary[9] = data_participant[data_participant['PID'] == 9]
    dictionary[10] = data_participant[data_participant['PID'] == 10]    
elif(city == "SG"):
    rageList = [1,2,3,4,5,6,7,8,9]  # SG
    dictionary[1] = data_participant[data_participant['PID'] == 1]   
    dictionary[2] = data_participant[data_participant['PID'] == 2]
    dictionary[3] = data_participant[data_participant['PID'] == 3]
    dictionary[4] = data_participant[data_participant['PID'] == 4]
    dictionary[5] = data_participant[data_participant['PID'] == 5]
    dictionary[6] = data_participant[data_participant['PID'] == 6]
    dictionary[7] = data_participant[data_participant['PID'] == 7]
    dictionary[8] = data_participant[data_participant['PID'] == 8]
    dictionary[9] = data_participant[data_participant['PID'] == 9] 
    
elif(city == "HK"):
    rageList = [2,4]  # HK  
    dictionary[2] = data_participant[data_participant['PID'] == 2]
    dictionary[4] = data_participant[data_participant['PID'] == 4]    
elif(city == "CN"):
    rageList = [1,4]  # CN
    dictionary[1] = data_participant[data_participant['PID'] == 1]
    dictionary[4] = data_participant[data_participant['PID'] == 4]
else:
    rageList = [1,6]  # ML
    dictionary[1] = data_participant[data_participant['PID'] == 1]
    dictionary[6] = data_participant[data_participant['PID'] == 6]
#%% Manupulation for CSV file generation
#data_frame = pd.DataFrame({"A": []})
#data_dic = {}
#for i in [1,2,3,4,5,6,7,8,9]:
#    data_pid = dictionary[i]
#    #data_frame['P'+str(i)] = data_pid['tonicSCL'].tolist()
#    data_dic[i] = data_pid['tonicSCL'].tolist()
#
#(pd.DataFrame.from_dict(data=data_dic, orient='index')
#   .to_csv('event_peak.csv', header=False))


data_diff_dictionary = {}    
if(city == "ZH"):
    rageList = [2,3,4,5,6,7,8,9,10]  # ZH
elif(city == "SG"):
    rageList = [1,2,3,4,5,6,7,8,9]  # SG
elif(city == "HK"):
    rageList = [2,4]  # HK    
else:
    rageList = [1,4]  # ML
    
for i in rageList:  
    #i = 4
    print(i)
    participant = i
    data_pid = dictionary[i]
    if(city == "ZH"):
        data_filter = data_pid[['Temp','RH','Lux','Sound','TTP_peak','TTP_AmpUs','CDA_TonicUs']]    
    else:
        data_filter = data_pid[['HSTemp','HSRH','Sound','Lux','Wind','TTP_peak','TTP_AmpUs','CDA_TonicUs']]    
        
    data_diff = data_filter.diff(periods=20)        
    data_diff = data_diff.dropna()    
    data_diff_dictionary[i] = data_diff

frames = [data_diff_dictionary[d] for d in data_diff_dictionary]
result = pd.concat(frames)
result.to_csv('data_corr_diff.csv',index = False, header=True)
#%%  

from matplotlib.pyplot import cm 
from matplotlib import colors as mcolors  
import matplotlib.patches as mpatches # for patching legend on plots
N = 9
color = iter(cm.rainbow(np.linspace(0,1,N)))
colors = []
for i in range(N):
    colors.append(next(color))

if(city == "ZH"):
    rageList = [2,3,4,5,6,7,8,9,10]  # ZH
elif(city == "SG"):
    rageList = [1,2,3,4,5,6,7,8,9]  # SG
elif(city == "HK"):
    rageList = [2,4]  # HK
else:
    rageList = [1,4]  # ML

# dictionary for a file containg difference 
for i in rageList:  
    #i = 1
    print(i)
    participant = i
    data_pid = dictionary[i]

    #data_filter = data_pid[['Temp','RH','Lux','Sound','TTP_peak','TTP_AmpUs','CDA_TonicUs']]    
    data_filter = data_pid[['HSTemp','Sound','Lux','TTP_peak','TTP_AmpUs','CDA_TonicUs']]    

    absolute = True
    norm = False    
    ### absolute 
    if(absolute == True):
        data_diff = data_filter
        Type = "Abs"
    else:
        ### diffiernce per minute
        data_diff = data_filter.diff(periods=20)
        Type = ""
        
    
    data_diff = data_diff.dropna()    
    pid_list = data_pid.index.tolist()
    dif_list =  data_diff.index.tolist()
    matches  = [x for x in pid_list if (x in dif_list)]    
    event_data = data_pid["EvenName"][matches]
    #data_diff['EvenName'] = event_data.tolist()
    ##for ZH data  

    listEvenNum = []

    #define fill boundries
    # check np.unique(status) for available status
    if(city == "ZH"):  
        for j in range(len(event_data)):
            if (event_data[matches[j]].startswith('ride80')):
                listEvenNum.append(2)
            elif (event_data[matches[j]].startswith('ride32')):
                    listEvenNum.append(1.5)
            elif (event_data[matches[j]].startswith('wait80')):
                    listEvenNum.append(1)
            elif (event_data[matches[j]].startswith('wait32')):
                    listEvenNum.append(0.5)
            elif (event_data[matches[j]].startswith('walk')):
                    listEvenNum.append(0)
            else:
                listEvenNum.append(-1)       
        #data_diff["EventName"]  = listEvenNum
        
        rideH   = 2 # -1 to 0    
        rideE   = 1.5 # -1 to 0        
        waitH   = 1 # -1 to 0
        waitE   = 0.5 # -1 to 
        walk    = 0 # -1 to 0
        unknown = -1 # -1 to 0
        #colors
        c_rideH   = 'm'
        c_rideE   = 'r'
        c_waitH   = 'g'
        c_waitE   = 'c' 
        c_walk    = 'b' 
        c_unknown = 'k' 
    else:
        for j in range(len(event_data)):
            if (event_data[matches[j]].startswith('ride')):
                listEvenNum.append(2)
            elif (event_data[matches[j]].startswith('wait')):
                    listEvenNum.append(1)
            elif (event_data[matches[j]].startswith('walk')):
                    listEvenNum.append(0)
            else:
                listEvenNum.append(-1)            
        #data_diff["EventName"]  = listEvenNum
        rideH   = 2 # -1 to 0    
        rideE   = 2 # -1 to 0        
        waitH   = 1 # -1 to 0
        waitE   = 1 # -1 to 
        walk    = 0 # -1 to 0
        unknown = -1 # -1 to 0
        # colors
        c_rideH   = 'r'
        c_rideE   = 'r'
        c_waitH   = 'g'
        c_waitE   = 'g' 
        c_walk    = 'b' 
        c_unknown = 'k' 

    
    timestamps = data_pid['Time'][data_diff.index]
    dates = [dt.datetime.fromtimestamp(ts) for ts in timestamps]
    #dates = [ts.time() for ts in dates]
    datenums=md.date2num(dates)
    
    
    
    #temp = np.asarray(data_diff['Temp'])
    temp = np.asarray(data_diff['HSTemp'])
    sound = np.asarray(data_diff['Sound'])
    sound = sound.astype(np.float)    
    #sound = np.zeros(temp.size)
    lux = np.asarray(data_diff['Lux'])
    #scl = np.asarray(data_diff['tonicSCL_0p05'])    
    scl = np.asarray(data_diff['CDA_TonicUs'])
    ampUs = np.asarray(data_diff['TTP_AmpUs'])
    peak = np.asarray(data_diff['TTP_peak'])
    
    status = np.asarray(listEvenNum)
    
    #checkin with normalization
    if(norm == True):
        Type = "Norm"
        x = temp
        temp =  (x-min(x))/(max(x)-min(x))
         
        #x = sound
        #sound =  (x-min(x))/(max(x)-min(x))
        
        x = lux
        lux =  (x-min(x))/(max(x)-min(x))
         
        x = scl
        scl =  (x-min(x))/(max(x)-min(x))
        
#        x = scr
#        scr =  (x-min(x))/(max(x)-min(x))
        
        x = ampUs
        ampUs =  (x-min(x))/(max(x)-min(x))
        
        x = peak
        peak =  (x-min(x))/(max(x)-min(x))
    
        #x = status
        #status =  (x-min(x))/(max(x)-min(x))
    


    #define plot condiations
    fig, ax = plt.subplots(figsize=(10, 12))
    # Environment variable charts
    axTemp = plt.subplot(611)    
    plt.plot(datenums,temp, 'blue')
    plt.setp(axTemp.get_xticklabels(), visible=False)
    axTemp.set_ylabel("Temp")
    plt.legend(['Temp'], loc='upper left',bbox_to_anchor=(1, 1))    

    
    axSound = plt.subplot(612, sharex=axTemp)
    plt.plot(datenums,sound, 'turquoise')
    plt.setp(axSound.get_xticklabels(), visible=False)
    axSound.set_ylabel("Sound")
    plt.legend(['Sound'], loc='upper left',bbox_to_anchor=(1, 1))   
    
    axLux = plt.subplot(613, sharex=axTemp)
    plt.plot(datenums,lux, 'orangered')
    plt.setp(axLux.get_xticklabels(), visible=False)
    axLux.set_ylabel("Lux")
    plt.legend(['Lux'], loc='upper left',bbox_to_anchor=(1, 1))    
    
    #Skin conducatence charts
    axSCL = plt.subplot(614, sharex=axTemp)
    plt.plot(datenums,scl, 'slateblue')
    plt.setp(axSCL.get_xticklabels(), visible=False)
    axSCL.set_ylabel(" SCL")
    plt.legend(['SCL'], loc='upper left',bbox_to_anchor=(1, 1))
    
#    axSCR = plt.subplot(715, sharex=axTemp)
#    plt.plot(datenums,scr, 'mediumslateblue')
#    plt.setp(axSCR.get_xticklabels(), visible=False)
#    axSCR.set_ylabel(" SCR")
#    plt.legend(['SCR',], loc='upper left',bbox_to_anchor=(1, 1))
    
    axampUs = plt.subplot(615, sharex=axTemp)
    plt.plot(datenums,ampUs, 'seagreen')
    plt.setp(axampUs.get_xticklabels(), visible=False)
    axampUs.set_ylabel("Amp $\mu$S")
    plt.legend(['Amp $\mu$S',], loc='upper left', bbox_to_anchor=(1, 1))
    
    axpeak = plt.subplot(616, sharex=axTemp)
    plt.plot(datenums,peak, 'seagreen')
    #plt.setp(axpeak.get_xticklabels(), visible=False)
    axpeak.set_ylabel(" Peak")
    xfmt = md.DateFormatter('%H:%M:%S')
    axpeak.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=25 )

    axTemp.fill_between(datenums,temp, temp.min(), where = status == unknown, facecolor = c_unknown, alpha=0.2, lw = 2, edgecolor='k')
    axTemp.fill_between(datenums,temp, temp.min(), where = status == walk, facecolor=  c_walk, alpha=0.1, lw =  1, edgecolor='k')
    axTemp.fill_between(datenums,temp, temp.min(), where = status == waitH, facecolor= c_waitH, alpha=0.1, lw = 1, edgecolor='k')
    axTemp.fill_between(datenums,temp, temp.min(), where = status == waitE, facecolor= c_waitE, alpha=0.1, lw = 1, edgecolor='k')
    axTemp.fill_between(datenums,temp, temp.min(), where = status == rideH, facecolor= c_rideH, alpha=0.1, lw = 1, edgecolor='k')
    axTemp.fill_between(datenums,temp, temp.min(), where = status == rideE, facecolor= c_rideE, alpha=0.1, lw = 1, edgecolor='k')

    axSound.fill_between(datenums,sound, sound.min(), where = status == unknown, facecolor = c_unknown, alpha=0.2, lw = 2, edgecolor='k')
    axSound.fill_between(datenums,sound, sound.min(), where = status == walk, facecolor=  c_walk, alpha=0.1, lw =  1, edgecolor='k')
    axSound.fill_between(datenums,sound, sound.min(), where = status == waitH, facecolor= c_waitH, alpha=0.1, lw = 1, edgecolor='k')
    axSound.fill_between(datenums,sound, sound.min(), where = status == waitE, facecolor= c_waitE, alpha=0.1, lw = 1, edgecolor='k')
    axSound.fill_between(datenums,sound, sound.min(), where = status == rideH, facecolor= c_rideH, alpha=0.1, lw = 1, edgecolor='k')
    axSound.fill_between(datenums,sound, sound.min(), where = status == rideE, facecolor= c_rideE, alpha=0.1, lw = 1, edgecolor='k')


    axLux.fill_between(datenums,lux, lux.min(), where = status == unknown, facecolor = c_unknown, alpha=0.2, lw = 2, edgecolor='k')
    axLux.fill_between(datenums,lux, lux.min(), where = status == walk, facecolor= c_walk, alpha=0.1, lw =  1, edgecolor='k')
    axLux.fill_between(datenums,lux, lux.min(), where = status == waitH, facecolor= c_waitH, alpha=0.1, lw = 1, edgecolor='k')
    axLux.fill_between(datenums,lux, lux.min(), where = status == waitE, facecolor= c_waitE, alpha=0.1, lw = 1, edgecolor='k')
    axLux.fill_between(datenums,lux, lux.min(), where = status == rideH, facecolor= c_rideH, alpha=0.1, lw = 1, edgecolor='k')
    axLux.fill_between(datenums,lux, lux.min(), where = status == rideE, facecolor= c_rideE, alpha=0.1, lw = 1, edgecolor='k')

    axSCL.fill_between(datenums,scl, scl.min(), where = status == unknown, facecolor = c_unknown, alpha=0.2, lw = 2, edgecolor='k')
    axSCL.fill_between(datenums,scl, scl.min(), where = status == walk, facecolor= c_walk, alpha=0.1, lw =  1, edgecolor='k')
    axSCL.fill_between(datenums,scl, scl.min(), where = status == waitH, facecolor= c_waitH, alpha=0.1, lw = 1, edgecolor='k')
    axSCL.fill_between(datenums,scl, scl.min(), where = status == waitE, facecolor= c_waitE, alpha=0.1, lw = 1, edgecolor='k')
    axSCL.fill_between(datenums,scl, scl.min(), where = status == rideH, facecolor= c_rideH, alpha=0.1, lw = 1, edgecolor='k')
    axSCL.fill_between(datenums,scl, scl.min(), where = status == rideE, facecolor= c_rideE, alpha=0.1, lw = 1, edgecolor='k')

#    axSCR.fill_between(datenums,scr, scr.min(), where = status == unknown, facecolor = c_unknown, alpha=0.2, lw = 2, edgecolor='k')
#    axSCR.fill_between(datenums,scr, scr.min(), where = status == walk, facecolor= c_walk, alpha=0.1, lw =  1, edgecolor='k')
#    axSCR.fill_between(datenums,scr, scr.min(), where = status == waitH, facecolor= c_waitH, alpha=0.1, lw = 1, edgecolor='k')
#    axSCR.fill_between(datenums,scr, scr.min(), where = status == waitE, facecolor= c_waitE, alpha=0.1, lw = 1, edgecolor='k')
#    axSCR.fill_between(datenums,scr, scr.min(), where = status == rideH, facecolor= c_rideH, alpha=0.1, lw = 1, edgecolor='k')
#    axSCR.fill_between(datenums,scr, scr.min(), where = status == rideE, facecolor= c_rideE, alpha=0.1, lw = 1, edgecolor='k')

    axampUs.fill_between(datenums,ampUs, ampUs.min(), where = status == unknown, facecolor = c_unknown, alpha=0.2, lw = 2, edgecolor='k')
    axampUs.fill_between(datenums,ampUs, ampUs.min(), where = status == walk, facecolor= c_walk, alpha=0.1, lw =  1, edgecolor='k')
    axampUs.fill_between(datenums,ampUs, ampUs.min(), where = status == waitH, facecolor= c_waitH, alpha=0.1, lw = 1, edgecolor='k')
    axampUs.fill_between(datenums,ampUs, ampUs.min(), where = status == waitE, facecolor= c_waitE, alpha=0.1, lw = 1, edgecolor='k')
    axampUs.fill_between(datenums,ampUs, ampUs.min(), where = status == rideH, facecolor= c_rideH, alpha=0.1, lw = 1, edgecolor='k')
    axampUs.fill_between(datenums,ampUs, ampUs.min(), where = status == rideE, facecolor= c_rideE, alpha=0.1, lw = 1, edgecolor='k')

    axpeak.fill_between(datenums,peak, peak.min(), where = status == unknown, facecolor = c_unknown, alpha=0.2, lw = 2, edgecolor='k')
    axpeak.fill_between(datenums,peak, peak.min(), where = status == walk, facecolor= c_walk, alpha=0.1, lw =  1, edgecolor='k')
    axpeak.fill_between(datenums,peak, peak.min(), where = status == waitH, facecolor= c_waitH, alpha=0.1, lw = 1, edgecolor='k')
    axpeak.fill_between(datenums,peak, peak.min(), where = status == waitE, facecolor= c_waitE, alpha=0.1, lw = 1, edgecolor='k')
    axpeak.fill_between(datenums,peak, peak.min(), where = status == rideH, facecolor= c_rideH, alpha=0.1, lw = 1, edgecolor='k')
    axpeak.fill_between(datenums,peak, peak.min(), where = status == rideE, facecolor= c_rideE, alpha=0.1, lw = 1, edgecolor='k')


     #ax3 = plt.subplot(313, sharex=ax1, sharey=ax1)
#    axStatus = plt.subplot(818, sharex=axTemp )
#    plt.plot(datenums,status, 'black')
#    xfmt = md.DateFormatter('%H:%M:%S')
#    axStatus.xaxis.set_major_formatter(xfmt)
#    plt.xticks(rotation=25 )
#    axStatus.set_ylabel("Status")
    #plt.legend(['Peak',], loc='upper left')
    l0 = mpatches.Patch(color='seagreen', alpha = 1, label="Peak")
    l1 = mpatches.Patch(color=c_unknown, alpha = 0.2, label="unknown")
    l2 = mpatches.Patch(color=c_walk, alpha = 0.1, label="walk")
    l3 = mpatches.Patch(color=c_waitH, alpha = 0.1, label="wait H")
    l4 = mpatches.Patch(color=c_waitE, alpha = 0.1, label="wait ")
    l5 = mpatches.Patch(color=c_rideH, alpha = 0.1, label="ride H")
    l6 = mpatches.Patch(color=c_rideE, alpha = 0.1, label="ride ")
    #plt.legend(handles=[l0,l1,l2,l3,l4,l5,l6],bbox_to_anchor=(1, 1))
    plt.legend(handles=[l0,l1,l2,l4,l6],bbox_to_anchor=(1, 1)) # for Ml
    #plt.legend(['Status (-1:unknown, 0:walk, 0-1:wait, 1-2:ride)'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, borderaxespad=0.)
   
    axpeak.set_xlabel("\n Time progress P"+str(participant)+'\n')    

    fig.savefig(city+"_"+Type+"_Line_P"+str(participant)+".pdf",bbox_inches='tight')
    fig.savefig(city+"_"+Type+"_Line_P"+str(participant)+".jpg",bbox_inches='tight')
    plt.show()
    plt.close(fig)