# Required packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Change directory
import os
#%% 
os.chdir("C://Users//vojha//Dropbox//0_Programming//ESUM_Experiments//ESUM_qunatified_data")
# Read in the data: Participants Biofeedback
#xl = pd.ExcelFile("Participants_Bio_feedback_data_dynamics.xlsx")
#xl.sheet_names for calling the name of the sheet. "Sheet1" is it in this excel sheet.
#bio = xl.parse("Sheet1")
#%%STEP 1
#bio = pd.read_csv("5s_smooth_withsensot_loss.csv")
bio = pd.read_csv("complied_data_filtered.csv")

del bio["Unnamed: 0"]#deleting unneccasry column
#[6,7,8,9,10,11,13,14,16,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]:
# Create dict variable d with all participants results stored in. By this, every participant's results is an own data frame
d = {} #making a dictionary 
for i in [6,7,8,9,10,11,13,16,23,24,25,26,27,28,29,30,31,32,34,35]:
    d[i] = bio[bio["participant"] == i]


#%%STEP: Spliting file
#Step creating DataFrame again
df = pd.DataFrame({'A' : []})     
for i in [6,7,8,9,10,11,13,16,18,23,24,25,26,27,28,29,30,32,34,35]:
    df1 = pd.DataFrame({'b':d[i][d[i].columns[6]].tolist()})
    df2 = pd.DataFrame({'b':d[i][d[i].columns[10]].tolist()})
    df = pd.concat([df,df1,df2], ignore_index=True, axis=1)

del df[0]
df.plot(figsize=(20, 20))
#%% Auxiliary STEP
#spliting participants and saving files
for i in [6,7,8,9,10,11,13,16,23,24,25,26,27,28,29,30,31,32,34,35]:
    df = d[i]
    file_name = "eda_gps_"+str(i)+".csv"
    df.to_csv(file_name)

#%% STEP: noramailazation (Optional at this stage)
#normalizing variables participants   
for i in [6,7,8,9,10,11,13,16,23,24,25,26,27,28,29,30,32,34,35]:
    for j in range(3,14):
        d[i][d[i].columns[j]] = d[i][d[i].columns[j]]/pd.DataFrame.max(d[i][d[i].columns[j]])

#%%STEP
#creating data freames variable wise
df_x = pd.DataFrame({'A' : []}) 
df_y = pd.DataFrame({'A' : []})  
df_sound = pd.DataFrame({'A' : []}) 
df_dust = pd.DataFrame({'A' : []})  
df_temp = pd.DataFrame({'A' : []}) 
df_rh = pd.DataFrame({'A' : []})   
df_light = pd.DataFrame({'A' : []}) 
df_area = pd.DataFrame({'A' : []}) 
df_peri = pd.DataFrame({'A' : []}) 
df_ocl = pd.DataFrame({'A' : []}) 
df_comp = pd.DataFrame({'A' : []}) 
df_peak = pd.DataFrame({'A' : []}) 
df_phase = pd.DataFrame({'A' : []})      
for i in [6,7,8,9,10,11,13,16,23,24,25,26,27,28,29,30,32,34,35]:
    df01 = pd.DataFrame({'b':d[i][d[i].columns[1]].tolist()})
    df_x = pd.concat([df_x,df01], ignore_index=True, axis=1)
    
    df02 = pd.DataFrame({'b':d[i][d[i].columns[2]].tolist()})
    df_y = pd.concat([df_x,df02], ignore_index=True, axis=1)
    
    
    df1 = pd.DataFrame({'b':d[i][d[i].columns[3]].tolist()})
    df_sound = pd.concat([df_sound,df1], ignore_index=True, axis=1)
    
    df2 = pd.DataFrame({'b':d[i][d[i].columns[4]].tolist()})
    df_dust = pd.concat([df_dust,df2], ignore_index=True, axis=1)
    
    df3 = pd.DataFrame({'b':d[i][d[i].columns[5]].tolist()})
    df_temp = pd.concat([df_temp,df3], ignore_index=True, axis=1)
    
    df4 = pd.DataFrame({'b':d[i][d[i].columns[6]].tolist()})
    df_rh = pd.concat([df_rh,df4], ignore_index=True, axis=1)
    
    df5 = pd.DataFrame({'b':d[i][d[i].columns[7]].tolist()})
    df_light = pd.concat([df_light,df5], ignore_index=True, axis=1)
    
    df8 = pd.DataFrame({'b':d[i][d[i].columns[8]].tolist()})
    df_area = pd.concat([df_area,df8], ignore_index=True, axis=1)
    
    df9 = pd.DataFrame({'b':d[i][d[i].columns[9]].tolist()})
    df_peri = pd.concat([df_peri,df9], ignore_index=True, axis=1)
    
    df10 = pd.DataFrame({'b':d[i][d[i].columns[10]].tolist()})
    df_ocl = pd.concat([df_ocl,df10], ignore_index=True, axis=1)
    
    df11 = pd.DataFrame({'b':d[i][d[i].columns[11]].tolist()})
    df_comp = pd.concat([df_comp,df11], ignore_index=True, axis=1)
    
    df6 = pd.DataFrame({'b':d[i][d[i].columns[12]].tolist()})
    df_peak = pd.concat([df_peak,df6], ignore_index=True, axis=1)
    
    df7 = pd.DataFrame({'b':d[i][d[i].columns[13]].tolist()})
    df_phase = pd.concat([df_phase,df7], ignore_index=True, axis=1)

