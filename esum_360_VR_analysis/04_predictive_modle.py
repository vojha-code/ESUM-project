# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 13:50:52 2018

@author: vojha
"""
%reset -f
%clear
import pandas as pd
import matplotlib.pyplot as plt # plotting and making graphs
import numpy as np
import os
from random import randint
import math
#%% data preparation
dataof = "DE"
if(dataof == "DE"):
    file_isovist = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','XYarusal.csv')
    file_isovist_unseen = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','IsovistsWeimarGrid.csv')
    file_isovist_pred = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','IsovistsWeimarGrid_Pred.csv')
else:
    file_isovist = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed','XYarusal.csv')
    file_isovist_unseen = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed','IsoZurichGrid.csv')
    file_isovist_pred = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed','IsoZurichGrid_Pred.csv')

data_isovist = pd.read_csv(file_isovist)
x = data_isovist[['Area','Perimeter','Compactness','Occlusivity','Min_radial','RayPortion_sky','RayPortion_obstacles', 'Betweenness Car', 'Betweenness Ped']] # Remember that Python does not slice inclusive of the ending index.
inputs = x.as_matrix()
#%%
predictVal = "clicker"
predictor = "tree"


if(predictVal == "peak"):
    #Regression
    y =  data_isovist[['peak']] 
    target = y.as_matrix()
else:
    # Classfication
    y =  data_isovist[['Clicker']] 
    target = y.as_matrix()

#%% Cross validation

#Spliting training data
#from random import randint # randmonnes
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(inputs, target, test_size=0.33, random_state=42)

# Now apply the transformations to the data:
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# Fit only to the training data
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# For peak
if(predictVal == "peak"):
    if(predictor == "MLP" ):
        #constructing MLP
        from sklearn.neural_network import  MLPRegressor
        mplReg = MLPRegressor(solver='sgd', alpha=1e-5, hidden_layer_sizes=(10), random_state=1)
        mplReg.fit(X_train, y_train)    #MLP TRAINING
        y_pred = mplReg.predict(X_test)    #prediction
    elif(predictor == "KNN" ):
        #constructing KNN
        from sklearn.neighbors import KNeighborsRegressor
        neigReg = KNeighborsRegressor(n_neighbors=3)
        neigReg.fit(X_train, y_train)    #MLP TRAINING
        y_pred = neigReg.predict(X_test)    #prediction
    else:
        from sklearn.tree import DecisionTreeRegressor
        treeReg = DecisionTreeRegressor(random_state=0)
        treeReg.fit(X_train, y_train)    #MLP TRAINING
        y_pred = treeReg.predict(X_test)    #prediction
    
    from sklearn.metrics import mean_squared_error
    print("Mean Squared Error:",mean_squared_error(y_test, y_pred))
    from sklearn.metrics import r2_score
    #print("R2 (Squared Correaltion-coeff):",r2_score(y_test, y_pred))
    from scipy.stats.stats import pearsonr
    a = np.squeeze(np.array(y_test))
    b = np.squeeze(np.array(y_pred))
    #print(pearsonr(a,b))
    print("R2 (Squared Correaltion-coeff):",pow(np.corrcoef(a,b),2))
else:
    if(predictor == "MLP" ):
        #constructing MLP
        from sklearn.neural_network import MLPClassifier
        mlpClass = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5),random_state=1)
        mlpClass.fit(X_train, y_train)    # TRAINING
        y_pred = mlpClass.predict(X_test)  #prediction
    elif(predictor == "KNN" ):
        #constructing KNN
        from sklearn.neighbors import KNeighborsClassifier
        neigClass = KNeighborsClassifier(n_neighbors=3)
        neigClass.fit(X_train, y_train)    # TRAINING
        y_pred = neigClass.predict(X_test) #prediction
    else:
        from sklearn.tree import DecisionTreeClassifier
        treeClass = DecisionTreeClassifier(random_state=0)
        treeClass.fit(X_train, y_train)    #MLP TRAINING
        y_pred = treeClass.predict(X_test)    #prediction
        
    from sklearn.metrics import accuracy_score
    print('\n Accuracy:',accuracy_score(y_test, y_pred)*100,"%\n")
#%%prediction
data_isovist_us = pd.read_csv(file_isovist_unseen)
column_to_fetch = ['2dIso 360 Area','2dIso 360 Perimeter','2dIso 360 Compactness','2dIso 360 Occlusivity','2dIso 360 Min radial','3dIso 360_110 RayPortion_sky','3dIso 360_110 RayPortion_obstacles','Betweenness Rn angular', 'Betweenness R600 angular']#'3dIso 360_110 Volume'
x = data_isovist_us[column_to_fetch]
inputs_unknon = x.as_matrix()

# data preprocessing
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# Fit only to the training data
scaler.fit(inputs)
X_train = scaler.transform(inputs)
# Fit only to the test unseen data
scaler.fit(inputs_unknon)
X_test = scaler.transform(inputs_unknon)


# For peak
if(predictVal == "peak"):
    if(predictor == "MLP" ):
        from sklearn.neural_network import  MLPRegressor
        mlpreg = MLPRegressor(solver='sgd', alpha=1e-5, hidden_layer_sizes=(10), random_state=1)
        mlpreg.fit(X_train, target)
        predict = mlpreg.predict(X_train)# known prediction
        unkno_pred = mlpreg.predict(X_test)# Unknown prediction
    elif(predictor == "KNN" ):
        #KNN
        from sklearn.neighbors import KNeighborsRegressor
        neigh = KNeighborsRegressor(n_neighbors=3)
        neigh = KNeighborsRegressor(n_neighbors=3)
        neigh.fit(X_train, target)
        predict = neigh.predict(X_train)# known prediction
        unkno_pred = neigh.predict(X_test)# unknown prediction
    else:# regression tree    
        from sklearn.tree import DecisionTreeRegressor
        tree = DecisionTreeRegressor(random_state=0)
        tree.fit(X_train, target)
        predict = tree.predict(X_train)# known prediction
        unkno_pred = tree.predict(X_test)# Unknown prediction
    
    from sklearn.metrics import mean_squared_error
    print("Mean Squared Error:",mean_squared_error(target, predict))
    from sklearn.metrics import r2_score
    print("R2 (Squared Correaltion-coeff):",r2_score(target, predict))        
    
else:# for clicker
    if(predictor == "MLP" ):
        #constructing MLP
        from sklearn.neural_network import MLPClassifier
        mlpClass = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5),random_state=1)
        mlpClass.fit(X_train, target)    # TRAINING
        predict = mlpClass.predict(X_train)# known prediction
        unkno_pred = mlpClass.predict(X_test)# unknown prediction
    elif(predictor == "KNN" ):
        #constructing KNN
        from sklearn.neighbors import KNeighborsClassifier
        neigClass = KNeighborsClassifier(n_neighbors=3)
        neigClass.fit(X_train, target)    # TRAINING
        predict = neigClass.predict(X_train)# known prediction
        unkno_pred = neigClass.predict(X_test)# unknown prediction
    else:
        from sklearn.tree import DecisionTreeClassifier
        treeClass = DecisionTreeClassifier(random_state=0)
        treeClass.fit(X_train, target)    #MLP TRAINING
        predict = treeClass.predict(X_train)# known prediction
        unkno_pred = treeClass.predict(X_test)# unknown prediction

    from sklearn.metrics import accuracy_score
    print('\n Accuracy:',accuracy_score(target, predict)*100,"%\n")
    


#%%
data_isovist_pred = pd.read_csv(file_isovist_pred)
coulmName = predictVal + '_' + predictor
data_isovist_pred[coulmName] = unkno_pred
data_isovist_pred.to_csv(file_isovist_pred, index=False)