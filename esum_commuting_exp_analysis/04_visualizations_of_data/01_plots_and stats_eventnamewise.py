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
#listcount = df_count['peakSCR'].tolist()
#print(listcount)
#listcountN = [float(i)/sum(listcount) for i in listcount]
#print(listcountN)
#percentage of increase in value

#listforbar = df_mean['Sound'].tolist()
#listforbarN = []
#for i in range(len(listcount)):
#    listforbarN.append(listforbar[i]/listcount[i])
#print(listforbarN)
##%%
#import matplotlib.pyplot as plt; plt.rcdefaults()
#
#n = len(df_mean['Sound'].tolist())
#from matplotlib.pyplot import cm 
#color = iter(cm.rainbow(np.linspace(0,1,n)))
#colors = []
#for i in range(n):
#    colors.append(next(color))
#
import numpy as np; np.random.seed(1)
import pandas as pd
import seaborn.apionly as sns
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(9,6))
p = df_sorted['Peak'].plot(kind="bar", color = "red", alpha = 0.4, fontsize=12)
p.set_title("Average of all rounds", fontsize=12)
p.set_xlabel(" ")
p.set_ylabel("Number of SCR/ minutes", fontsize=12)
fig.savefig("EventArousals_"+city+".pdf",bbox_inches='tight')
fig.savefig("EventArousals_"+city+".jpg",bbox_inches='tight')
plt.show()
plt.close(fig)
fig.clear


#fig, ax = plt.subplots(figsize=(10, 12))
#plt.bar(listforbarname,df_sorted['Peak'].tolist(), color = "red", alpha = 0.5)
#ax.set_ylabel("Number of SCR/ minutes")
#ax.set_title("Average of all rounds")
#plt.xticks(rotation=90 )
#fig.savefig("EventArousals_"+city+".pdf",bbox_inches='tight')
#fig.savefig("EventArousals_"+city+".jpg",bbox_inches='tight')
#plt.show()
#plt.close(fig)
#%% eventwise EDA peak data preparation 
#data_grouped_event1 = data_participant.groupby(['EvenName'])
#df_mean1 = data_grouped_event1.mean()
##removing unknun data
#df_mean1 = df_mean1[df_mean1.index != "unknown"] #removing unknun data
#df_mean1 = df_mean1[df_mean1.index != "S"] #removing unknun data
#eventnames = df_mean1.index.tolist()
#data_eda_peak = []
#for i in range(len(eventnames)):
#    data_eda_peak.append (data_participant[data_participant["EvenName"] == eventnames[i]]["phase"].tolist())
##
##for i in range(len(data_eda_peak)):
##    for j in range(len(data_eda_peak)):
##        if(i != j ):
##            a = data_eda_peak[i]
##            b = data_eda_peak[j]
##            t2, p2 = stats.ttest_ind(a,b)
##            print(eventnames[i],",",eventnames[j]," : t = " + str(t2), " p = " + str(2*p2))
##            
## Cross Checking with the internal scipy function
#a = data_eda_peak[0]
#b = data_eda_peak[1]
#
#print(np.mean(a),np.mean(b))
#
#t2, p2 = stats.ttest_ind(a,b, equal_var = False)
#print("t = " + str(t2))
#print("p = " + str(2*p2))
##Note that we multiply the p value by 2 because its a twp tail t-test
#### You can see that after comparing the t statistic with the critical t value (computed internally) 
## we get a good p value of 0.0005 and thus we reject the null hypothesis and 
## thus it proves that the mean of the two distributions are different and statistically significant.

#%%
import numpy as np
import matplotlib.pyplot as plt

N =  len(df_mean)
ind = np.arange(int(N))  # the x locations for the groups
width = 0.35       # the width of the bars


plt.rcdefaults()
from matplotlib.pyplot import cm 
color = iter(cm.rainbow(np.linspace(0,1,N)))
colors = []
for i in range(N):
    colors.append(next(color))


fig, ax = plt.subplots(figsize=(5, 5))