del df_x[0]
del df_y[0]
del df_sound[0]
del df_dust[0]
del df_temp[0]
del df_rh[0]
del df_light[0]
del df_area[0]
del df_peri[0]
del df_ocl[0]
del df_comp[0]
del df_peak[0]
del df_phase[0]


#%%STEP: Computing mean
df_x['mean'] = df_x.mean(axis=1)
df_y['mean'] = df_y.mean(axis=1)

df_sound['mean'] = df_sound.mean(axis=1)
df_dust['mean'] = df_dust.mean(axis=1)
df_temp['mean'] = df_temp.mean(axis=1)
df_rh['mean'] = df_rh.mean(axis=1)
df_light['mean'] = df_light.mean(axis=1)

df_area['mean'] = df_area.mean(axis=1)
df_peri['mean'] = df_peri.mean(axis=1)
df_ocl['mean'] = df_ocl.mean(axis=1)
df_comp['mean'] = df_comp.mean(axis=1)

df_peak['mean'] = df_peak.mean(axis=1)
df_phase['mean'] = df_phase.mean(axis=1)


X = np.array(df_x['mean'].tolist())
Y = np.array(df_y['mean'].tolist())
sound = np.array(df_sound['mean'].tolist())
dust = np.array(df_dust['mean'].tolist())
temp = np.array(df_temp['mean'].tolist())
rh = np.array(df_rh['mean'].tolist())
light = np.array(df_light['mean'].tolist())
area = np.array(df_area['mean'].tolist())
peri = np.array(df_peri['mean'].tolist())
ocl = np.array(df_ocl['mean'].tolist())
comp = np.array(df_comp['mean'].tolist())
peaks = np.array(df_peak['mean'].tolist())
phase = np.array(df_phase['mean'].tolist())

df_mean_of_all = pd.DataFrame({'A' : []})   
df_mean_of_all = pd.concat([df_mean_of_all,
                            df_x['mean'],
                            df_y['mean'],
                            df_sound['mean'],
                            df_dust['mean'],
                            df_temp['mean'],
                            df_rh['mean'],
                            df_light['mean'],
                            df_area['mean'],
                            df_peri['mean'],
                            df_ocl['mean'],
                            df_comp['mean'],
                            df_peak['mean'],
                            df_phase['mean']],  
                            ignore_index=True, axis=1)
del df_mean_of_all[0]
combined_norm_mean = os.path.join("combnied_norm_mean_data.csv")
df_mean_of_all.to_csv(combined_norm_mean)

#%% STEP: heat map of correlation matrix
import seaborn as sns
df_mean_only_variables = df_mean_of_all.copy(deep=True)

del df_mean_only_variables[1]
del df_mean_only_variables[2]

