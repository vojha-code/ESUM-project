# Required packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import scipy.stats as stats
import math

# Change directory
import os
#%% 
file_path = "C://Users//vojha//Dropbox//0_Programming//ESUM_Experiments//Participant_Data//gps_sensor_data//5s//smoot_signals//complied_data_filtered_with_ID.csv"
# Read in the data: Participants Biofeedback
#xl = pd.ExcelFile("Participants_Bio_feedback_data_dynamics.xlsx")
#xl.sheet_names for calling the name of the sheet. "Sheet1" is it in this excel sheet.
#bio = xl.parse("Sheet1")
file_path_demograph = "C://Users//vojha//Dropbox//0_Programming//ESUM_Experiments//Participant_Data//demography"

data = pd.read_csv(file_path)
#del data["Unnamed: 0"]#deleting unneccasry column
#histogram
#data = data["Area"].tolist()
#fig = plt.figure(figsize=(3.5, 3.8))
#hist, bins = np.histogram(data)
#width = 0.9 * (bins[1] - bins[0])
#center = (bins[:-1] + bins[1:]) / 2
#plt.bar(center, hist, align='center', color = "royalblue", width=width)
##plt.title("Light value distribution")
##plt.xlabel("Sound")
##plt.xlabel("Dust")
##plt.xlabel("Temperature")
##plt.xlabel("Relative Humidity")
#plt.xlabel("Area")
##plt.xlabel("Area")
##plt.ylabel("Frequency")
#fig.savefig('hist_area.pdf')
#fig.savefig('hist_area.jpeg')
#plt.show()


