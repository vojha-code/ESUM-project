# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 13:50:52 2018

@author: vojha
"""
%reset -f
%clear

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from random import randint

#%%
#markedEDA = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed\markedEDA","eda_ledalab")
#eventEDA = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Weimar_360\processed\markedEDA","event_ledalab")

markedEDA = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed\markedEDA","eda_ledalab")
eventEDA = os.path.join("C:\\Users\\vojha\Documents\ETH_project_data\VR_Data\Work\Zurich_360\processed\markedEDA","event_ledalab")

#%%
os.chdir(markedEDA)

eda_files = os.listdir(markedEDA)
pid = 1
for files in eda_files:
    print(" ",pid,files)
    #This will move the file from one folder to another : os.rename(hoboSource, hobodestination)
    os.rename(os.path.join(markedEDA,files),os.path.join(markedEDA,"leda_exp_"+str(pid)+".txt"))
    pid = pid + 1
    

os.chdir(eventEDA)
event_files = os.listdir(eventEDA)
pid = 1
for files in event_files:
    print(" ",pid,files)
    #This will move the file from one folder to another : os.rename(hoboSource, hobodestination)
    os.rename(os.path.join(eventEDA,files),os.path.join(eventEDA,"eventduration_exp_"+str(pid)+".txt"))
    pid = pid + 1    