old_names = df_mean_only_variables.columns
new_names = ['Sound', 'Dust', 'Temperature', 'Humidity', 'Illuminance', 'Area', 'Perimeter', 'Occlusivity', 'Compactness', 'nSCR', 'SCR']
df_mean_only_variables.rename(columns=dict(zip(old_names, new_names)), inplace=True)
#del df_mean_only_variables["Perimeter"]
#del df_mean_only_variables["Occlusivity"]
#correlation matrix
fig, ax = plt.subplots(figsize=(8.5, 7.5))
corr = df_mean_only_variables.corr()
mask = np.zeros_like(corr, dtype=np.bool)
#mask[np.triu_indices_from(mask)] = True
cmp = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmp,square=True, ax=ax)
#sns.heatmap(corr, mask=mask, cmap=cmp, vmax=.3,square=True,linewidths=.5, cbar_kws={"shrink": .9}, ax=ax)
#fig.savefig('corre_matrix.pdf')
#fig.savefig('corre_matrix.jpeg')
#corr.to_csv("correlation_matrix.csv")

#%%Correaltion matrix another version
import numpy as np; np.random.seed(1)
import pandas as pd
import seaborn.apionly as sns
import matplotlib.pyplot as plt

# Generate a random dataset
#cols = [s*4 for s in list("ABCD")]
#df = pd.DataFrame(data=np.random.rayleigh(scale=5, size=(100, 4)), columns=cols)

# Compute the correlation matrix
#corr = df.corr()
#print(corr)
df_mean_only_variables = df_mean_of_all.copy(deep=True)
del df_mean_only_variables[1]
del df_mean_only_variables[2]

old_names = df_mean_only_variables.columns
#new_names = ['S', 'D', 'T', 'H', 'L', 'A', 'P', 'O', 'C', 'N', 'R']
new_names = ['Sound', 'Dust', 'Temperature', 'Humidity', 'Illuminance', 'Area', 'Perimeter', 'Occlusivity', 'Compactness', 'nSCR', 'SCR']
df_mean_only_variables.rename(columns=dict(zip(old_names, new_names)), inplace=True)
corr = df_mean_only_variables.corr()
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(8.5, 7.5))

# Draw the heatmap with the mask and correct aspect ratio
vmax = np.abs(corr.values[~mask]).max()
sns.heatmap(corr, mask=mask, cmap=plt.cm.PuOr, vmin=-vmax, vmax=vmax,
            square=True, linecolor="lightgray", linewidths=1, ax=ax)
for i in range(len(corr)):
    #ax.text(i+0.5,len(corr)-(i+0.5), corr.columns[i], 
            #ha="center", va="center", rotation=45)
    for j in range(i+1, len(corr)):
        s = "{:.3f}".format(corr.values[i,j])
        ax.text(j+0.5,(i+0.5),s, 
            ha="center", va="center")
#ax.axis("off")
plt.show()
fig.savefig('corre_matrix.pdf')
fig.savefig('corre_matrix.jpeg')
#corr.to_csv("correlation_matrix.csv")

#%%STEP: Truncating unncessary rows
#droping first values
df_sound = df_sound.drop(df_sound.index[[0]])
df_dust = df_dust.drop(df_dust.index[[0]])
df_temp = df_temp.drop(df_temp.index[[0]])
df_rh = df_rh.drop(df_rh.index[[0]])
df_light = df_light.drop(df_light.index[[0]])
df_area = df_area.drop(df_area.index[[0]])
df_peri = df_peri.drop(df_peri.index[[0]])
df_ocl = df_ocl.drop(df_ocl.index[[0]])
df_comp = df_comp.drop(df_comp.index[[0]])
df_peak = df_peak.drop(df_peak.index[[0]])
df_phase = df_phase.drop(df_phase.index[[0]])


#droping last rows values
df_sound = df_sound.drop(df_sound.index[[len(df_sound)-1]])
df_dust = df_dust.drop(df_dust.index[[len(df_dust)-1]])
df_temp = df_temp.drop(df_temp.index[[len(df_temp)-1]])
df_rh = df_rh.drop(df_rh.index[[len(df_rh)-1]])
df_light = df_light.drop(df_light.index[[len(df_light)-1]])
df_area = df_area.drop(df_area.index[[len(df_area)-1]])
df_peri = df_peri.drop(df_peri.index[[len(df_peri)-1]])
df_ocl = df_ocl.drop(df_ocl.index[[len(df_ocl)-1]])
df_comp = df_comp.drop(df_comp.index[[len(df_comp)-1]])
df_peak = df_peak.drop(df_peak.index[[len(df_peak)-1]])
df_phase = df_phase.drop(df_phase.index[[len(df_phase)-1]])

