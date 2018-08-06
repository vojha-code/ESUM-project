
%reset -f
%clear

import pysal

import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.patches as mpatches # for patching legend on plots
import numpy as np
import os
from random import randint
import math
from scipy.spatial import distance

#N = 10
#Z = np.random.random((N,N))
## Create the matrix of weigthts
#w = pysal.lat2W(Z.shape[0], Z.shape[1])
#
## Crate the pysal Moran object
#mi = pysal.Moran(Z, w)
#
## Verify Moran's I results
#print(mi.I)
#print(mi.p_norm)


#%%

dataof = "ZH"
if(dataof == "DE"):
    file_360 = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','XYarusal.csv')
    file_block = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_Block\processed','XYarusal.csv')    
    file_com = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_Block\processed','XYComaprision.csv')    
else:
    file_real = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_real','XYarousal_real.csv')
    file_360 = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed','XYarusal.csv')
    file_block = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_Block\processed','XYarusal.csv')
    file_com = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_Block\processed','XYComaprision.csv')    
    
    data_XY_real = pd.read_csv(file_real)

data_XY_360 = pd.read_csv(file_360)
data_XY_block = pd.read_csv(file_block)

x_360 = data_XY_360[['Latitude','Longitude','peak','Clicker']]
x_block = data_XY_block[['Latitude','Longitude','peak','Clicker']]


if(dataof != "DE"):
    x_real = data_XY_real[['X','Y','EDA_peaks']]
    #x_real = x_real[x_real['EDA_peaks'] <= 4.2]
    CHx = np.asarray(x_real['Y'].tolist()) #This should go to A input
    CHy = np.asarray(x_real['X'].tolist()) #This should go B input
    
    WGS_x,WGS_y = CH1903toWGS1984(CHx, CHy)
    
    x_real["Latitude"] = WGS_x.tolist()
    x_real["Longitude"] = WGS_y.tolist()

#%%

main_xy = x_block
retr_xy = x_360
#retr_xy = x_real

#%% Calculating average radious
radius = []
avgRadius = 0
for i in range(len(main_xy)-1):
    x1 = main_xy['Latitude'][i]
    y1 = main_xy['Longitude'][i]
    
    x2 = main_xy['Latitude'][i+1]
    y2 = main_xy['Longitude'][i+1]
    
    #a = (x1,y1)
    #b = (x2,y2)
    #distance.euclidean(a, b)
    d = np.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))
    #print("point ",i, ":", d)
    radius.append(float(d*0.6))# taking 70 % of the distance as a redious
    avgRadius = avgRadius + float(d/2)

avgRadius = float(avgRadius/len(radius)) 
radius.append(radius[len(radius)-1])
print("avgRadius:", avgRadius)
#%% Brlient method but do not work in this case perhaps did not go in more detail
lineX = []
lineY1 = []
lineY2 = []
    
fig, ax = plt.subplots(figsize=(12, 8))
#for i in range(len(main_xy)):
for i in range(6,7):
    x1 = main_xy['Latitude'][i]
    y1 = main_xy['Longitude'][i]
    
    x2 = main_xy['Latitude'][i+1]
    y2 = main_xy['Longitude'][i+1]
    
    #midpoint calculation
    xc = float((x1+x2)/2)
    yc = float((y1+y2)/2)
    print("point ",i, ":",x1, y1, x2, y2, xc, yc)  
    plt.plot([x1,x2], [y1,y2], 'r--', linewidth=0.5)
    plt.plot(x1,y1, color = "green", marker = "o", alpha = 0.5, markersize = 10)
    plt.plot(x2,y2, color = "green", marker = "o", alpha = 0.8, markersize = 10)
    plt.plot(xc,yc, color = "red", marker = "o", alpha = 0.5, markersize = 10)
    
    dist_from_midpoint = np.sqrt(math.pow((x2-xc),2) + math.pow((y2-yc),2)) # Base of a traingle 
    Base = dist_from_midpoint
    #given_perpenduclar_line_length
    Perpendicular = 0.005 # perpenducular of a traing
    Hypotenuse = distance.euclidean(Base, Perpendicular)    
    Slope = float(float(Hypotenuse) / float(Base))
    
    yc1 = Slope*(x2-xc) + yc
    yc2 = -Slope*(x2-xc) + yc
    
    #print("point ",i, ":",xc, yc1, yc2)
    lineX.append(xc)
    lineY1.append(yc1)
    lineY2.append(yc2)

    plt.plot(xc,yc1, color = "blue", marker = "o", alpha = 0.3, markersize = 10)
    plt.plot(xc,yc2, color = "blue", marker = "o", alpha = 0.8, markersize = 10)
    plt.plot([xc,xc], [yc1,yc2], 'g--', linewidth=0.7)
    
    
    #check if xc, yc1 is on left or right
    d = (xc-x1)*(y2-y1)-(yc1-y1)*(x2-x1)
    if (d < 0):
        print("Left side", d)
    else:
        print("Right side", d)