peakSCR_mean = tuple(df_mean['Peak'].tolist())
rects1 = ax.bar(ind, peakSCR_mean, width, color=colors[0]) # without std bar

peakSCR_mean = tuple(df_mean['Amp'].tolist())
rects2 = ax.bar(ind + width/2, peakSCR_mean, width, color=colors[1]) # without std bar

#add some text for labels, title and axes ticks
ax.set_ylabel('Average \# SCR peaks')
ax.legend((rects1[0],rects2[0]), ('\# Peak','Amp'))

#phasicSCR_mean = tuple(df_mean['phasicSCR'].tolist())
#phasicSCR_std = tuple(df_std['phasicSCR'].tolist())
#rects2 = ax.bar(ind, phasicSCR_mean, width, color=colors[0])
##rects2 = ax.bar(ind, phasicSCR_mean, width, color=colors[1], yerr=phasicSCR_std)
#
#tonicSCL_mean = tuple(df_mean['tonicSCL'].tolist())
#tonicSCL_std = tuple(df_std['tonicSCL'].tolist())
#rects3 = ax.bar(ind + width, tonicSCL_mean, width, color=colors[1])
##rects3 = ax.bar(ind + width, tonicSCL_mean, width, color=colors[2], yerr=tonicSCL_std)
#ax.set_ylabel('Average significant conductance ($\mu$S)')
#ax.set_title('Singapoore: Skin Conductance Response (SCR) and Skin conductane Level (SCL) per window (1-4s)')
#ax.set_xticks(ind + width / 2)
#ax.legend((rects2[0], rects3[0]), ('SCR', 'SCL'))

ax.set_xticklabels(tuple(listforbarname))



#def autolabel(rects):
#    """
#    Attach a text label above each bar displaying its height
#    """
#    for rect in rects:
#        height = rect.get_height()
#        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                '%d' % int(height),
#                ha='center', va='bottom')
#
#autolabel(rects1)
#autolabel(rects2)

plt.show()
fig.savefig('ZH_peak_pid_gen_all.pdf')
fig.savefig('ZH_peak_pid_gen_all.jpg')
plt.close(fig)

#%% Brar ploy another type

plt.rcdefaults()
from matplotlib.pyplot import cm 
color = iter(cm.rainbow(np.linspace(0,1,N)))
colors = []
for i in range(N):
    colors.append(next(color))

# Setting the positions and width for the bars
pos = list(range(len(df_mean))) 
width = 0.25 
    
# Plotting the bars
fig, ax = plt.subplots(figsize=(10,5))

# Create a bar with pre_score data,
# in position pos,
plt.bar(pos, 
        #using df['pre_score'] data,
        df_mean['peakSCR_0p01'], 
        #df_mean['tonicSCL_0p01'], 
        # of width
        width, 
        # with alpha 0.5
        alpha=0.5, 
        # with color
        color=colors[0], #'#EE3224', 
        # with label the first value in first_name
        label= 'peak 0.01') 
        #label= 'SCL 0.01') 

# Create a bar with mid_score data,
# in position pos + some width buffer,
plt.bar([p + width for p in pos], 
        #using df['mid_score'] data,
        df_mean['peakSCR_0p05'],
        #df_mean['tonicSCL_0p05'], 
        # of width
        width, 
        # with alpha 0.5
        alpha=0.5, 
        # with color
        color=colors[1], #'#F78F1E', 
        # with label the second value in first_name
        label= 'peak 0.05') 
        #label= 'SCL 0.05') 

# Create a bar with post_score data,
# in position pos + some width buffer,
plt.bar([p + width*2 for p in pos], 
        #using df['post_score'] data,
        df_mean['peakSCR_0p1'], 
        #df_mean['tonicSCL_0p1'], 
        # of width
        width, 
        # with alpha 0.5
        alpha=0.5, 
        # with color
        color=colors[2], #'#FFC222', 
        # with label the third value in first_name
        label= 'peak 0.1')
        #label= 'SCL 0.1') 