#result = data.sort(["participant"], ascending=[1,1])
#grouped_sum = data.groupby(['ID']).sum()
grouped_mean = data.groupby(['ID']).mean()
x_y_phase_peak = grouped_mean[['X','Y','Sound','Dust','TempEN','RH','Light','EDA_phase','EDA_peaks']]
x_y_phase_peak.to_csv("per_xy_pahse_mean_all_var.csv")
#normalized_grouped_mean =(x_y_phase_peak-x_y_phase_peak.min())/(x_y_phase_peak.max()-x_y_phase_peak.min())
cols_to_norm = ['Sound','Dust','TempEN','RH','Light','EDA_phase','EDA_peaks']
x_y_phase_peak[cols_to_norm] = x_y_phase_peak[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
normalized_grouped_mean = x_y_phase_peak
normalized_grouped_mean.to_csv("per_xy_pahse_mean_norm_all_var.csv")

#slicing the data frame participants wise
#[6,7,9,10,13,24,27,28,34,35]#native
#[8,11,16,23,25,26,29,30,31,32]#non-native  
#[6,8,9,10,11,16,23,25,27,28,29,30,31]#20-30
#[7,13,23,24,26,32,34,35]#30 and above

#%%
cols_to_norm = ['EDA_phase','EDA_peaks']
data[cols_to_norm] = data[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

#%%all participants
grouped_mean = data.groupby(['X', 'Y']).mean()
grouped_mean = grouped_mean[['EDA_phase','EDA_peaks']]
#grouped_mean.to_csv("per_xy_pahse_norm_mean.csv")

#%%
native = data[(data.participant == 6) | 
        (data.participant == 7)|
        (data.participant == 9)|
        (data.participant == 10)|
        (data.participant == 13)|
        (data.participant == 24)|
        (data.participant == 27)|
        (data.participant == 28)|
        (data.participant == 34)|
        (data.participant == 35)]

native_grouped_mean = native.groupby(['ID']).mean()
#native_grouped_mean = native_grouped_mean[['EDA_phase','EDA_peaks']]
native_grouped_mean = native_grouped_mean[['X','Y','EDA_phase','EDA_peaks']]



non_native = data[(data.participant == 8)|
        (data.participant == 11)|
        (data.participant == 16)|
        (data.participant == 23)|
        (data.participant == 25)|
        (data.participant == 26)|
        (data.participant == 29)|
        (data.participant == 30)|
        (data.participant == 31)|
        (data.participant == 32)]

non_native_grouped_mean = non_native.groupby(['ID']).mean()
#non_native_grouped_mean = non_native_grouped_mean[['EDA_phase','EDA_peaks']]
non_native_grouped_mean = non_native_grouped_mean[['X','Y','EDA_phase','EDA_peaks']]



min_a = native_grouped_mean[['EDA_phase','EDA_peaks']].min(axis=0).tolist()
min_b = non_native_grouped_mean[['EDA_phase','EDA_peaks']].min(axis=0).tolist()


max_a = native_grouped_mean[['EDA_phase','EDA_peaks']].max(axis=0).tolist()
max_b = non_native_grouped_mean[['EDA_phase','EDA_peaks']].max(axis=0).tolist()

min_phase = min([min_a[0],min_b[0]])
min_peak = min([min_a[1],min_b[1]])
max_phase = max([max_a[0],max_b[0]])
max_peak = max([max_a[1],max_b[1]])


cols_to_norm = ['EDA_phase']
native_grouped_mean["EDA_phase_norm"] = native_grouped_mean[cols_to_norm].apply(lambda x: (x - min_phase) / (max_phase - min_phase))
non_native_grouped_mean["EDA_phase_norm"] = non_native_grouped_mean[cols_to_norm].apply(lambda x: (x - min_phase) / (max_phase - min_phase))

cols_to_norm = ['EDA_peaks']
native_grouped_mean["EDA_peaks_norm"] = native_grouped_mean[cols_to_norm].apply(lambda x: (x - min_peak) / (max_peak - min_peak))
non_native_grouped_mean["EDA_peaks_norm"] = non_native_grouped_mean[cols_to_norm].apply(lambda x: (x - min_peak) / (max_peak - min_peak))



native_grouped_mean.to_csv("per_xy_pahse_norm_mean_native.csv")
non_native_grouped_mean.to_csv("per_xy_pahse_norm_mean_non_native.csv")


#%%age
age_20_30 = data[(data.participant == 6)|
        (data.participant == 8)|
        (data.participant == 9)|
        (data.participant == 10)|
        (data.participant == 11)|
        (data.participant == 16)|
        (data.participant == 23)|
        (data.participant == 25)|
        (data.participant == 27)|
        (data.participant == 28)|
        (data.participant == 29)|
        (data.participant == 30)|
        (data.participant == 31)]

age_20_30_grouped_mean = age_20_30.groupby(['ID']).mean()
#age_20_30_grouped_mean = age_20_30_grouped_mean[['EDA_phase','EDA_peaks']]
age_20_30_grouped_mean = age_20_30_grouped_mean[['X','Y','EDA_phase','EDA_peaks']]


age_30_above = data[(data.participant == 7)|
        (data.participant == 13)|
        (data.participant == 23)|
        (data.participant == 24)|
        (data.participant == 26)|
        (data.participant == 32)|
        (data.participant == 34)|
        (data.participant == 35)]

age_30_above_grouped_mean = age_30_above.groupby(['ID']).mean()
#age_30_above_grouped_mean = age_30_above_grouped_mean[['EDA_phase','EDA_peaks']]
age_30_above_grouped_mean = age_30_above_grouped_mean[['X','Y','EDA_phase','EDA_peaks']]



min_a = age_20_30_grouped_mean[['EDA_phase','EDA_peaks']].min(axis=0).tolist()
min_b = age_30_above_grouped_mean[['EDA_phase','EDA_peaks']].min(axis=0).tolist()


max_a = age_20_30_grouped_mean[['EDA_phase','EDA_peaks']].max(axis=0).tolist()
max_b = age_30_above_grouped_mean[['EDA_phase','EDA_peaks']].max(axis=0).tolist()

min_phase = min([min_a[0],min_b[0]])
min_peak = min([min_a[1],min_b[1]])
max_phase = max([max_a[0],max_b[0]])
max_peak = max([max_a[1],max_b[1]])


cols_to_norm = ['EDA_phase']
age_20_30_grouped_mean["EDA_phase_norm"] = age_20_30_grouped_mean[cols_to_norm].apply(lambda x: (x - min_phase) / (max_phase - min_phase))
age_30_above_grouped_mean["EDA_phase_norm"] = age_30_above_grouped_mean[cols_to_norm].apply(lambda x: (x - min_phase) / (max_phase - min_phase))

cols_to_norm = ['EDA_peaks']
age_20_30_grouped_mean["EDA_peaks_norm"] = age_20_30_grouped_mean[cols_to_norm].apply(lambda x: (x - min_peak) / (max_peak - min_peak))
age_30_above_grouped_mean["EDA_peaks_norm"] = age_30_above_grouped_mean[cols_to_norm].apply(lambda x: (x - min_peak) / (max_peak - min_peak))


age_20_30_grouped_mean.to_csv("per_xy_pahse_norm_mean_age_20_30.csv")
age_30_above_grouped_mean.to_csv("per_xy_pahse_norm_mean_age_30_above.csv")

#%%place
village_town = data[(data.participant == 6)|
        (data.participant == 7)|
        (data.participant == 24)|
        (data.participant == 27)|
        (data.participant == 28)|
        (data.participant == 32)|
        (data.participant == 34)|
        (data.participant == 35)]

village_town_mean = village_town.groupby(['ID']).mean()
#village_town_mean = village_town_mean[['EDA_phase','EDA_peaks']]
village_town_mean = village_town_mean[['X','Y','EDA_phase','EDA_peaks']]



city = data[(data.participant == 9)|
        (data.participant == 10)|
        (data.participant == 11)|
        (data.participant == 13)|
        (data.participant == 26)|
        (data.participant == 30)|
        (data.participant == 29)|
        (data.participant == 31)]

city_mean = city.groupby(['ID']).mean()
#city_mean = city_mean[['EDA_phase','EDA_peaks']]
city_mean = city_mean[['X','Y','EDA_phase','EDA_peaks']]


metropolis = data[(data.participant == 8)|
        (data.participant == 16)|
        (data.participant == 23)|
        (data.participant == 25)]

metropolis_mean = metropolis.groupby(['ID']).mean()
#metropolis_mean = metropolis_mean[['EDA_phase','EDA_peaks']]
metropolis_mean = metropolis_mean[['X','Y','EDA_phase','EDA_peaks']]


min_a = village_town_mean[['EDA_phase','EDA_peaks']].min(axis=0).tolist()
min_b = city_mean[['EDA_phase','EDA_peaks']].min(axis=0).tolist()
min_c = metropolis_mean[['EDA_phase','EDA_peaks']].min(axis=0).tolist()


max_a = village_town_mean[['EDA_phase','EDA_peaks']].max(axis=0).tolist()
max_b = city_mean[['EDA_phase','EDA_peaks']].max(axis=0).tolist()
max_c = metropolis_mean[['EDA_phase','EDA_peaks']].max(axis=0).tolist()

min_phase = min([min_a[0],min_b[0],min_c[0]])
min_peak = min([min_a[1],min_b[1],min_c[1]])
max_phase = max([max_a[0],max_b[0],max_c[0]])
max_peak = max([max_a[1],max_b[1],max_c[1]])


cols_to_norm = ['EDA_phase']
village_town_mean["EDA_phase_norm"] = village_town_mean[cols_to_norm].apply(lambda x: (x - min_phase) / (max_phase - min_phase))
city_mean["EDA_phase_norm"] = city_mean[cols_to_norm].apply(lambda x: (x - min_phase) / (max_phase - min_phase))
metropolis_mean["EDA_phase_norm"] = metropolis_mean[cols_to_norm].apply(lambda x: (x - min_phase) / (max_phase - min_phase))

cols_to_norm = ['EDA_peaks']
village_town_mean["EDA_peaks_norm"] = village_town_mean[cols_to_norm].apply(lambda x: (x - min_peak) / (max_peak - min_peak))
city_mean["EDA_peaks_norm"] = city_mean[cols_to_norm].apply(lambda x: (x - min_peak) / (max_peak - min_peak))
metropolis_mean["EDA_peaks_norm"] = metropolis_mean[cols_to_norm].apply(lambda x: (x - min_peak) / (max_peak - min_peak))

village_town_mean.to_csv("per_xy_pahse_norm_mean_village.csv")
city_mean.to_csv("per_xy_pahse_norm_mean_city.csv")
metropolis_mean.to_csv("per_xy_pahse_norm_mean_metro.csv")



#%% Stat
list_stat = []
A = native_grouped_mean['EDA_phase'].tolist()
B = non_native_grouped_mean['EDA_phase'].tolist()
stats.ttest_ind(a= A,b= B, equal_var=False)    # Assume samples have equal variance?
#stats.ks_2samp(A, B)


A = age_20_30_grouped_mean['EDA_phase'].tolist()
B = age_30_above_grouped_mean['EDA_phase'].tolist()
stats.ttest_ind(a= A,b= B, equal_var=False)    # Assume samples have equal variance?
stats.ks_2samp(A, B)

A = village_town_mean['EDA_phase'].tolist()
B = city_mean['EDA_phase'].tolist()
stats.ttest_ind(a= A,b= B, equal_var=False)    # Assume samples have equal variance?
#stats.ks_2samp(A, B)

A = village_town_mean['EDA_phase'].tolist()
B = metropolis_mean['EDA_phase'].tolist()
stats.ttest_ind(a= A,b= B, equal_var=False)    # Assume samples have equal variance?
#stats.ks_2samp(A, B)

A = city_mean['EDA_phase'].tolist()
B = metropolis_mean['EDA_phase'].tolist()
stats.ttest_ind(a= A,b= B, equal_var=False)    # Assume samples have equal variance?
#stats.ks_2samp(A, B)
#%%mean

list_sums = []
colum_to_sum = "EDA_peaks_norm"
list_sums.append(native_grouped_mean[colum_to_sum].mean())
list_sums.append(non_native_grouped_mean[colum_to_sum].mean())
list_sums.append(age_20_30_grouped_mean[colum_to_sum].mean())
list_sums.append(age_30_above_grouped_mean[colum_to_sum].mean())
list_sums.append(village_town_mean[colum_to_sum].mean())
list_sums.append(city_mean[colum_to_sum].mean())
list_sums.append(metropolis_mean[colum_to_sum].mean())
list_sums
#%%Combination point to point
result_ethenic =  pd.concat([native_grouped_mean, non_native_grouped_mean], axis=1, join_axes=[native_grouped_mean.index])
result_ethenic.columns = ["native_phase","native_peak","non_native_phase","non_native_peak"]

result_age =  pd.concat([age_20_30_grouped_mean, age_30_above_grouped_mean], axis=1, join_axes=[age_20_30_grouped_mean.index])
result_age.columns = ["age_tt_phase","age_tt_peak","age_ta_phase","age_ta_peak"]

result_place =  pd.concat([village_town_mean,city_mean, metropolis_mean], axis=1, join_axes=[village_town_mean.index])
result_place.columns = ["vilage_phase","vilage_peak","city_phase","city_peak","metro_phase","metro_peak"]


#%%line plot

plt.style.use("default")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5,2])
plt.plot(grouped_mean['EDA_phase'].tolist())
#plt.plot(result_ethenic['native_phase'].tolist(), label = 'native (0.13)', color = 'seagreen', linewidth=1)
#plt.plot(result_ethenic['non_native_phase'].tolist(), label = 'non-native (0.15)', color = 'red',linewidth=1)
#plt.plot(result_age['age_tt_phase'].tolist(), label = 'age 20-29 (0.12)', color = 'dimgray',linewidth=1)
#plt.plot(result_age['age_ta_phase'].tolist(), label = 'age 30+ (0.18)', color = 'orange',linewidth=1)
#plt.plot(result_place['vilage_phase'].tolist(), label = 'village (0.13)', color = 'olivedrab',linewidth=1)
#plt.plot(result_place['city_phase'].tolist(), label = 'city (0.17)', color = 'orange',linewidth=1)
#plt.plot(result_place['metro_phase'].tolist(), label = 'metropolis (0.11)', color = 'royalblue',linewidth=1)

#ax.set_ylim([0,1])
plt.xticks([])
plt.ylabel('Normalized mean')
#plt.xlabel('Locations')
#plt.title('All variable normalized mean signal analysis')
plt.legend()
fig.savefig('demograpgy_all.pdf')
fig.savefig('demograpgy_all.jpeg')
plt.show()
plt.close(fig)



#%%bar plot data



list1 = result_ethenic["native_peak"].tolist()
list2 = result_ethenic["non_native_peak"].tolist()

list1 = result_age["age_tt_phase"].tolist()
list2 = result_age["age_ta_phase"].tolist()


#%% create bar plot
length = len(list1)

fig, ax = plt.subplots()
index = np.arange(length)
bar_width = 1
opacity = 0.8
 

rects1 = plt.bar(index,list1 , bar_width,
                 alpha=opacity,
                 color='b',
                 label='age 20-29')
 
rects2 = plt.bar(index , list2, bar_width,
                 alpha=opacity,
                 color='g',
                 label='age 30+')
 
#plt.xlabel('Person')
#plt.ylabel('Scores')
#plt.title('Scores by person')
#plt.xticks(index + bar_width, ('A', 'B', 'C', 'D'))
plt.xticks([])
plt.legend()
 
plt.tight_layout()
plt.show()



