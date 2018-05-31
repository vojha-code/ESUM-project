""""
Last Modifed: 01 June 2017: 16:12 
@author: Varun Ojha 
This program marke process EDA signal.
It works on EDA dat was taken from Empatica output
EDA singal works on 4 Hz frequency

:::Inputs files:::
    EDA.csv marked in t seconds
    tag.csv
    status.csv
    data_all_par#.csv

:::Outputs files:::
    "EDA_data_path_marked.csv"
    'Marker_path_'+str(i)+'.txt'
    'Event_duration_path_'+str(i)+'.txt'
    'Category_names_path.txt'
    
    "EDA_data_"+str(time_window)+"s_marked.csv"
    "Marker_"+str(time_window)+"s_"+str(i)+".txt"
    "Event_duration_"+str(time_window)+"s_"+str(i)+".txt"
    
    "GPS_data_"+str(time_window)+"s_marked.csv"
    "GPG_loc_"+str(time_window)+"s_"+str(i)+".txt"

"""
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
participant_data_path = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\Participant_Data"
filepath_gps_data = participant_data_path+"\\all_participants"
#%% retrive eda data
def retrive_eda(filepath,participant):
    # inputs from system
    #filepath = input("Path to E4 directory: ")
    eda_filepath = os.path.join(filepath, participant)
    # retiving EDA file
    eda_file =  os.path.join(eda_filepath,'EDA.csv')

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
    #eda_data["marker"] = np.zeros(len(eda_data))
    eda_data["path_marker"] = marker
    #eda_data["regular_marker"] = marker
    eda_data["event_marker"] = np.zeros(len(eda_data))
    eda_data["event_marker_regular"] = np.zeros(len(eda_data))
    #eda_data["class"] = np.zeros(len(eda_data))

    #upsampling
    #eda_data = eda_data.resample('125L').mean()
    #eda_data = eda_data.interpolate()

    #eda_data.head()
    #eda_data.tail()
    return eda_data
#%%tags time
def retrive_tag_time(filepath,participant):
    tags_filepath = os.path.join(filepath, participant)
    tags_file =  os.path.join(tags_filepath,'tags.csv')
    tag_data = pd.DataFrame.from_csv(tags_file,header=None)
    
    tags_time_list = []
    for i in range(len(tag_data)):
        tag_time = datetime.utcfromtimestamp(tag_data.index[i]).strftime('%Y-%m-%d %H:%M:%S.%f')
        tags_time_list.append(dateutil.parser.parse(tag_time))
    
    #tag_data
    #for i in range(len(tags_time_list)):
        #    print(i,": ",tags_time_list[i])
    
    #create mask time list
    #len(status_time_list)
    #len(tags_time_list)
    return tags_time_list
#%%status file retrival
def retrive_status(filepath,participant):
    #statusfile
    status_filepath = os.path.join(filepath, participant)
    status_file =  os.path.join(status_filepath,'status.csv')
    #status_data = pd.read_csv(status_file, header=None)
    status_data = pd.DataFrame.from_csv(status_file,header=None)
    
    #reducing time of status clock
    status_time_list = []
    for i in range(len(status_data)):
        #print(i,": ",status_data.index[i])
        if(isinstance(status_data.index[i], np.float64) or isinstance(status_data.index[i], np.int64)):
            status_time = datetime.utcfromtimestamp(status_data.index[i]).strftime('%Y-%m-%d %H:%M:%S.%f')
            status_time = dateutil.parser.parse(status_time)
            red_status_time = status_time  + timedelta(hours=-2)
            status_time_list.append(red_status_time)
        else:
            status_time = dateutil.parser.parse(status_data.index[i].strftime('%Y-%m-%d %H:%M:%S.%f'))
            red_status_time = status_time  + timedelta(hours=-2)
            status_time_list.append(red_status_time)
        #print(": ",status_time_list[i])
        
        #printing status time    
        #for i in range(len(status_time_list)):
            #    print(i,": ",status_time_list[i])
    return status_time_list
