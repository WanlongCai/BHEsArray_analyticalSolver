# -*- coding: utf-8 -*- {}
'''
csv reader
'''
import matplotlib.pyplot as plt
import numpy as np
from scipy import special as sp
import os
import math
import pandas as pd
import csv

import beier.py as beier
#%% semi analytical result
ana_rt_df_Tin = pd.read_csv('./semi_ana/Result_Tin.csv',
                    delimiter=',',
                    index_col=[0],
                    dtype={'data_index': str})
ana_rt_df_Tout = pd.read_csv('./semi_ana/Result_Tout.csv',
                    delimiter=',',
                    index_col=[0],
                    dtype={'data_index': str})

#%%beier
beier_T_fluid_array = beier.xxx
beier_time_array = beier.xxx



#%%plotting