#%%STEP: After mean normalization
df_sound =(df_sound-df_sound.min())/(df_sound.max()-df_sound.min())
df_dust = (df_dust-df_dust.min())/(df_dust.max()-df_dust.min())
df_temp = (df_temp-df_temp.min())/(df_temp.max()-df_temp.min())
df_rh = (df_rh-df_rh.min())/(df_rh.max()-df_rh.min())
df_light = (df_light-df_light.min())/(df_light.max()-df_light.min())
df_area = (df_area-df_area.min())/(df_area.max()-df_area.min())
df_peri = (df_peri-df_peri.min())/(df_peri.max()-df_peri.min())
df_ocl = (df_ocl-df_ocl.min())/(df_ocl.max()-df_ocl.min())
df_comp = (df_comp-df_comp.min())/(df_comp.max()-df_comp.min())
df_peak = (df_peak-df_peak.min())/(df_peak.max()-df_peak.min())
df_phase = (df_phase-df_phase.min())/(df_phase.max()-df_phase.min())
#%% other env variable plots


#%%STEP: ploting variables
plt.style.use("default")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5,2])
#plt.plot(df_sound['mean'].tolist(), label = 'Sound', color = 'seagreen', linewidth=1.5)
#plt.plot(df_dust['mean'].tolist(), label = 'Dust', color = 'dimgray',linewidth=1.5)
#plt.plot(df_temp['mean'].tolist(), label = 'Temperature', color = 'red',linewidth=1.5)
#plt.plot(df_rh['mean'].tolist(), label = 'Humidity', color = 'deepskyblue',linewidth=1.5)
#plt.plot(df_light['mean'].tolist(), label = 'Illuminance', color = 'orange',linewidth=1.5)
#plt.plot(df_area['mean'].tolist(), label = 'Area',color = "olivedrab",linewidth=1.5)
#plt.plot(df_peri['mean'].tolist(), label = 'Perimeter')
#plt.plot(df_ocl['mean'].tolist(), label = 'Occlusivity')
#plt.plot(df_comp['mean'].tolist(), label = 'Compactness',color = "chocolate",linewidth=1.5)
plt.plot(df_peak['mean'].tolist(), label = 'nSCR', color = "darkblue",linewidth=1.5)
plt.plot(df_phase['mean'].tolist(), label = 'SCR', color = "royalblue",linewidth=1.5)
plt.ylabel('Normalized mean value')
plt.xlabel('Quantified samples')
#plt.title('All variable normalized mean signal analysis')
plt.legend()
fig.savefig('norm_mean_peak_plot.pdf')
fig.savefig('norm_mean_peak_plot.jpeg')
#fig.savefig('isovist_variable_norm_mean_plot_peak.pdf')
plt.show()
plt.close(fig)

#%% #%%Temprary practice codes
#Creating the differentials of all variables and append them to the data frames
for i in [6,7,8,9,10,11,13,16,18,23,24,25,26,27,28,29,30,32,34,35]:
    d[i] = d[i].join(pd.DataFrame(np.append(0,np.diff(d[i]["Sound"],n=1)),index=d[i].index))
    d[i].columns.values[11] = "dSound"
    d[i] = d[i].join(pd.DataFrame(np.append(0,np.diff(d[i]["Dust"],n=1)),index=d[i].index))
    d[i].columns.values[12] = "dDust"
    d[i] = d[i].join(pd.DataFrame(np.append(0,np.diff(d[i]["TempEN"],n=1)),index=d[i].index))    
    d[i].columns.values[13] = "dTempEN"
    d[i] = d[i].join(pd.DataFrame(np.append(0,np.diff(d[i]["RH"],n=1)),index=d[i].index))
    d[i].columns.values[14] = "dRH"
    d[i] = d[i].join(pd.DataFrame(np.append(0,np.diff(d[i]["Light"],n=1)),index=d[i].index))
    d[i].columns.values[15] = "dLight"
    d[i] = d[i].join(pd.DataFrame(np.append(0,np.diff(d[i]["#WiFi"],n=1)),index=d[i].index))
    d[i].columns.values[16] = "d#WiFi"
    d[i] = d[i].join(pd.DataFrame(np.append(0,np.diff(d[i]["HR"],n=1)),index=d[i].index))
    d[i].columns.values[17] = "dHR"
    d[i] = d[i].join(pd.DataFrame(np.append(0,np.diff(d[i]["BVP"],n=1)),index=d[i].index))
    d[i].columns.values[18] = "dBVP"
    d[i] = d[i].join(pd.DataFrame(np.append(0,np.diff(d[i]["EDA"],n=1)),index=d[i].index))
    d[i].columns.values[19] = "dEDA"
    d[i] = d[i].join(pd.DataFrame(np.append(0,np.diff(d[i]["TempBF"],n=1)),index=d[i].index))
    d[i].columns.values[20] = "dTempBF"