# Set the y axis label
ax.set_ylabel('Average number of significant SCR (peaks)')

# Set the chart's title
#ax.set_title('ZH: Skin conductance response (SCR) within per response time window (1-4s)')
ax.set_title('ZH: Significant number of SCRs within per response time window (1-4s)')

# Set the position of the x ticks
ax.set_xticks([p + 1.5 * width for p in pos])

#listforbarname = ['P2','P3','P4','P5','P6','P7', 'P8','P9','P10']
# Set the labels for the x ticks
ax.set_xticklabels(listforbarname)

# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*4)
plt.ylim([0, max(df_mean['peakSCR_0p01'] + df_mean['peakSCR_0p05'] + df_mean['peakSCR_0p1'])] )
#plt.ylim([0, max(df_mean['tonicSCL_0p01'] + df_mean['tonicSCL_0p05'] + df_mean['tonicSCL_0p1'])] )

# Adding the legend and showing the plot
#plt.legend(['peak 0.01$\mu$S','peak 0.05$\mu$S','peak 0.1$\mu$S'], loc='upper right')
plt.legend(['peak 0.01$\mu$S','peak 0.05$\mu$S','peak 0.1$\mu$S'], loc='upper right')

#plt.grid()
plt.show()
fig.savefig('ZH_peak_event_gen_com_all.pdf')
fig.savefig('ZH_peal_event_gen_com_all.jpg')
plt.close(fig)
#%% ploting invironment variables
import matplotlib.pyplot as plt;
means = df_mean[['Lux']]
#errors = df_std[['peakSCR', 'phasicSCR','tonicSCR']]


#fig, ax = plt.subplots(figsize=(12, 7))
ax = means.plot.bar(color='y') #r,b,c,y
ax.set_title("Average illuminance per window")
ax.set_xlabel("\n\n Events")
ax.set_ylabel("Average illuminance")
fig = ax.get_figure()
fig.savefig('SG_Lux_pid.png')
fig.savefig('SG_Lux_pid.pdf')
#%% line chart
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md # for date in x axis
import datetime as dt
import time

data_participant = pd.read_csv("merged_data.csv")
data_participant = data_participant.drop(['Unnamed: 0'], axis=1)

dictionary = {}
dictionary[1] = data_participant[data_participant['PID'] == 1]
dictionary[2] = data_participant[data_participant['PID'] == 2]
dictionary[3] = data_participant[data_participant['PID'] == 3]
dictionary[4] = data_participant[data_participant['PID'] == 4]
dictionary[5] = data_participant[data_participant['PID'] == 5]
dictionary[6] = data_participant[data_participant['PID'] == 6]
dictionary[7] = data_participant[data_participant['PID'] == 7]
dictionary[8] = data_participant[data_participant['PID'] == 8]
dictionary[9] = data_participant[data_participant['PID'] == 9]
#dictionary[10] = data_participant[data_participant['PID'] == 10]

#dictionary = {}
#dictionary[1] = data_participant[data_participant['EvenName'] == 'ride1']
#dictionary[2] = data_participant[data_participant['EvenName'] == 'ride2']
#dictionary[3] = data_participant[data_participant['EvenName'] == 'ride3']
#dictionary[4] = data_participant[data_participant['EvenName'] == 'wait1']
#dictionary[5] = data_participant[data_participant['EvenName'] == 'wait2']
#dictionary[6] = data_participant[data_participant['EvenName'] == 'wait3']
#dictionary[7] = data_participant[data_participant['EvenName'] == 'walk']


dictionary = {}
dictionary[1] = data_participant[data_participant['EvenName'] == 'ride80-1']
dictionary[2] = data_participant[data_participant['EvenName'] == 'ride80-2']
dictionary[3] = data_participant[data_participant['EvenName'] == 'ride32-1']
dictionary[4] = data_participant[data_participant['EvenName'] == 'ride32-2']
dictionary[5] = data_participant[data_participant['EvenName'] == 'wait80-1']
dictionary[6] = data_participant[data_participant['EvenName'] == 'wait80-2']
dictionary[7] = data_participant[data_participant['EvenName'] == 'wait32-1']
dictionary[8] = data_participant[data_participant['EvenName'] == 'wait32-2']
dictionary[9] = data_participant[data_participant['EvenName'] == 'walk']



