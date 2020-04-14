# -*- coding: utf-8 -*- {}
'''
csv reader
'''
import matplotlib.pyplot as plt
import numpy as np
from scipy import special as sp
import pandas as pd
import csv
plt.rcParams.update({'figure.max_open_warning': 0})

#%% fig
data_size = 100/0.2
xaxial = np.arange(0,data_size,1)
#plt.figure(figsize=(6, 4), dpi = 300)
plt.figure()
   
#beier
plt.plot(beier_time_array,beier_T_fluid_array,c='r',lw=1,ls='--', marker='x',markersize=4,  label= 'beier')
#ana
#plt.plot(xaxial,ana_rt_df_test.iloc[0,:]-30-273.15,c='c',lw=1,ls=':', marker='x',markersize=4,  label= 'ana BHE1 soil')

#    plt.grid(True, linestyle = "-.", color = "gray", linewidth = "0.5")
#    plt.axhline(-5, c ='k',ls='--',lw=1, )
plt.xlim([0,100])
plt.ylim([10,30])
#plt.yticks(np.arange(7, 12, 0.5))
#plt.xticks(np.arange(0,data_size,2),np.arange(0,191,20))
plt.ylabel('Temperature [$^\circ$C]',fontsize=12)
plt.xlabel('Hour',fontsize=12)
plt.legend(loc='best',ncol =1,fontsize=8,labelspacing=0.3)

plt.savefig('bench_result.png', dpi = 300, transparent = False)