#For representing the data visually, it is helpful to normalize the data by dividing them by their maximum value of each participant.
# The maximum of each participant's results

        
## Normalizing data frame directly
df = pd.DataFrame({'A' : []})
df["TempEN"] = bio["TempEN"]
df["EDA_phase"] = bio["EDA_phase"]
del df["A"]

from sklearn import preprocessing

x = df.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df = pd.DataFrame(x_scaled)
df.columns = ['x','y']
df["participants"]=bio["participant"]



x = np.arange(500)
i = 6
plt.plot(x,d[i][d[i].columns[6]], color = 'b')
d[7][d[7].columns[10]]
for i in [6,7,8,9,10,11,13,16,18,23,24,25,26,27,28,29,30,32,34,35]:
    i = 6
    fig = plt.figure(1)
    plt.plot(d[i][d[i].columns[6]], color = 'b')
    plt.plot(d[i][d[i].columns[10]], color = 'r')
    fig.set_size_inches(40, 10)
    #plt.ylim([-0.2,0.2])

plt.legend([str(d[i].columns.values[1]),str(d[i].columns.values[2]),str(d[i].columns.values[3]),str(d[i].columns.values[4]),str(d[i].columns.values[5]),str(d[i].columns.values[6]),str(d[i].columns.values[7]),str(d[i].columns.values[8]),str(d[i].columns.values[9]), str(d[i].columns.values[10])], loc ='upper right')
plt.xlabel('Trackpoint')
    #plt.show()  


for i in [5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]:
    for j,color in enumerate(['b','g','r','m','y','k','c','goldenrod','deepskyblue','lawngreen'], start=1):
        fig = plt.figure(1)
        plt.plot(d[i][d[i].columns[j]], color = color)
        fig.set_size_inches(40, 10)
        #plt.ylim([-0.2,0.2])
        plt.legend([str(d[i].columns.values[1]),str(d[i].columns.values[2]),str(d[i].columns.values[3]),str(d[i].columns.values[4]),str(d[i].columns.values[5]),str(d[i].columns.values[6]),str(d[i].columns.values[7]),str(d[i].columns.values[8]),str(d[i].columns.values[9]), str(d[i].columns.values[10])], loc ='upper right')
    plt.xlabel('Trackpoint')
    #plt.show()

    fig.savefig("Plots/Absolute_"+str(i), dpi=300)
    plt.clf()


for i in [5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]:
    for j,color in enumerate(['b','g','r','m','y','k','c','goldenrod','deepskyblue','lawngreen'], start=11):
        fig = plt.figure(1)
        plt.plot(d[i][d[i].columns[j]], color = color)
        fig.set_size_inches(100, 10)
        plt.ylim([-0.2,0.2])
        #set_color_cycle([(1,1,1),(1,1,0)])
        plt.legend([str(d[i].columns.values[11]),str(d[i].columns.values[12]),str(d[i].columns.values[13]),str(d[i].columns.values[14]),str(d[i].columns.values[15]),str(d[i].columns.values[16]),str(d[i].columns.values[17]),str(d[i].columns.values[18]),str(d[i].columns.values[19]),str(d[i].columns.values[20])], loc ='upper right')
    plt.xlabel('Trackpoint')
    #plt.show()

    fig.savefig("Plots/Differential_"+str(i), dpi=300)
    plt.clf()

#%%Temprary practice codes

df_temp = pd.concat([df_temp,df1], ignore_index=True, axis=1)
#creating maps
plt.style.use('ggplot')
plt.figure(); 
df_temp.plot(figsize=(20, 20));
df_phase.plot(figsize=(20, 20));

df.plot(figsize=(20, 20))





plt.figure()
plt.plot(sound, label='a')
plt.plot(dust)
plt.plot(temp)
plt.plot(rh)
plt.plot(light)
plt.plot(phase)
plt.plot(peaks)
plt.plot(bio['X'].tolist(),bio['Y'].tolist())