data_frame = pd.DataFrame({"A": []})
data_dic = {}
for i in [1,2,3,4,5,6,7,8,9]:
    data_pid = dictionary[i]
    #data_frame['P'+str(i)] = data_pid['tonicSCL'].tolist()
    data_dic[i] = data_pid['tonicSCL'].tolist()

(pd.DataFrame.from_dict(data=data_dic, orient='index')
   .to_csv('event_peak.csv', header=False))
    
#%%  
from matplotlib import colors as mcolors  

#for i in [2,3,4,5,6,7,8,9,10]:
for i in [1,2,3,4,5,6,7,8,9]:
    #i = 10
    print(i)
    participant = i
    data_pid = dictionary[i]

    data_filter = data_pid[['Temp','RH','Sound','Lux','tonicSCL_0p05','phasicSCR_0p05','peakSCR_0p05','peakSCR_0p1']]    
    #data_filter = data_pid[['HSTemp','Sound','Lux','tonicSCL_0p05','phasicSCR_0p05','peakSCR_0p1']]    
    data_diff = data_filter.diff(periods=20)    
    data_diff = data_diff.dropna()    
    pid_list = data_pid.index.tolist()
    dif_list =  data_diff.index.tolist()
    matches  = [x for x in pid_list if (x in dif_list)]    
    event_data = data_pid["EvenName"][matches]
    #data_diff['EvenName'] = event_data.tolist()
    ##for ZH data  
#    listEvenNum = []
#    for j in range(len(event_data)):
#        if (event_data[matches[j]].startswith('ride80')):
#            listEvenNum.append(2)
#        elif (event_data[matches[j]].startswith('ride32')):
#                listEvenNum.append(1.5)
#        elif (event_data[matches[j]].startswith('wait80')):
#                listEvenNum.append(1)
#        elif (event_data[matches[j]].startswith('wait32')):
#                listEvenNum.append(0.5)
#        elif (event_data[matches[j]].startswith('walk')):
#                listEvenNum.append(0)
#        else:
#            listEvenNum.append(-1)
            
    listEvenNum = []
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
#    from scipy import stats
#    cutoff = 2 # this may varry form case to case for 3 use 0.4;
#    #df = data_mean_gps[(np.abs(stats.zscore(data_mean_gps)) < cutoff).all(axis=1)]
#    data_diff["TempCut"] = (np.abs(stats.zscore(data_diff['HSTemp'])) < cutoff).tolist()
#    #data_mean_gps["CutXY"] = ~np.array((data_mean_gps['wgs_x'] < 1.2).tolist())
    
    
    #data_diff = data_diff.drop(data_diff.iloc[:,0].index.tolist()[0])
    
    timestamps = data_pid['Time'][data_diff.index]
    dates = [dt.datetime.fromtimestamp(ts) for ts in timestamps]
    #dates = [ts.time() for ts in dates]
    datenums=md.date2num(dates)
    
    #t2 = np.asarray(data_diff['HSRH'])
    #temp = np.asarray(data_diff['HSTemp'])
    temp = np.asarray(data_diff['Temp'])
    sound = np.asarray(data_diff['Sound'])
    lux = np.asarray(data_diff['Lux'])
    
    scl = np.asarray(data_diff['tonicSCL_0p05'])    
    scr = np.asarray(data_diff['phasicSCR_0p05'])
    peak05 = np.asarray(data_diff['peakSCR_0p05'])
    peak1 = np.asarray(data_diff['peakSCR_0p1'])
    
    status = np.asarray(listEvenNum)
    

    