#%% retirive gps information
def retrive_gps_data(filepath_gps_data,i):
    #i = 7
    gps_file_name = "data_all_"+str(i)+".csv"
    gps_file =  os.path.join(filepath_gps_data,gps_file_name)
    print(gps_file[-6:])
    
    gps_data = pd.DataFrame.from_csv(gps_file,header=None)
    gps_data = gps_data.iloc[:,[i+4 for i in range(8)]]
    del gps_data[10]
    
    #correction of sound and dust values
    sound = gps_data[5].tolist()
    dust = gps_data[6].tolist()
    #sound interpolation
    i = 0
    while(i < len(gps_data)):
        j = i +1
        try:
            while(True):
                if(sound[i] == sound[j]):
                    sound[j] = np.NaN
                    j += 1
                else:
                    i = j
                    break
        except IndexError:
            break
                            
    gps_data[0] =  sound   
    gps_data = gps_data.interpolate(method='linear')#linear interpolation
    
    #dust interpolation
    i = 0
    while(i < len(gps_data)):
        j = i +1
        try:
            while(True): #finding forward repeating values
                if(dust[i] == dust[j]):
                    dust[j] = np.NaN # assingning NaN to each repeating values
                    j += 1
                else:
                    i = j
                    break
        except IndexError:
            break        
    
    gps_data[1] =  dust #new dust values          
    gps_data = gps_data.interpolate(method='linear') #linear interpolation
    
    del gps_data[5]# deleting columns for old values
    del gps_data[6]# deleting columns for old values
    gps_data = gps_data.rename(columns={0: 5, 1: 6})# renaming column "0" to "5"
    gps_data = gps_data.sort_index(axis=1)# renaming column "1" to "6"
    
    
    # retining time list for further comparision with tags and time list
    gps_time_list = []  
    for i in range(len(gps_data)):
        gps_time = datetime.utcfromtimestamp(gps_data.index[i]).strftime('%Y-%m-%d %H:%M:%S.%f')
        gps_time = dateutil.parser.parse(gps_time)
        red_gps_time = gps_time  + timedelta(hours=-2)
        gps_time_list.append(red_gps_time)
        
        if(gps_data[11].iloc[i] == 0.0):
            gps_data[11].iloc[i] = np.nan
        
        if(gps_data[12].iloc[i] == 0.0):
            gps_data[12].iloc[i] = np.nan
        
    gps_data = gps_data.interpolate(method='linear')
    
    return gps_data,gps_time_list
#%% printing the time order
def print_time_order(eda_start_time,eda_end_time,tags_time_list,status_time_list):
    #Checking
    # eda_start <= T1 < T2 < T3 < S1 < S2 < S3 <..... < S14 < T4 <= eda_end
    if (eda_start_time <= tags_time_list[0]): # edat start  <= tag 1
        print("EDA start <= T1")
    else:
        print("EDA start > T1: SOMETHING WRONG",eda_start_time," <= ", tags_time_list[0])
    
    if (tags_time_list[1] <= tags_time_list[2]): #tag 2 < tag3 
        print("T1 <= T2 ")
    else:
        print("T1 > T2 :  SOMETHING WRONG", tags_time_list[1], "<=  ", tags_time_list[2])
    
    if (tags_time_list[2] <= status_time_list[0]): # tage 3 < status 1
        print("T3 <= S1 ")
    else:
        print("T3 > S1 :  SOMETHING WRONG", tags_time_list[2], " < =", status_time_list[0])
    
    if (status_time_list[13] <= tags_time_list[3]):  #  status 14 < tag 4
        print("S14 <= T4 ")
    else:
        print("S14 > T4 :  SOMETHING WRONG", status_time_list[13], " <= ", tags_time_list[3])
    
    if (tags_time_list[3] <= eda_end_time):
        print("T4 <= EDA end ")
    else:
        print("T4 > Eda end:  SOMETHING WRONG", tags_time_list[3]," <= ", eda_end_time)
