# -*- coding: utf-8 -*-

#%%importing packages
import pandas as pd
import numpy as np
import scipy.signal as scisig
import os
from datetime import datetime
from datetime import timedelta
from calendar import timegm
import dateutil.parser


#%% File selection
os.chdir("C:\\Users\\vojha\\Dropbox\\00_Programming\\ESUM_Experiments\\Bus_Stop_Project_Data")


eda_file =  'EDA.csv'

# EDA Variables 
list_of_columns_eda = ["EDA"]
#expected_sample_rate_eda = 4
#freq_eda = "250L"

#Feteching data
# Load data
eda_data = pd.DataFrame.from_csv(eda_file)
eda_data.reset_index(inplace=True)

# Get the startTime and sample rate
startTime = pd.to_datetime(float(eda_data.columns.values[0]),unit="s")
sampleRate = float(eda_data.iloc[0][0]) #retriving sample rate
eda_data = eda_data[eda_data.index!=0] #reindexing eda dataframe
eda_data.index = eda_data.index-1 #reindexing eda dataframe


# Reset the data frame assuming expected_sample_rate
eda_data.columns = list_of_columns_eda # Changing column Name 
#perform upsampling
eda_data.index = pd.DatetimeIndex(start=startTime,periods = len(eda_data),freq='250L')
#eda_data["timestamp"] = eda_data.index 

#creating only seconds list
secondslist = np.zeros(len(eda_data))
seconds = 0.000
for i in range(len(secondslist)):
    secondslist[i] = seconds
    seconds += 0.250 # for 4Hz  
eda_data["time"] = secondslist

#initializing marker
marker = np.empty(len(eda_data))
marker.fill(-1)

eda_data["event_marker_regular"] = np.zeros(len(eda_data))

slice_time_window = 5.000
time_window = int(slice_time_window)

marked_eda_data,event_duration_regular =  create_regular_marker(eda_data,slice_time_window)

#creating only seconds list
secondslist = np.zeros(len(marked_eda_data))
seconds = 0.000
for j in range(len(secondslist)):
    secondslist[j] = seconds
    seconds += 0.250 # for 4Hz  
marked_eda_data["regular_time"] = secondslist
    
save_regular_results(marked_eda_data,event_duration_regular)
#%% marke regular interval
def create_regular_marker(sliced_data,interval):    
    event = 1
    event_duration_regular = []
    sliced_data["event_marker_regular"][0] = event
    seconds = 0.000
    for i in range(len(sliced_data)):
        if (seconds == interval):
            event_duration_regular.append(seconds)
            event += 1
            sliced_data["event_marker_regular"][i]= event
            seconds = 0.000   
        seconds += 0.250 # for 4Hz 
    
    # append last even only if it is about "seconds == slice_time_window"   
    if(seconds < (slice_time_window-0.50)):
        sliced_data.loc[sliced_data['event_marker_regular'] == event, 'event_marker_regular'] = 0.0
        #sliced_eda_data.loc[sliced_eda_data['event_marker_regular'] == event, 'EDA'].iloc[0] #only for retriving value
    else:
        event_duration_regular.append(seconds) #appending last event  
        
    if (len(event_duration_regular)==event):
        print('Perfect: ',len(event_duration_regular)," = ",(event))
    
    return sliced_data,event_duration_regular

#%% save regular daya
def save_regular_results(sliced_eda_data,event_duration):
    eda_out_file = os.path.join("EDA_data_"+str(time_window)+"s_marked.csv")
    eda_out_file1 =  os.path.join("Marker_"+str(time_window)+"s_"+str(i)+".txt")
    eda_out_file2 =  os.path.join("Event_duration_"+str(time_window)+"s_"+str(i)+".txt")

    list1 = sliced_eda_data["regular_time"].tolist()
    list2 = sliced_eda_data["EDA"].tolist()
    list3 = sliced_eda_data["event_marker_regular"].tolist()
    eda_data_out = list(zip(list1,list2,list3))
    
    sliced_eda_data.to_csv(eda_out_file)
    np.savetxt(eda_out_file1, eda_data_out, delimiter="\t", fmt='%s')
    np.savetxt(eda_out_file2, event_duration, delimiter="\n", fmt='%s')
    
    
#%% Plot the peaqks and data
import matplotlib.pyplot as plt



df_eda = marked_eda_data.loc[marked_eda_data['event_marker_regular'] != 0]
cols_to_norm = ['EDA']
df_eda[cols_to_norm] = df_eda[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
norm_df_eda  = df_eda


df_peak = pd.read_excel("Marker_exp_1.xls",sheetname='ERA')
cols_to_norm = ['CDA.nSCR']
df_peak[cols_to_norm] = df_peak[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
norm_df_peak  = df_peak
norm_df_peak['Peak'] = [0 if x < 0.5 else 1 for x in norm_df_peak['CDA.nSCR']]


plt.style.use("default")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5,2])
plt.plot(norm_df_eda['EDA'].tolist(), label = 'EDA', color = 'seagreen', linewidth=1.5)
plt.plot(norm_df_peak["Peak"].tolist(), label = 'Peak', color = 'dimgray',linewidth=1.5)

plt.ylabel('Normalized mean value')
plt.xlabel('Quantified samples')
#plt.title('All variable normalized mean signal analysis')
plt.legend()
fig.savefig('norm_mean_peak_plot.pdf')
fig.savefig('norm_mean_peak_plot.jpeg')
#fig.savefig('isovist_variable_norm_mean_plot_peak.pdf')
plt.show()
plt.close(fig)    

#%% Filterining
#original signal
data = eda_data['EDA']
plt.plot(data)

#low pass filter
data = butter_lowpass_filter(eda_data['EDA'], 1.0, 8, 6)
plt.plot(data)

#high pass filter
data = butter_highpass_filter(eda_data['EDA'], 1.0, 8, 6)
print(eda_data['EDA'])
plt.plot(data)

#%%
def butter_lowpass(cutoff, fs, order=5):
    # filtering helper functions
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scisig.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

#%%
def butter_lowpass_filter(data, cutoff, fs, order=5):
    # filtering helper functions
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = scisig.lfilter(b, a, data)
    return y

#%%
def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scisig.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

#%%
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = scisig.filtfilt(b, a, data)
    return y