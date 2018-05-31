import pandas as pd
import numpy as np
import scipy.signal as scisig
import os
from datetime import datetime
from datetime import timedelta
from calendar import timegm
import dateutil.parser


import matplotlib.pyplot as plt
import numpy as np
from random import randint

import pywt
from sklearn.mixture import GaussianMixture

#%%
participant_data_path = "C:\\Users\\vojha\\Dropbox\\0_Programming\\ESUM_Experiments\\Participant_Data"
filepath = participant_data_path+"\\gps_locations"

#good examples: 6, 11,16,23
#bad examples: 5, 17, 33, 36

participant = 23
file_name = 'EDA_data_'+str(participant)+'.csv'
eda_file =  os.path.join(filepath,file_name)
eda_data = pd.DataFrame.from_csv(eda_file)


eda_signal = eda_data["EDA"].tolist() 

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[9, 7])
plt.plot(eda_signal, linewidth=1,  label="EDA signal")
ax.set_ylabel("Value")
ax.set_xlabel("Samples")
plt.legend()
plt.show()
fig.savefig('considered_ex_4.pdf')
plt.close(fig)