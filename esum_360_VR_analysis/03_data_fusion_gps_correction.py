# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 13:50:52 2018

@author: vojha
"""
%reset -f
%clear

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
import math

import datetime
from datetime import timedelta
from calendar import timegm
import dateutil.parser
from time import mktime

#%% time
def make_timestamnp(timedata):
    return mktime(timedata.timetuple())
    
#%%
def convert_from_timestamp(date_in_some_format):
    date_as_string = datetime.datetime.fromtimestamp(date_in_some_format)
    date_as_string = date_as_string + timedelta(hours=+int(0)) # correction for UTC time difference
    return date_as_string
#%%
def convert_to_timestamp(date_in_some_format):
    date_as_string = dateutil.parser.parse(date_in_some_format)
    return date_as_string
#%% data time parsers with correction of time
def convert_to_timestamp_correction(date_in_some_format):
    date_as_string = dateutil.parser.parse(date_in_some_format)
    date_as_string = date_as_string + timedelta(hours=+int(2)) # correction for UTC time difference
    return date_as_string 
#%%
dataof = "DE"
if(dataof == "DE"):
    file_gps = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','Weimar360GPS.csv')
    data_gps = pd.read_csv(file_gps)
    
    EDA_File_Raw = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed\markedEDA',"eda_marked")
    EDA_File_Pro = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed\processedEDA","0p1")
    
    VideoQ = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed\Video","Q")
    VideoT = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed\Video","T")
    fileSaves = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','compliedData')
    file_complied = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','merged_data.csv')
    file_groupXY = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','XYarusal.csv')
    file_groupClick = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','XYClicker.csv')
else:
    file_gps = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed','Zurich360GPS.csv')
    data_gps = pd.read_csv(file_gps)
    
    EDA_File_Raw = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed\markedEDA',"eda_marked")
    EDA_File_Pro = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed\processedEDA","0p1")
    
    VideoQ = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed\Video","Q")
    VideoT = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed\Video","T")
    fileSaves = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed','compliedData')
    file_complied = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed','merged_data.csv')
    file_groupXY = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed','XYarusal.csv')
    file_groupClick = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed','XYClicker.csv')
#%%

files_EDA = os.listdir(EDA_File_Raw) # raw eda file 
files_LEDA = os.listdir(EDA_File_Pro) # processed eda file 
files_Q = os.listdir(VideoQ) # Cliker files
files_T = os.listdir(VideoT) # time, start, pausing and finish experiment time

#%%
if(len(files_EDA) == len(files_LEDA) == len(files_Q) == len(files_T)):    
    idxflag = []
    for idx in range(len(files_EDA)):   
        #idx = 0
        if(files_EDA[idx][19:21] == files_LEDA[idx][9:11] == files_Q[idx][3:5] == files_T[idx][3:5]):
            print("Check data:", idx, files_EDA[idx][19:21],"\n")    
            data_eda_raw = pd.read_csv(os.path.join(EDA_File_Raw,files_EDA[idx]))
            data_eda_raw.rename(columns={'Unnamed: 0': 'Timestamp'}, inplace=True)
            #data_eda_raw["EDA"].plot() % This will compile all the plot in a single file
            plt.plot(data_eda_raw["EDA"])
            plt.show()

#%%
de = [0,1,2,4,10,14,15,21,22,25,26,27,28]
zh = [0,1,3,5,7,17,33]

#%%
count = 0
if(len(files_EDA) == len(files_LEDA) == len(files_Q) == len(files_T)):    
    idxflag = []
    for idx in range(len(files_EDA)):  
        if(dataof == "DE"):
            reject = de
        else:
            reject = zh
        if(not(idx in reject)):
            print("Check data:", idx, files_EDA[idx][19:21],"\n")    
            data_eda_raw = pd.read_csv(os.path.join(EDA_File_Raw,files_EDA[idx]))
            data_eda_raw.rename(columns={'Unnamed: 0': 'Timestamp'}, inplace=True)
            #data_eda_raw["EDA"].plot() % This will compile all the plot in a single file
            plt.plot(data_eda_raw["EDA"])
            plt.show()
            count = count + 1
#%%
if(len(files_EDA) == len(files_LEDA) == len(files_Q) == len(files_T)):    
    idxflag = []
    for idx in range(len(files_EDA)):     
        #idx = 0
        if(files_EDA[idx][19:21] == files_LEDA[idx][9:11] == files_Q[idx][3:5] == files_T[idx][3:5]):
            if(dataof == "DE"):
                reject = de
            else:
                reject = zh
            if(not(idx in reject)):
                print("Number matches:", idx, files_EDA[idx][19:21],"\n")    
                data_eda_raw = pd.read_csv(os.path.join(EDA_File_Raw,files_EDA[idx]))
                data_eda_raw.rename(columns={'Unnamed: 0': 'Timestamp'}, inplace=True)
                data_eda_raw = data_eda_raw.set_index(pd.DatetimeIndex(data_eda_raw['Timestamp']))
                data_eda_raw_5s = data_eda_raw.resample('5S', how='sum')
                
                data_leda = pd.read_excel(os.path.join(EDA_File_Pro,files_LEDA[idx]),sheetname='CDA')
                data_leda = data_leda[['CDA.nSCR','CDA.SCR [muS]','CDA.Tonic [muS]']]
                data_leda.rename(columns={'CDA.nSCR': 'peak','CDA.SCR [muS]': 'SCR','CDA.Tonic [muS]': 'SCL'}, inplace=True)
                    
                if(len(data_eda_raw_5s) > len(data_leda)):
                    data_eda_raw_5s = data_eda_raw_5s.drop(data_eda_raw_5s.index[len(data_eda_raw_5s)-1])
                    #data_leda["Timestamp"] = data_eda_raw_5s.index.values.tolist()
                
                data_VQ = pd.read_csv(os.path.join(VideoQ,files_Q[idx]))
                data_Play = data_VQ[np.isnan(data_VQ['input'])]
                data_Play.rename(columns={'item_label_a': 'Status'}, inplace=True)
                del data_Play['item_label_b']
                del data_Play['input']
                data_VQ = data_VQ[(np.isnan(data_VQ['input']) == False)]
                
                data_VT = pd.read_csv(os.path.join(VideoT,files_T[idx]))
                data_VT_5s = data_VT # preserving VT
                data_VT_5s["Timestamp"] = data_VT_5s['unix_time'].apply(convert_from_timestamp)
                data_VT_5s = data_VT_5s.set_index(pd.DatetimeIndex(data_VT_5s['Timestamp']))
                data_clicker = data_VT_5s[["clicker_input"]]
                from scipy import stats
                #from collections import Counter
                #mode = lambda x: x.mode() if len(x) > 0 else 0
                mode = lambda x: stats.mode(x)[0] if len(x) > 0 else 0
                #mode = lambda x: Counter(x).most_common(1)
                #length = lambda x: len(x)
                data_clicker = data_clicker.resample('5S', how={mode})
                data_clicker.columns = ["clicker_input"]
                data_clicker["Timestamp"] = data_clicker.index
                set_for_gt_3 = 0
                data_clicker["clicker_input"] =  [x if x <= 3 else set_for_gt_3 for x in data_clicker["clicker_input"]]
                
                data_Play = data_Play.append({'checkpoint': data_VT.iloc[0]["unix_time"], 'Status': "Start"}, ignore_index=True)
                data_Play = data_Play.append({'checkpoint': data_VT.iloc[len(data_VT)-1]["unix_time"], 'Status': "End"}, ignore_index=True)
                data_Play = data_Play.sort_values(['checkpoint']).reset_index(drop=True)
                
                recording = []
                for iPlay in range(len(data_Play)):
                    if(data_Play["Status"][iPlay] == "Start"):
                        recording.append("Play")
                    if(data_Play["Status"][iPlay] == "Play"):
                        recording.append("Pause")
                    if(data_Play["Status"][iPlay] == "Pause"):
                        recording.append("Play")
                    if(data_Play["Status"][iPlay] == "End"):
                        recording.append("Pause")                    
                data_Play["Recording"] = recording
                del data_Play["Status"]
                
                #Check time 
                time_eda_start = convert_to_timestamp_correction(data_eda_raw_5s.index[0].strftime('%Y-%m-%d %H:%M:%S.%f'))
                time_eda_end = convert_to_timestamp_correction(data_eda_raw_5s.index[len(data_eda_raw_5s)-1].strftime('%Y-%m-%d %H:%M:%S.%f'))
                
                print(time_eda_start, "EDA Start")
                for iPlay in range(len(data_Play)):
                    print("     ",convert_from_timestamp(data_Play["checkpoint"][iPlay]),data_Play["Recording"][iPlay])
                    if(mktime(time_eda_end.timetuple()) < data_Play["checkpoint"][iPlay]):
                        idxflag.append(idx)
                print(time_eda_end,"End Stop \n")
                
    #            #Find Play time only
                itrEDA = 0
                iPlay = 0
                playtime = 0
                listPlayPause = []
                listTimeStamp = []
                while(itrEDA < len(data_leda)):
                    time_eda = convert_to_timestamp_correction(data_eda_raw_5s.index[itrEDA].strftime('%Y-%m-%d %H:%M:%S.%f'))
                    time_eda = mktime(time_eda.timetuple())
                    #print(" ",itrEDA,time_eda)                  
                    #itrEDA = itrEDA + 1
                    #print(iPlay)
                    if(iPlay < len(data_Play)):
                        if((time_eda <= data_Play["checkpoint"][iPlay]) and (data_Play["Recording"][iPlay] == 'Play')):
                            listPlayPause.append('Pause')
                            listTimeStamp.append(time_eda)
                            itrEDA = itrEDA + 1
                        elif((time_eda <= data_Play["checkpoint"][iPlay]) and (data_Play["Recording"][iPlay] == 'Pause')):
                            listPlayPause.append('Play')
                            listTimeStamp.append(time_eda)
                            itrEDA = itrEDA + 1
                            playtime = playtime + 1
                        else:
                            iPlay = iPlay + 1  
                    else:
                        listPlayPause.append('Pause')
                        listTimeStamp.append(time_eda)
                        itrEDA = itrEDA + 1
                
                print("Total play time (min): ", (playtime*5)/60)
                print("Total click time (min):", (len(data_VT)/60)/4)
                data_leda["Status"] = listPlayPause
                data_leda["Timestamp"] = listTimeStamp
                
                # Processing GPS with every five second location            
                data_gps["Seconds"] = data_gps["Time-Minutes"]*60
                data_gps["Seconds"] = data_gps["Seconds"] + data_gps["Time-Seconds"]
                #data_gps["Seconds"] = data_gps["Seconds"] + data_gps["Time-Miliseconds"]/1000
                #data_gps["Seconds"] = data_gps['Seconds'].apply(lambda x: round(x))
                data_gps_smaple_5s = data_gps[data_gps["Seconds"] % 5 == 0].reset_index(drop = True)
                data_gps_smaple_5s = data_gps_smaple_5s.groupby(['Seconds']).mean().reset_index()
                
                
                #Fetching only play time
                data_leda_play = data_leda[data_leda["Status"]=="Play"]
                print("Lengths: ", len(data_leda), len(data_leda_play), len(data_gps_smaple_5s))
                
                #Assinging GPS to data
                if(len(data_gps_smaple_5s)< len(data_leda_play)):
                    data_leda_play = data_leda_play.head(len(data_gps_smaple_5s))
                    
                data_leda_play["Latitude"] = data_gps_smaple_5s.head(n = len(data_leda_play))['Latitude'].tolist()
                data_leda_play["Longitude"] = data_gps_smaple_5s.head(n = len(data_leda_play))['Longitude'].tolist()
                data_leda_play["Area"] = data_gps_smaple_5s.head(n = len(data_leda_play))['2dIso 180 Area'].tolist()
                data_leda_play["Perimeter"] = data_gps_smaple_5s.head(n = len(data_leda_play))['2dIso 180 Perimeter'].tolist()
                data_leda_play["Compactness"] = data_gps_smaple_5s.head(n = len(data_leda_play))['2dIso 180 Compactness'].tolist()
                data_leda_play["Occlusivity"] = data_gps_smaple_5s.head(n = len(data_leda_play))['2dIso 180 Occlusivity'].tolist()
                data_leda_play["Min_radial"] = data_gps_smaple_5s.head(n = len(data_leda_play))['2dIso 360 Min radial'].tolist()
                data_leda_play["Volume"] = data_gps_smaple_5s.head(n = len(data_leda_play))['3dIso 360_110 Volume'].tolist()
                data_leda_play["RayPortion_sky"] = data_gps_smaple_5s.head(n = len(data_leda_play))['3dIso 360_110 RayPortion_sky'].tolist()
                data_leda_play["RayPortion_obstacles"] = data_gps_smaple_5s.head(n = len(data_leda_play))['3dIso 360_110 RayPortion_obstacles'].tolist()
                data_leda_play["Betweenness Car"] = data_gps_smaple_5s.head(n = len(data_leda_play))['Betweenness Rn angular'].tolist()                
                data_leda_play["Betweenness Ped"] = data_gps_smaple_5s.head(n = len(data_leda_play))['Betweenness R600 angular'].tolist()  

       
                del data_leda_play["Status"]
                
                if(len(data_clicker) > len(data_leda_play)):
                    print("Clicker: ",len(data_clicker))
                
                data_leda_play = data_leda_play.reset_index(drop = True)
                data_clicker = data_clicker.reset_index(drop = True)
                itrClick = 0
                listCliker = []
                for itrLedaLab in range(len(data_leda_play)):
                    sums_click = 0
                    time_play = data_leda_play["Timestamp"][itrLedaLab]
                    while((itrClick < len(data_clicker)) and (data_clicker["Timestamp"].apply(make_timestamnp)[itrClick] < time_play)):
                        #print("",itrLedaLab,itrClick)
                        sums_click = sums_click + data_clicker["clicker_input"][itrClick]
                        itrClick = itrClick + 1
                    listCliker.append(sums_click)
                
                data_leda_play["Clicker"] = listCliker
                
                #Saving files
                fileData = os.path.join(fileSaves,'pData'+files_EDA[idx][19:21]+'.csv')
                data_leda_play.to_csv(fileData, index = False)
            else:
                print(str(idx)+" is courrupt")
        else:
            print("False-Name")
         
    #end of for loop        
    print('      Please check flags:',idxflag)
else:    
    print("False-Length")        
#%% complied the files
os.chdir(fileSaves)    
fileSaveslist = os.listdir(fileSaves)
i = 0
for file in fileSaveslist:
    if(i == 0):
        result = pd.DataFrame.from_csv(file,index_col=None)
        #result = result.drop(['Unnamed: 0'], axis=1)
        i = i+1
    else:
        temp = pd.DataFrame.from_csv(file,index_col=None)
        #temp = temp.drop(['Unnamed: 0'], axis=1)
        result = result.append(temp)
result = result.reset_index(drop=True)     
result.to_csv(file_complied)
#%%
result.peak = result.peak.astype(float)


resultGroup = result.groupby(['Latitude','Longitude'], as_index=False).mean()

mode = lambda x: stats.mode(x)[0][0] if len(x) > 0 else 0
resultGroupCLick = result.groupby(['Latitude','Longitude']).Clicker.apply(mode)
#resultGroup.to_csv(file_groupClick)
#del  resultGroup["Cliker"]
resultGroup["Clicker"] = resultGroupCLick.tolist()
resultGroup.to_csv(file_groupXY)



#file_peak = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','peakXY.csv')
#resultPeak = result[result["peak"] != 0].reset_index(drop=True)   
#resultPeak = resultPeak.groupby(['Latitude','Longitude'], as_index=False)
#resultPeak.to_csv(file_peak)

