import pandas as pd
import numpy as np
import scipy.signal as scisig
import os

def getInputLoadFile():
    ''' OUTPUT:
        data:   DataFrame, index is a list of timestamps at 8Hz, columns include 
                AccelZ, AccelY, AccelX, Temp, EDA, filtered_eda
    '''
    print ("Please enter information about your EDA file... ")
    
    filepath = './' #input("\tPath to E4 directory: ")
    filepath_confirm = os.path.join(filepath,"EDA.csv")
    data = loadData_E4(filepath)
    data = data.interpolate()
    
    return data, filepath_confirm

def getOutputPath():
    outfile = 'OutEDA.csv' #input('\tFile name: ')
    outputPath = './' #input('\tFile directory (./ for this directory): ')
    fullOutputPath = os.path.join(outputPath,outfile)
    if fullOutputPath[-4:] != '.csv':
        fullOutputPath = fullOutputPath+'.csv'
    return fullOutputPath

def loadData_E4(filepath):
    # Load EDA data
    eda_data = _loadSingleFile_E4(os.path.join(filepath,'EDA.csv'),["EDA"],4,"250L")
    # Get the filtered data using a low-pass butterworth filter (cutoff:1hz, fs:8hz, order:6)
    eda_data['filtered_eda'] =  butter_lowpass_filter(eda_data['EDA'], 1.0, 8, 6)

    # Load ACC data
    #acc_data = _loadSingleFile_E4(os.path.join(filepath,'ACC.csv'),["AccelX","AccelY","AccelZ"],32,"31250U")
    # Scale the accelometer to +-2g
    #acc_data[["AccelX","AccelY","AccelZ"]] = acc_data[["AccelX","AccelY","AccelZ"]]/64.0

    # Load Temperature data
    #temperature_data = _loadSingleFile_E4(os.path.join(filepath,'TEMP.csv'),["Temp"],4,"250L")
    
    #data = eda_data.join(acc_data, how='outer')
    #data = data.join(temperature_data, how='outer')
    
    data = eda_data
    return data


def _loadSingleFile_E4(filepath,list_of_columns, expected_sample_rate,freq):
    # Load data
    data = pd.DataFrame.from_csv(filepath)
    data.reset_index(inplace=True)
    
    # Get the startTime and sample rate
    startTime = pd.to_datetime(float(data.columns.values[0]),unit="s")
    sampleRate = float(data.iloc[0][0])
    data = data[data.index!=0]
    data.index = data.index-1
    
    # Reset the data frame assuming expected_sample_rate
    data.columns = list_of_columns
    if sampleRate != expected_sample_rate:
        print('ERROR, NOT SAMPLED AT {0}HZ. PROBLEMS WILL OCCUR\n'.format(expected_sample_rate))
    #data.index = pd.DatetimeIndex(start=startTime,periods = len(data),freq=freq)

    # Make sure data has a sample rate of 8Hz
    data = interpolateDataTo8Hz(data,sampleRate,startTime)

    return data


def interpolateDataTo8Hz(data,sample_rate,startTime):
    if sample_rate<8:
        # Upsample by linear interpolation
        if sample_rate==2:
            data.index = pd.DatetimeIndex(start=startTime,periods = len(data),freq='500L')
        elif sample_rate==4:
            data.index = pd.DatetimeIndex(start=startTime,periods = len(data),freq='250L')
        data = data.resample("125L").mean()
    else:
        if sample_rate>8:
            # Downsample
            idx_range = range(0,len(data))
            print()
            data = data.iloc[idx_range[0::int(sample_rate/8)]]
        # Set the index to be 8Hz
        data.index = pd.DatetimeIndex(start=startTime,periods = len(data),freq='125L')

    # Interpolate all empty values
    data = interpolateEmptyValues(data)
    return data

def interpolateEmptyValues(data):
    cols = data.columns.values
    #data = data.resample('2s').interpolate() 
    for c in cols:
        data[c] = data[c].interpolate()

    return data

def butter_lowpass(cutoff, fs, order=5):
    # Filtering Helper functions
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scisig.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    # Filtering Helper functions
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = scisig.lfilter(b, a, data)
    return y


