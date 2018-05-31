#importing packages
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
filepath = participant_data_path

#%% Main loop
for i in [5,6,8,10,11,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]:
    i = 5
    participant = str(i)
    if i < 10:
        participant = "0"+participant
    
    print("EDA data Marking participant: ",participant)
    eda_data = retrive_eda(filepath,participant) #fetching eda data
    tags_time_list = retrive_tag_time(filepath,participant) #fetching eda data
    status_time_list = retrive_status(filepath,participant) #fetching status time data
    
    eda_start_time =  dateutil.parser.parse(eda_data.index[1].strftime('%Y-%m-%d %H:%M:%S.%f'))
    eda_end_time =  dateutil.parser.parse(eda_data.index[len(eda_data)-1].strftime('%Y-%m-%d %H:%M:%S.%f'))
    
    print_time_order(eda_start_time,eda_end_time,tags_time_list,status_time_list)  
    eda_data,event_duration,category_name_list = creat_marker(eda_data,eda_start_time,eda_end_time,tags_time_list,status_time_list)
    save_results(filepath,participant,i,eda_data,event_duration,category_name_list)
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
    sampleRate = float(eda_data.iloc[0][0])
    eda_data = eda_data[eda_data.index!=0]
    eda_data.index = eda_data.index-1
    
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
    marker = np.empty(len(eda_data))
    marker.fill(-1)
    #eda_data["marker"] = np.zeros(len(eda_data))
    eda_data["marker"] = marker
    eda_data["event_marker"] = np.zeros(len(eda_data))
    #eda_data["class"] = np.zeros(len(eda_data))

    #upsampling
    #eda_data = eda_data.resample('125L').mean()
    #eda_data = eda_data.interpolate()

    #eda_data.head()
    #eda_data.tail()
    return eda_data

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
      
    #chaking first marker
    #tags_time_list[0]
    #status_time_list[0]
    #eda_data.index[0]
    #mask_time_list[0]
                
    #chaking las marker
    #tags_time_list[len(tags_time_list)-1]
    #status_time_list[len(status_time_list)-1]
    #eda_data.index[len(eda_data)-1]
    #mask_time_list[len(mask_time_list)-1]


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
    for i in range(len(mask_time_list)):
        for j in range(len(eda_data)):
            curr_time =  dateutil.parser.parse(eda_data.index[j].strftime('%Y-%m-%d %H:%M:%S.%f'))
            if (eda_data["marker"][j] == -1.0) and (curr_time <= mask_time_list[i]):
                eda_data["marker"][j] = i
    
    print("marker assigned")

    event = 1
    eda_data["event_marker"][0] = event
    event += 1
    duration = 0.0
    event_duration = []
    for j in range(1,len(eda_data)):
        duration += 0.250
        if (eda_data["marker"][j-1] != eda_data["marker"][j]):
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
#%% marking and event marking
def creat_marker_regular_interval(eda_data,eda_start_time,eda_end_time,tags_time_list,status_time_list):
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
    for i in range(len(mask_time_list)):
        for j in range(len(eda_data)):
            curr_time =  dateutil.parser.parse(eda_data.index[j].strftime('%Y-%m-%d %H:%M:%S.%f'))
            if (eda_data["marker"][j] == -1.0) and (curr_time <= mask_time_list[i]):
                eda_data["marker"][j] = i
    
    print("marker assigned")

    event = 1
    eda_data["event_marker"][0] = event
    event += 1
    duration = 0.0
    event_duration = []
    for j in range(1,len(eda_data)):
        duration += 0.250
        if (eda_data["marker"][j-1] != eda_data["marker"][j]):
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
#%% wrting to a file
def save_results(filepath,participant,i,eda_data,event_duration,category_name_list):
    save_filepath = os.path.join(filepath, participant)
    eda_out_file = os.path.join(save_filepath,"EDA_data_out.csv")
    eda_out_file1 =  os.path.join(save_filepath,'leda_exp_'+str(i)+'.txt')
    eda_out_file2 =  os.path.join(save_filepath,'eventduration_exp_'+str(i)+'.txt')
    eda_out_file3 =  os.path.join(save_filepath,'category_list_name.txt')

    list1 = eda_data["time"].tolist()
    list2 = eda_data["EDA"].tolist()
    list3 = eda_data["event_marker"].tolist()
    eda_data_out = list(zip(list1,list2,list3))
    
    eda_data.to_csv(eda_out_file)
    np.savetxt(eda_out_file1, eda_data_out, delimiter="\t", fmt='%s')
    np.savetxt(eda_out_file2, event_duration, delimiter="\n", fmt='%s')
    np.savetxt(eda_out_file3, category_name_list, delimiter="\n", fmt='%s')
   