#%%
avgPeak = []
avgClicker = []
usedIndex = []
count_true = 0
count_false = 0
for i in range(len(main_xy)):
    xc = main_xy['Latitude'][i]
    yc = main_xy['Longitude'][i]

    count = 0 # indeix for other array    
    sumPeak = 0
    sumClicker = 0
    j = 0
    while(True):
        if((j not in usedIndex)):
            if(j < len(retr_xy)):
                xj = retr_xy['Latitude'][j]
                yj = retr_xy['Longitude'][j]
        
                dist = np.sqrt(math.pow((xj-xc),2) + math.pow((yj-yc),2))
                if(dist < radius[i]*1.7):
                    print("True",i,j)
                    sumPeak = sumPeak +  retr_xy['peak'][j]
                    sumClicker = sumClicker +  retr_xy['Clicker'][j]
                    #sumPeak = sumPeak +  retr_xy['EDA_peaks'][j]# for real zh data
                    count = count + 1
                    usedIndex.append(j)
                else:
                    print("False",i,j, count)
                    break
            else:
                print("No more data",i,j, count)
                break
        j = j + 1
        #end while
    if(count > 0):
        avgPeak.append(float(sumPeak/float(count)))
        avgClicker.append(float(sumClicker/float(count)))  
    else:
        avgPeak.append(np.nan)
        avgClicker.append(np.nan)          

print("check",len(avgPeak)," = ",len(main_xy))




#%%
main_xy["peak_360"] = avgPeak
main_xy["clicker_360"] = avgClicker
main_xy.to_csv(file_com)

#%%
def CHtoWGSlat(x,y):
    """
    Convert CH1903 system to WGS1984 system (latitude)
 
    :param x: northing
    :param y: easting
    :return: latitude in WGS1984 system
 
    """
    x_aux = (x - 200000) / 1000000
    y_aux = (y - 600000) / 1000000
 
    lat = (16.9023892 + (3.238272 * x_aux)) \
          - (0.270978 * pow(y_aux, 2)) \
          - (0.002528 * pow(x_aux, 2)) \
          - (0.0447 * pow(y_aux, 2) * x_aux) \
          - (0.0140 * pow(x_aux, 3))
 
    lat = (lat * 100) / 36
 
    return lat
 
def CHtoWGSlng(x,y):
    """
    Convert CH1903 system to WGS1984 system (longitude)
 
    :param x: northing
    :param y: easting
    :return: longitude in WGS1984 system
 
    """
    x_aux = (x - 200000) / 1000000
    y_aux = (y - 600000) / 1000000
 
    lng = (2.6779094 + (4.728982 * y_aux) + (0.791484 * y_aux * x_aux) +
           (0.1306 * y_aux * pow(x_aux, 2))) - (0.0436 * pow(y_aux, 3))
 
    lng = (lng * 100) / 36
 
    return lng
 
def CH1903toWGS1984(x, y):
  """Converts coordinates from CH1903_LV03 to WGS1984 adopting the code taken from
     method from http://www.swisstopo.admin.ch/internet/swisstopo/de/home/products/software/products/skripts.html
 
     :param x: x coordinates in degrees in CH1903 (northing)
     :param y: y coordinates in degrees in CH1903 (easting)
     :return: a pair containing the latitude and longitude of the given coordinates, respectively"""
 
  lat = CHtoWGSlat(x, y)
  lng = CHtoWGSlng(x, y)
 
  return lat, lng