#%% marking and event marking
def creat_marker(eda_data,eda_start_time,eda_end_time,tags_time_list,status_time_list):
    # eda_start <= T1 < T2 < T3 < S1 < S2 < S3 <..... < S14 < T4 <= eda_end
    category_name_list = []
    mask_time_list = []
    #mark 0
    mask_time_list.append(tags_time_list[0]) # tag 1
    category_name_list.append("Eda start < T1")
    #mark 1
    mask_time_list.append(tags_time_list[1]) # tag 2
    category_name_list.append("T1 < T2")
    #mark 2
    mask_time_list.append(tags_time_list[2])# tag 3
    category_name_list.append("T2 < T3")
    
    #mark 2-one last
    for i in range(0,len(status_time_list)):
        string_name = ""
        if (status_time_list[i] > tags_time_list[3]):
            mask_time_list.append(tags_time_list[3]) # if s14 < tage4
            string_name = "S"+str(i+1)+" > T4"
            category_name_list.append(string_name)
        else:
            mask_time_list.append(status_time_list[i])
            if(i == 0):
                string_name = "T3 < S"+ str(i+1)
            else:
                string_name = "T"+str(i+1)+" < S"+ str(i+2)
            category_name_list.append(string_name)

    #last marer if exist
    if (mask_time_list[len(mask_time_list)-1] < eda_end_time):
        mask_time_list.append(eda_end_time)
        string_name = "T4/S14 < EDA end"
        category_name_list.append(string_name)
            
    #creating marker
    #eda_data = marker_assignment(eda_data,mask_time_list,"path_marker")
    #for i in range(len(mask_time_list)):
    #   for j in range(len(eda_data)):
    #        curr_time =  dateutil.parser.parse(eda_data.index[j].strftime('%Y-%m-%d %H:%M:%S.%f'))
    #        if (eda_data["path_marker"][j] == -1.0) and (curr_time <= mask_time_list[i]):
    #            eda_data["path_marker"][j] = i
                #print("mark: ",i)
    #print("marker assigned")
    #creating marker
    j = 0
    count = 0
    for i in range(len(eda_data)):
        if (eda_data["path_marker"][i] == -1.0):
            curr_time =  dateutil.parser.parse(eda_data.index[i].strftime('%Y-%m-%d %H:%M:%S.%f'))
            if (curr_time <= mask_time_list[j]):
                eda_data["path_marker"][i] = j
                #print("mark: ",j)
                count +=1
            else:
                j +=1
                eda_data["path_marker"][i] = j
                #print("mark: ",j)
                count +=1
    
    print("path_marker","assigned",count)

    event = 1
    eda_data["event_marker"][0] = event
    event += 1
    duration = 0.0
    event_duration = []
    for j in range(1,len(eda_data)):
        duration += 0.250
        if (eda_data["path_marker"][j-1] != eda_data["path_marker"][j]):
                eda_data["event_marker"][j] = event
                event += 1
                event_duration.append(duration)
                #print(duration)
                duration = 0
                
    event_duration.append(duration)
    #sum(event_duration)
    #eda_data["time"][len(eda_data)-1]

    if (len(event_duration)==event-1):
        print('Perfect: ',len(event_duration)," = ",(event-1))
    
    return eda_data,event_duration,category_name_list
#%%retive sliced eda singla betweenm two given time stamps
def retirive_sliced_eda_signal(tags_time_list,eda_data):
    slice_time_start = tags_time_list[2] # tag 3 is the fist point of slice
    slice_time_end = tags_time_list[3] # tag 4 is the end point of the slice
    
    #slicing eda
    slice_mask = []
    for i in range(len(eda_data)):
        curr_time =  dateutil.parser.parse(eda_data.index[i].strftime('%Y-%m-%d %H:%M:%S.%f'))
        if(curr_time >= slice_time_start and curr_time <= slice_time_end):
            slice_mask.append(True)
        else:
            slice_mask.append(False)
               
    sliced_eda_data = eda_data[slice_mask]
    
    return sliced_eda_data
#%% marke regular interval
def create_regular_marker(sliced_data,interval):    
    event = 1
    event_duration_regular = []
    sliced_data["event_marker_regular"][0] = event
    seconds = 0.000
    for i in range(len(sliced_eda_data)):
        if (seconds == interval):
            event_duration_regular.append(seconds)
            event += 1
            sliced_data["event_marker_regular"][i]= event
            seconds = 0.000   
        seconds += 0.250 # for 4Hz 
    
    # append last even only if it is about "seconds == slice_time_window"   
    if(seconds < (slice_time_window-0.50)):
        sliced_eda_data.loc[sliced_eda_data['event_marker_regular'] == event, 'event_marker_regular'] = 0.0
        #sliced_eda_data.loc[sliced_eda_data['event_marker_regular'] == event, 'EDA'].iloc[0] #only for retriving value
    else:
        event_duration_regular.append(seconds) #appending last event  
        
    if (len(event_duration_regular)==event):
        print('Perfect: ',len(event_duration_regular)," = ",(event))
    
    return sliced_data,event_duration_regular
