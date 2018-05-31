
%reset -f
%clear

import pysal

import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint
import math


N = 10
Z = np.random.random((N,N))
# Create the matrix of weigthts
w = pysal.lat2W(Z.shape[0], Z.shape[1])

# Crate the pysal Moran object
mi = pysal.Moran(Z, w)

# Verify Moran's I results
print(mi.I)
print(mi.p_norm)


#%%

dataof = "DE"
if(dataof == "DE"):
    file_groupXY = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed','XYarusal.csv')
else:
    file_groupXY = os.path.join('C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed','XYarusal.csv')
    
