#%% imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
from scipy import stats
#%% retrive data
participant_data_path = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\Participant_Data"
diretory_eda_sliced = participant_data_path+"\\sliced_eda_data"
file_list_edas = os.listdir(diretory_eda_sliced)
#fetch the eda_marked_results
event_data_sliced,length_list = collect_regular_sliced_edas(diretory_eda_sliced,file_list_edas)
columns_list = event_data_sliced.columns.tolist()
columns_list.sort(key=float)
event_data_sliced = event_data_sliced.reindex(columns=columns_list)  
event_data_sliced.to_csv("sliced_eda_combined.csv")
#%% collect_regular_results
def collect_regular_sliced_edas(diretory,file_list):
    list_of_EDAs = []
    participants_name = []
    length_list = []
    for i in range(len(file_list)):
        result_file = os.path.join(diretory, file_list[i])
        result_data = pd.DataFrame.from_csv(result_file)
        #print(i," ",file_list[i],":", len(result_data["Event"]))
        participant = ""
        if i > 25:
            participant = file_list[i][16:17]
        else:
            participant = file_list[i][16:18]
        
        print(participant)
        ithlist = result_data["EDA"].tolist()
        list_of_EDAs.append(ithlist)
        
        length_list.append(len(ithlist))
        participants_name.append(participant)

    event_data = pd.DataFrame(list_of_EDAs)
    event_data = event_data.transpose()
    event_data.columns = participants_name
    
    return event_data,length_list    

#%% recive and manupulate ts data fro unequal to equal 
path = "./"
file_list_sliced = os.path.join(path, "sliced_eda_combined.csv")
data = pd.DataFrame.from_csv(file_list_sliced)
data = data.fillna(0)
data.to_csv("sliced_eda_interpolated.csv")


#%% box plot of EDA peaks distrubtion analysis
filepath = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\ESUM_qunatified_data"
filename_raw = "5s_data_filtered_ml_with_sensor_loss.csv"
filename_smooth = "5s_smooth_withsensot_loss.csv"

#gps_sensor_data_merged_file = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\processesed_data_gps.csv"
raw_data = pd.DataFrame.from_csv(os.path.join(filepath,filename_raw))
raw_data = raw_data.fillna(0)

smooth_data = pd.DataFrame.from_csv(os.path.join(filepath,filename_smooth))
smooth_data = smooth_data.fillna(0)


#For sumaary of the box plot
df_box = pd.DataFrame({'A' : []})
df_box["Original"] = raw_data["EDA_peaks"].tolist()
del df_box["A"]
df_box.describe()

df_box = pd.DataFrame({'A' : []})
df_box["Smooth"] =  smooth_data["EDA_peaks"].tolist()
del df_box["A"]
df_box.describe()



fig = plt.figure(figsize=(5, 3))
fig = df_box.plot.box(vert=True).get_figure()
plt.ylabel("nSCR")
plt.show()
fig.savefig('eda_peak_range.pdf')

#plt.style.use('ggplot')
plt.style.use('grayscale')
plt.style.use('default')
#data = [1,2,3,4,5,6,7,8,9]
# basic plot

fig = plt.figure(figsize=(5.5, 3.8))
#plt.hist(data)
x = np.asarray(raw_data["EDA_peaks"].tolist())
y = np.asarray(smooth_data["EDA_peaks"].tolist())
data =[x,y]
plt.hist(data,  alpha=0.7, label=['Original', 'Smooth'], color = ["black","gray"])
#plt.hist(data,  alpha=0.7, label=['Original', 'Smooth'])
plt.legend(loc='upper right')
#plt.title("EDA peak distribution analysis")
plt.xlabel("nSCR")
plt.ylabel("Frequency")
fig.savefig('eda_peak_range_hist.pdf')
fig.savefig('eda_peak_range_hist.png')
plt.show()




#histogram
data = smooth_data["Light"].tolist()
fig = plt.figure(figsize=(4, 4))
hist, bins = np.histogram(data)
width = 0.9 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', color = "royalblue", width=width)
#plt.title("Light value distribution")
#plt.xlabel("Sound")
#plt.xlabel("Dust")
#plt.xlabel("Temperature")
#plt.xlabel("Relative Humidity")
plt.xlabel("Illuminance")
#plt.xlabel("Area")
#plt.ylabel("Frequency")
fig.savefig('hist_light.pdf')
fig.savefig('hist_light.jpg')
plt.show()


# notched plot
plt.figure()
plt.boxplot(data, 1)
plt.ylim((-10,50))
# change outlier point symbols
plt.figure()
plt.boxplot(data, 0, 'gD')
plt.set_xticklabels("EDA Peaks")
plt.get_xaxis().tick_bottom()
plt.xlabel("EDA Peaks")


#horizontal box plot
data =  [raw_data["EDA_peaks"].tolist(), smooth_data["EDA_peaks"].tolist()]
# don't show outlier points
plt.figure()
plt.boxplot(data, 0, '')

# horizontal boxes
fig = plt.figure(figsize=(5, 3))
#plt.figure()
labels1 = ['Original', 'Smooth']
bp = plt.boxplot(data, 
                 vert=True,  # vertical box alignment
                 notch=True,
                 patch_artist=False,  # fill with color
                 labels=labels1)
#bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
plt.setp(bp['boxes'])
plt.setp(bp['whiskers'], color='gray')
plt.setp(bp['fliers'],  marker='+')
plt.ylabel("nSCR")
#plt.xlabel("SC data")
# fill with colors

colors = ['gray', 'lightgray']
for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
#plt.title("EDA peak range analysis")
fig.savefig('eda_peak_range.pdf',facecolor='white', transparent=False)
fig.savefig('eda_peak_range.png',facecolor='white', transparent=False)
plt.show()



# change whisker length
plt.figure()
plt.boxplot(data, 0, 'rs', 0, 0.75)

# fake up some more data
spread = np.random.rand(50) * 100
center = np.ones(25) * 40
flier_high = np.random.rand(10) * 100 + 100
flier_low = np.random.rand(10) * -100
d2 = np.concatenate((spread, center, flier_high, flier_low), 0)
data.shape = (-1, 1)
d2.shape = (-1, 1)
# data = concatenate( (data, d2), 1 )
# Making a 2-D array only works if all the columns are the
# same length.  If they are not, then use a list instead.
# This is actually more efficient because boxplot converts
# a 2-D array into a list of vectors internally anyway.
data = [data, d2, d2[::2, 0]]
# multiple box plots on one figure
plt.figure()
plt.boxplot(data)

plt.show()

fig.savefig('test2png.png', dpi=100)