#%% Date time Timestamp tests
#tm = '1970-01-01 06:00:00 +0500'
#tm = '2016-04-07 11:51:06.500'
##fmt = '%Y-%m-%d %H:%M:%S %z'
#fmt = '%Y-%m-%d %H:%M:%S.%f'
#time1 = timegm(datetime.strptime(tm, fmt).utctimetuple())
#
#
#start_status_time1 = dateutil.parser.parse(status_data.index[1].strftime('%Y-%m-%d %H:%M:%S.%f'))
#start_eda_time1 = dateutil.parser.parse(eda_data.index[1].strftime('%Y-%m-%d %H:%M:%S.%f'))
#
#
#end_status_time1 = dateutil.parser.parse(status_data.index[len(status_data)-1].strftime('%Y-%m-%d %H:%M:%S.%f'))
#end_eda_time1 = dateutil.parser.parse(eda_data.index[len(eda_data)-1].strftime('%Y-%m-%d %H:%M:%S.%f'))
#red_end_status_time1 = end_status_time1  + timedelta(hours=-2)
#
#
#start_eda_datetime =  dateutil.parser.parse(eda_data.index[1].strftime('%Y-%m-%d %H:%M:%S.%f'))
#end_eda_datetime =  dateutil.parser.parse(eda_data.index[5].strftime('%Y-%m-%d %H:%M:%S.%f'))
#type(start_eda_datetime)
#
#mask = eda_data.index
#for i in range(len(mask)):
#    mask[i] =  dateutil.parser.parse(eda_data.index[i].strftime('%Y-%m-%d %H:%M:%S.%f'))
#
#
#
#start_eda_datetime = start_eda_datetime.timestamp()
#end_eda_datetime = end_eda_datetime.timestamp()
#type(start_eda_datetime)
#
#eda_data[start_eda_datetime:end_eda_datetime]
#eda_data[eda_data.index[1]:eda_data.index[5]]
#eda_data[eda_data[eda_data.index[:] < eda_data.index[5]]

#%% ploting eda data
eda_response = eda_data["EDA"].tolist()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
fig = plt.figure(figsize=(9, 7))
plt.plot(eda_response)
plt.ylabel('EDA response')
plt.xlabel('Time ($\mu$s)')
plt.title('Raw EDA response of a participant')  
fig.savefig('eda_response.pdf')
plt.close(fig)


#B       business day frequency
#C       custom business day frequency (experimental)
#D       calendar day frequency
#W       weekly frequency
#M       month end frequency
#SM      semi-month end frequency (15th and end of month)
#BM      business month end frequency
#CBM     custom business month end frequency
#MS      month start frequency
#SMS     semi-month start frequency (1st and 15th)
#BMS     business month start frequency
#CBMS    custom business month start frequency
#Q       quarter end frequency
#BQ      business quarter endfrequency
#QS      quarter start frequency
#BQS     business quarter start frequency
#A       year end frequency
#BA      business year end frequency
#AS      year start frequency
#BAS     business year start frequency
#BH      business hour frequency
#H       hourly frequency
#T       minutely frequency
#S       secondly frequency
#L       milliseonds
#U       microseconds
#N       nanoseconds