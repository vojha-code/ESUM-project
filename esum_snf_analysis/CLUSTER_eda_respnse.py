# -*- coding: utf-8 -*-
"""
Created on Fri May 12 09:45:53 2017

@author: vojha
"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from random import randint

import matplotlib.patches as mpatches # for patching legend on plots
#%%
#preparing data
filepath = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\ESUM_qunatified_data"
#filename = "5s_smooth_withsensot_loss.csv"
filename = "merged_data_2Donly_for_smooth.csv"

eda_data = pd.read_csv(os.path.join(filepath,filename))
del eda_data["ID"]
del eda_data["EDA_label"]
eda_data.columns = ["P","X","Y","Area","Perimeter","Oculocity","Compactness","EDA_peaks","EDA_phase","multilavel"]

#x = eda_data[['Sound', 'Dust','TempEN','RH', 'Light']]
x = eda_data[['Area', 'Perimeter','Oculocity','Compactness']]
#participants = eda_data[['participant']]
inputs = x.as_matrix()
y = eda_data[['multilavel']]
target = y.as_matrix()


# K means clusterining
K = 3
#initialize and carry out clustering
km = KMeans(n_clusters = K)
km.fit(inputs)

#find center of clusters
centroids = km.cluster_centers_
labels = km.labels_



print(centroids)
print(labels)

#style assingment to plot
#style.use("ggplot")

from matplotlib.mlab import PCA
results = PCA(data)



fig = plt.figure(figsize=(9,7))
colors = ["g.","b.","r."]
for i in range(len(inputs)):
    #print("coordinate:",inputs[i], "label:", labels[i])
    #plt.plot(inputs[i][0], inputs[i][3], colors[labels[i]], markersize = 5)
    plt.plot(inputs[i][0], inputs[i][3], colors[target[i][0]], markersize = 10)
    
green_dot = mpatches.Patch(color='green', label='Normal')
blue_dot = mpatches.Patch(color='blue', label='Low arousals')
red_dot = mpatches.Patch(color='red', label='High arousals')

plt.legend(handles=[green_dot,blue_dot,red_dot,])
#plt.title("Clustering of envirnment variables")
#plt.title("☺ of 2D Isovist")
plt.xlabel("Area")
plt.ylabel("Compactness")
#plt.ylabel("Relative humidity")
#plt.ylabel("Light (Illuminance)")
plt.show()
#fig.savefig('temp_vs_sound_eda_peaks.pdf')
#fig.savefig('area_vs_compactness_eda_peaks.pdf')
plt.close(fig)

df_x_y_l = pd.DataFrame({'A' : []})  
df_x_y_l["X"] = eda_data["X"]
df_x_y_l["Y"] = eda_data["Y"]
df_x_y_l["L"] = labels.tolist()
del df_x_y_l["A"]
df_x_y_l.to_csv(os.path.join("isoVist_x_y_l.csv"))



silhouette_avg = silhouette_score(inputs, labels)
print("For n_clusters =", K, "The average silhouette_score is :", silhouette_avg)

from scipy.stats.stats import pearsonr
pearsonr(target, labels)
np.corrcoef(target.tolist, labels)[0, 1]



#DBSCAN clusterining
epsilon = 0.9
min_neighbour = 10

data = StandardScaler().fit_transform(inputs) 

dbsc = DBSCAN(eps = epsilon, min_samples = min_neighbour).fit(data)

labels = dbsc.labels_
core_samples = np.zeros_like(labels, dtype = bool)
core_samples[dbsc.core_sample_indices_] = True

new_label = labels + 1
colors = ["g.","r.","c.","y."]
for i in range(len(inputs)):
    print("coordinate:",inputs[i], "label:", new_label[i])
    plt.plot(inputs[i][0], inputs[i][1], colors[new_label[i]], markersize = 10)
    
plt.title("DBSCAN of iris data")
plt.xlabel('Sepal Length')
plt.ylabel('Sepal width')

silhouette_avg = silhouette_score(inputs, labels)
print("The average silhouette_score is :", silhouette_avg)