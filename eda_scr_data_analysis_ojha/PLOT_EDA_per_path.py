#%% imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
#%% retrive data
diretory ="C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\eda_Ledalab_analysis\\path_data_only\\results"
file_list = os.listdir(diretory)
del file_list[0]
del file_list[4]


event_data = pd.DataFrame({'A' : []})
for i in range(len(file_list)):
    result_file = os.path.join(diretory, file_list[i])
    result_data = pd.read_excel(result_file,sheetname='ERA')
    print(i," ",file_list[i],":", len(result_data["Event"]))
    participant = ""
    if i > 15:
        participant = file_list[i][12:13]
    else:
        participant = file_list[i][12:14]
        
    event_data[participant] = result_data["CDA.nSCR"].tolist()

del event_data['A']

participant_data_path = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\Participant_Data"
event_name_file = participant_data_path+"\\category_list_name.txt"
event_names_text = open(event_name_file, "r")
event_names = event_names_text.readlines()

#event_data["Event Name"] = event_names

#event_data.to_csv("Combined_Results.csv")

#%% even duration
event_duration = pd.DataFrame.from_csv('total_time_duration.csv',header = None)
average_event_duration = []
for i in range(len(event_duration)):
    average_event_duration.append(event_duration.index[i]/len(file_list))
    
col_list= list(event_data) 
#col_list.remove('d')
event_data['sum'] = event_data[col_list].sum(axis=1)
eda_response_sum =  event_data["sum"].tolist() 
average_eda_response = [] 
for i in range(3,len(event_duration)-1):
    average_eda_response.append(eda_response_sum[i]/average_event_duration[i])



import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(7, 4))
#objects = ('Start', 'Story', 'Pre-walk', 'Walk to 1', '1-2', '2-3','3-4','4-5','5-6','6-7','7-8',
#           '8-9','9-10','10-11','11-12','12-13','13-14','14-Finish')

events_name_int =  [i+1 for i in range(len(average_eda_response))]
y_pos = np.arange(len(events_name_int))

plt.bar(y_pos, average_eda_response, align='center', alpha=0.5, color = "royalblue")
plt.xticks(y_pos, events_name_int)
plt.ylabel('Normalized nSCR')
plt.xlabel('Path Segments')
#plt.title('EDA anlsysis of participants')
plt.show()
fig.savefig('eda_average_arousal.pdf')
plt.close(fig)

#%% stacked bar chart or area

data = event_data.as_matrix()
data = np.delete(data,[0,1,2,17],axis=0)
data = np.transpose(data)
ind = np.arange(data.shape[1])


bottom = np.vstack((np.zeros((data.shape[1],), dtype=data.dtype),
                    np.cumsum(data, axis=0)[:-1]))

cmap = plt.cm.get_cmap("hsv", data.shape[0]+1)
colors = []
for i in range(data.shape[0]):
    colors.append(cmap(i))

fig = plt.figure(figsize=(7, 4))
for dat, col, bot in zip(data, colors, bottom):
    plt.bar(ind, dat, color=col, bottom=bot)

plt.ylabel('Sum of all participant\'s nSCR')
plt.xlabel('Path Segments')
#plt.title('EDA analysis of path points')  
events_name_int =  [i+1 for i in range(data.shape[1])]
plt.xticks(ind,events_name_int)
#plt.text(0, 12, r'Start', rotation =  'vertical')
#plt.text(1, 3500, r'Bed-time story', rotation =  'vertical') 
#plt.text(2, 5000, r'Before walk start', rotation =  'vertical') 
#plt.text(3, 2700, r'Walk start to point 1', rotation =  'vertical') 
#plt.text(4, 1500, r'Point 1 to 2', rotation =  'vertical')
#plt.text(5, 2200, r'Point 2 to 3', rotation =  'vertical')
#plt.text(6, 1550, r'Point 3 to 4', rotation =  'vertical') 
#plt.text(7, 2000, r'Point 4 to 5', rotation =  'vertical')
#plt.text(8, 1800, r'Point 5 to 6', rotation =  'vertical') 
#plt.text(9, 1600, r'Point 6 to 7', rotation =  'vertical') 
#plt.text(10, 1600, r'Point 7 to 8', rotation =  'vertical') 
#plt.text(11, 1400, r'Point 8 to 9', rotation =  'vertical')
#plt.text(12, 2100, r'Point 9 to 10', rotation =  'vertical') 
#plt.text(13, 2000, r'Point 10 to 11', rotation =  'vertical') 
#plt.text(14, 1800, r'Point 11 to 12', rotation =  'vertical') 
#plt.text(15, 2100, r'Point 12 to 13', rotation =  'vertical') 
#plt.text(16, 2000, r'Point 13 to 14', rotation =  'vertical')
#plt.text(17, 2800, r'Point 14 to End', rotation =  'vertical') 
fig.savefig('eda_analysis.pdf')
plt.show()
plt.close(fig)
#%% Example
ind = np.arange(3)
a = [3,6,9]
b = [2,7,1]
c = [0,3,1]
d = [4,0,3]

data = np.array([a, b, c, d])
bottom = np.vstack((np.zeros((data.shape[1],), dtype=data.dtype),np.cumsum(data, axis=0)[:-1]))

colors = ('#ff3333', '#33ff33', '#3333ff', '#33ffff')
for dat, col, bot in zip(data, colors, bottom):
    plt.bar(ind, dat, color=col, bottom=bot)
    
plt.text(0.0, 12, r'$\mu=100,\ \sigma=15$', rotation =  'vertical') 
plt.text(1.0, 12, r'Green dominance', rotation =  'vertical') 

#%%
plt.style.use('ggplot')
file = "gps_data_5s_filtered.csv"
data = pd.read_csv(file)
df = data["TempEN"]

fig = plt.figure(figsize=(9, 7))
df.plot.hist(stacked=True, bins=20)
plt.xlabel('Environment Temperature')
fig.savefig('TempEN_hist.pdf')
plt.close(fig)