#    temp_data = np.asmatrix([t1,t2,t3])
#    
#    from sklearn.preprocessing import StandardScaler
#    scaler = StandardScaler()
#    scaler.fit(temp_data)
#    temp_data_transform = scaler.transform(temp_data)
#    
#    t1 = temp_data_transform[0]
#    t2 = temp_data_transform[1]
#    t3 = temp_data_transform[2]
##
##    data = [[0, 0], [0, 0], [1, 1], [1, 1]]
##    scaler = StandardScaler()
##    print(scaler.fit(data))
##    print(scaler.transform(data))
#    
    fig, ax = plt.subplots(figsize=(10, 12))
    #plt.subplots_adjust(bottom=0.2)
    #plt.xticks( rotation=25 )
    #ax=plt.gca()
    
    # Environment variable charts
    axTemp = plt.subplot(811)
    plt.plot(datenums,temp, 'lightcoral')
    plt.setp(axTemp.get_xticklabels(), visible=False)
    axTemp.set_ylabel("Temp")
    plt.legend(['Temp'], loc='upper left')       
    
    axSound = plt.subplot(812, sharex=axTemp)
    plt.plot(datenums,sound, 'turquoise')
    plt.setp(axSound.get_xticklabels(), visible=False)
    axSound.set_ylabel("Sound")
    plt.legend(['Sound'], loc='upper left')   
    
    axLux = plt.subplot(813, sharex=axTemp)
    plt.plot(datenums,lux, 'sandybrown')
    plt.setp(axLux.get_xticklabels(), visible=False)
    axLux.set_ylabel("Lux")
    plt.legend(['Lux'], loc='upper left')    
    
    #Skin conducatence charts
    axSCL = plt.subplot(814, sharex=axTemp)
    plt.plot(datenums,scl, 'mediumslateblue')
    plt.setp(axSCL.get_xticklabels(), visible=False)
    axSCL.set_ylabel(" SCL")
    plt.legend(['SCL'], loc='upper left')
    
    axSCR = plt.subplot(815, sharex=axTemp)
    plt.plot(datenums,scr, 'plum')
    plt.setp(axSCR.get_xticklabels(), visible=False)
    axSCR.set_ylabel(" SCR")
    plt.legend(['SCR',], loc='upper left')
    
    axPeak05 = plt.subplot(816, sharex=axTemp)
    plt.plot(datenums,peak05, 'orchid')
    plt.setp(axPeak05.get_xticklabels(), visible=False)
    axPeak05.set_ylabel(" Peak 05")
    plt.legend(['SCR',], loc='upper left')
    
    axPeak1 = plt.subplot(817, sharex=axTemp)
    plt.plot(datenums,peak1, 'darkmagenta')
    plt.setp(axPeak1.get_xticklabels(), visible=False)
    axPeak1.set_ylabel(" Peak 0.1")
    plt.legend(['Peak',], loc='upper left')
    
    #ax3 = plt.subplot(313, sharex=ax1, sharey=ax1)
    axStatus = plt.subplot(818, sharex=axTemp )
    plt.plot(datenums,status, 'darkgray')
    xfmt = md.DateFormatter('%H:%M:%S')
    axStatus.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation=25 )
    axStatus.set_ylabel("Status")
    plt.legend(['Status (-1:unknown, 0:walk, 0-1:wait, 1-2:ride)'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, borderaxespad=0.)
    axStatus.set_xlabel("\n Time progress P"+str(participant)+'\n')

    fig.savefig('SG_Line_P'+str(participant)+'.pdf')
    fig.savefig('SG_Line_P'+str(participant)+'.jpg')
    plt.show()
    plt.close(fig)
    

#%%
    
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import time

n=20
duration=1000
now=time.mktime(time.localtime())
timestamps=np.linspace(now,now+duration,n)
dates=[dt.datetime.fromtimestamp(ts) for ts in timestamps]
datenums=md.date2num(dates)
values=np.sin((timestamps-now)/duration*2*np.pi)
plt.subplots_adjust(bottom=0.2)
plt.xticks( rotation=25 )
ax=plt.gca()
xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.plot(datenums,values)
plt.show()