#%% retrive gps data fro interval seconds
def retrive_gps_for_time(gps_data,gps_time_list,sliced_eda_data,event_duration_regular,interval,lenth_reduce):
    #
    time_list = []
    coradinate_x_list = []
    coradinate_y_list = []
    col_sound_list = []
    col_dust_list = []
    col_temp_en_list = []
    col_rh__list = []
    col_lisght__list = []
    
    index_gps = 0
    for i in range(len(event_duration_regular)-lenth_reduce):
        slice_time =  sliced_eda_data[sliced_eda_data["event_marker_regular"]==i].index
        gps_time =  gps_time_list[index_gps]        
        slice_time_is_less_than_gps = (slice_time < gps_time)[0]
        if(slice_time_is_less_than_gps and index_gps < len(gps_data)):
            index_gps = index_gps
        else:
            index_gps = index_gps + interval
        
        print(index_gps)
            
        seconds = 0
        sound  = 0.0
        dust  = 0.0
        temp  = 0.0
        rh  = 0.0
        light  = 0.0
        time_list.append(slice_time[0])
        coradinate_x_list.append(gps_data[11].iloc[index_gps])
        coradinate_y_list.append(gps_data[12].iloc[index_gps])
        
        for j in range(interval):
            if(j+index_gps):
                sound = sound + gps_data[5].iloc[j+index_gps]
                dust = dust + gps_data[6].iloc[j+index_gps]
                temp = temp + gps_data[7].iloc[j+index_gps]
                rh = rh + gps_data[8].iloc[j+index_gps]
                light = light + gps_data[9].iloc[j+index_gps]
                

            
        col_sound_list.append(sound/interval)
        col_dust_list.append(dust/interval)
        col_temp_en_list.append(temp/interval)
        col_rh__list.append(rh/interval)
        col_lisght__list.append(light/interval)

    collected_data = pd.DataFrame({'A' : []}) 
    collected_data["time"] = time_list
    collected_data["X"] = coradinate_x_list
    collected_data["Y"] = coradinate_y_list
    collected_data["Sound"] = col_sound_list
    collected_data["Dust"] = col_dust_list
    collected_data["TempEN"] = col_temp_en_list
    collected_data["RH"] = col_rh__list
    collected_data["Light"] = col_lisght__list
    del collected_data['A']
    gps_data_for_t = collected_data
    
    return collected_data
#%% assign marker
def marker_assignment(data,mask_time_list,colName):
    #creating marker
    j = 0
    count = 0
    for i in range(len(data)):
        if (data[colName][i] == -1.0):
            curr_time =  dateutil.parser.parse(data.index[i].strftime('%Y-%m-%d %H:%M:%S.%f'))
            if (curr_time <= mask_time_list[j]):
                data[colName][i] = j
                print("mark: ",j)
                count +=1
            else:
                j +=1
                data[colName][i] = j
                print("mark: ",j)
                count +=1
    
    print(colName,"assigned",count)
    return data
#%% wrting to a file
def save_results(filepath,participant,i,eda_data,event_duration,category_name_list):
    save_filepath = os.path.join(filepath, participant)
    eda_out_file = os.path.join(save_filepath,"EDA_data_path_marked.csv")
    eda_out_file1 =  os.path.join(save_filepath,'Marker_path_'+str(i)+'.txt')
    eda_out_file2 =  os.path.join(save_filepath,'Event_duration_path_'+str(i)+'.txt')
    eda_out_file3 =  os.path.join(save_filepath,'Category_names_path.txt')

    list1 = eda_data["time"].tolist()
    list2 = eda_data["EDA"].tolist()
    list3 = eda_data["event_marker"].tolist()
    eda_data_out = list(zip(list1,list2,list3))
    
    eda_data.to_csv(eda_out_file)
    np.savetxt(eda_out_file1, eda_data_out, delimiter="\t", fmt='%s')
    np.savetxt(eda_out_file2, event_duration, delimiter="\n", fmt='%s')
    np.savetxt(eda_out_file3, category_name_list, delimiter="\n", fmt='%s')
