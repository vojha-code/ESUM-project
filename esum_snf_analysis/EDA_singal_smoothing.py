# -*- coding: utf-8 -*-
"""
@author: vojha

File EDA (Signal) smoothing 

"""

#Libraries required fro running these files
import pandas as pd
import numpy as np
import scipy.signal as scisig
import os
from datetime import datetime
from datetime import timedelta
from calendar import timegm
import dateutil.parser


import matplotlib.pyplot as plt
import numpy as np
from random import randint

import pywt
from sklearn.mixture import GaussianMixture
#%% input folder and file path
# participant_data_path is folder to which all dataset are kept
participant_data_path = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\Participant_Data"

# within the folder "participant_data_path" which folder has the EDA participant data?
# filepath is the folder where all eda data are kept
filepath = participant_data_path+"\\eda_data_marked"

#%%

# ALl file name must be named as "EDA_data_*.csv" where * is the number of participant

#total_number_of_file = 35
#for i in range(total_number_of_file): #if all files are available and can be processed correctly

#If some files are missing and some are faulty use the following for loop (as in my case)
for i in [6,7,8,9,10,11,13,16,18,23,24,25,26,27,28,29,30,32,34,35]: #
    
    #run for participant i
    participant = i; # if you want to run for only one participant select and run only from this line
    # i.e, from line "participant = *" where * is the number of only one participant
    
    
    #------------PARAMETERS For Wevlet transofr----------#
    # how many lavel for transofrm you want
    wavelet_lavel = 1
    # threshold for smoothing
    delta = 0.001

    #filename must be "EDA_data_*.csv" where * is the number of participant
    file_name = 'EDA_data_'+str(participant)+'.csv'
    eda_file =  os.path.join(filepath,file_name)
    eda_data = pd.DataFrame.from_csv(eda_file)
    contaminatedSC = eda_data["EDA"].tolist() #Mearking original EDA as contaminated EDA
    
    #-----------SMOOTHING PROCESS ------------------------#
    # uncomment if you also want your data to be passed through low pass filter.
    # contaminatedSC = butter_lowpass_filter(contaminatedSC, 1.0, 8, 6) 
    

    contaminatedSC = np.asarray(contaminatedSC)
    # making data even length
    if(len(contaminatedSC)%2 != 0):
        contaminatedSC = np.delete(contaminatedSC, len(contaminatedSC)-1)
        eda_data = eda_data.drop(eda_data.index[len(eda_data)-1])
    
    #statiinary walet transforma with HAAR wevlet transform
    coeffs = pywt.swt(contaminatedSC, 'Haar', level=wavelet_lavel) # Haar
    #plt.hist(coeffs[1][1])
    
   
    #some commands related to plot generation
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[6, 3.5])
    plt.plot(contaminatedSC, color="blue", label="Original signal") # inputs are data, color, and label
    plt.plot(coeffs[0][1],  color="darkorange", label="Wavelet coefficients") 
    
    #threshold delta applied on coefficient levels of EDA signal
    for j in range(wavelet_lavel):
        for i in range(len(contaminatedSC)):
            # x(i) = x(i) if  -delta < x(i) < delta else x(i) = 0.0
            if (coeffs[j][1][i] > -delta) and (coeffs[j][1][i] < delta):
                coeffs[j][1][i] =  coeffs[j][1][i]
            else:
                coeffs[j][1][i] = 0.0
        
    plt.plot(coeffs[0][1], color="limegreen", label="Threshold")
    ax.set_ylabel("$\mu S$")
    ax.set_xlabel("Time (ms)")
    plt.legend()
    plt.show()
    fig.savefig('SC_filtering_p'+str(participant)+'.pdf')
    plt.close(fig)
    
    #inverse SWT
    refinedSC = pywt.iswt(coeffs, 'Haar')#Haar
    
    
    #Original and filter signal
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5.5, 2])
    plt.plot(contaminatedSC, color="red" , label="Original signal",linewidth = 0.5)
    #plt.plot(refinedSC, color="darkorange", label="Smoothed signal", linewidth = 0.5)
    ax.set_ylabel("$\mu S$")
    ax.set_xlabel("Time (ms)")
    plt.legend()
    plt.show()
    #fig.savefig('SC_orignal_v_filter_p'+str(participant)+'.pdf')
    fig.savefig('discarded_ex_'+str(1)+'.pdf')
    plt.close(fig)
    
    #Write back to original data
    eda_data["filteredEDA"] =  refinedSC.tolist()
    save_regular_results(filepath, file_name,eda_data,participant)

#%%procces and save data
def save_regular_results(filepath, file_name, df,participant):
    eda_out_file = os.path.join(filepath, file_name)
    df.to_csv(eda_out_file) 
    
    
    eda_out_file1 =  os.path.join(filepath,'leda_exp_'+str(participant)+'.txt')
    list1 = df["regular_time"].tolist()#Fetching regular time
    list2 = df["filteredEDA"].tolist()#Fetching regular time
    list3 = df["event_marker_regular"].tolist()#Fetching regular time
    eda_data_out = list(zip(list1,list2,list3)) # Zip all list into one list
    
    np.savetxt(eda_out_file1, eda_data_out, delimiter="\t", fmt='%s')
#%%
##original signal
#data = eda_data['eda']
#plt.plot(data)
#
##low pass filter
#data = butter_lowpass_filter(eda_data['eda'], 1.0, 8, 6)
#plt.plot(data)
#
##high pass filter
#data = butter_highpass_filter(eda_data['eda'], 1.0, 8, 6)
#plt.plot(data)
#
#def butter_lowpass(cutoff, fs, order=5):
#    # filtering helper functions
#    nyq = 0.5 * fs
#    normal_cutoff = cutoff / nyq
#    b, a = scisig.butter(order, normal_cutoff, btype='low', analog=false)
#    return b, a
#
#def butter_lowpass_filter(data, cutoff, fs, order=5):
#    # filtering helper functions
#    b, a = butter_lowpass(cutoff, fs, order=order)
#    y = scisig.lfilter(b, a, data)
#    return y
#
#def butter_highpass(cutoff, fs, order=5):
#    nyq = 0.5 * fs
#    normal_cutoff = cutoff / nyq
#    b, a = scisig.butter(order, normal_cutoff, btype='high', analog=false)
#    return b, a
#
#def butter_highpass_filter(data, cutoff, fs, order=5):
#    b, a = butter_highpass(cutoff, fs, order=order)
#    y = scisig.filtfilt(b, a, data)
#    return y