#%% save regular daya
def save_regular_results(filepath,participant,i,sliced_eda_data,event_duration):
    save_filepath = os.path.join(filepath, participant)
    eda_out_file = os.path.join(save_filepath,"EDA_data_"+str(time_window)+"s_marked.csv")
    eda_out_file1 =  os.path.join(save_filepath,"Marker_"+str(time_window)+"s_"+str(i)+".txt")
    eda_out_file2 =  os.path.join(save_filepath,"Event_duration_"+str(time_window)+"s_"+str(i)+".txt")

    list1 = sliced_eda_data["regular_time"].tolist()
    list2 = sliced_eda_data["EDA"].tolist()
    list3 = sliced_eda_data["event_marker_regular"].tolist()
    eda_data_out = list(zip(list1,list2,list3))
    
    sliced_eda_data.to_csv(eda_out_file)
    np.savetxt(eda_out_file1, eda_data_out, delimiter="\t", fmt='%s')
    np.savetxt(eda_out_file2, event_duration, delimiter="\n", fmt='%s')
#%% save regular daya
def save_gps_data_results(filepath,participant,i,gps_data_for_t):
    save_filepath = os.path.join(filepath, participant)
    eda_out_file = os.path.join(save_filepath,"GPS_data_"+str(time_window)+"s_marked.csv")
    eda_out_file1 =  os.path.join(save_filepath,"GPG_loc_"+str(time_window)+"s_"+str(i)+".txt")

    list1 = gps_data_for_t["X"].tolist()
    list2 = gps_data_for_t["Y"].tolist()
    eda_data_out = list(zip(list1,list2))
    
    gps_data_for_t.to_csv(eda_out_file)
    np.savetxt(eda_out_file1, eda_data_out, delimiter="\t", fmt='%s')
#%%
print("End of all function")


#%% Main loop
#[5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]:
#[15,16,19,21,33,34]:
    
slice_time_window = 5.000
time_window = int(slice_time_window)

#[5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]:
for i in [6,7,8,9,10,11,13,15,16,17,18,23,24,25,26,27,28,29,30,31,32,34,35]:
    #fix_file = 6
    lenth_reduce = 1 #default is zero
    #i = fix_file
    if(i == 15 or i == 16 or i ==18):
        lenth_reduce = 2
    
    if(i == 34 ):
        lenth_reduce = 15  

    if(i == 35 ):
        lenth_reduce = 6
        
    participant = str(i)
    if i < 10:
        participant = "0"+participant
    print("EDA data Marking participant: ",participant)
    # retiving EDA file
    gps_data,gps_time_list = retrive_gps_data(filepath_gps_data,i)#featching gps_data
    eda_data = retrive_eda(filepath,participant) #fetching eda data
    tags_time_list = retrive_tag_time(filepath,participant) #fetching eda data
    status_time_list = retrive_status(filepath,participant) #fetching status time data
    
    eda_start_time =  dateutil.parser.parse(eda_data.index[1].strftime('%Y-%m-%d %H:%M:%S.%f'))
    eda_end_time =  dateutil.parser.parse(eda_data.index[len(eda_data)-1].strftime('%Y-%m-%d %H:%M:%S.%f'))
    print_time_order(eda_start_time,eda_end_time,tags_time_list,status_time_list)  
    #marking evenits
    eda_data,event_duration,category_name_list = creat_marker(eda_data,eda_start_time,eda_end_time,tags_time_list,status_time_list)
    
    sliced_eda_data = retirive_sliced_eda_signal(tags_time_list,eda_data)
    
    sliced_eda_data,event_duration_regular = create_regular_marker(sliced_eda_data,slice_time_window)
    
    #creating only seconds list
    secondslist = np.zeros(len(sliced_eda_data))
    seconds = 0.000
    for j in range(len(secondslist)):
        secondslist[j] = seconds
        seconds += 0.250 # for 4Hz  
    sliced_eda_data["regular_time"] = secondslist
    #j = 0

    gps_data_for_t = retrive_gps_for_time(gps_data,gps_time_list,sliced_eda_data,event_duration_regular,int(slice_time_window),lenth_reduce)
    

    #i = fix_file
    #save_results(filepath,participant,i,eda_data,event_duration,category_name_list)
    save_regular_results(filepath,participant,i,sliced_eda_data,event_duration_regular)
    save_gps_data_results(filepath,participant,i,gps_data_for_t)
    print("Files saved")