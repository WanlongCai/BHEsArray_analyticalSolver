# -*- coding: utf-8 -*- {}
'''
2D BHEs array model for shifting behavior calculation procedure
Author: Shuang Chen
'''
import sys
print(sys.version)
import numpy as np
import pandas as pd
import time

import base_module.ILS_analytical_solver as mod_ILS
import base_module.Utpye_bhe_analytical_solver as mod_bhe
import base_module.bcs_tespy as mod_nw

#%%main parameters
time_tot = 10*24*60*60 #s
delta_t = 86400 #s
timestep_tot = int(time_tot/delta_t)

#BHE
BHE_num = 9
BHE_length = 50 #m
BHE_f_r = 0.5 #kg/s

#%%initialize
###main data containers initialise
row_name = []
for i in range(1, BHE_num+1):
    row_name.append('BHE' + str(i))
col_name = []
for i in range(0, timestep_tot+1):
    col_name.append('Time at ' + str(i) + 'step')
##soil
Result_df_soil = pd.DataFrame(np.zeros((BHE_num, timestep_tot+1)),index=row_name, columns=col_name)
##BHE
#BHE power is the driving force of the system, start from timestep = 1,
#all other results e.g. fluid and soil temperature are started from timestep = 1.
#power
Result_df_BHE_power = pd.DataFrame(np.zeros((BHE_num, timestep_tot+1)),index=row_name, columns=col_name)
#velocity
Result_df_BHE_f_r = pd.DataFrame(np.zeros((BHE_num, timestep_tot+1)),index=row_name, columns=col_name)
##fluid
#inflow T
Result_df_fluid_in = pd.DataFrame(index=row_name, columns=col_name)
#outflow T
Result_df_fluid_out = pd.DataFrame(index=row_name, columns=col_name)

#parameters initialise
#BHE
Result_df_BHE_f_r = Result_df_BHE_f_r + BHE_f_r
#soil
T0 = mod_ILS.T0
Result_df_soil.iloc[:,0] = T0

   
#%%solve
#solver time counter starts
time_solver_start = time.clock()
print('Solve process')
max_iter = 100

for step in range(1, timestep_tot +1):
    t = step * delta_t
    print('timestep = %d start' % step )
    # equal power for all BHEs on the first thermal loading
    if step == 1:
        #update global dataframe BHE power
        Result_df_BHE_power.iloc[:,1] = mod_nw.consumer_demand(0)/BHE_num
#        TODO: mod_bhe two calculation sort
        #update global dataframe BHE inflow and out flow
        Result_df_fluid_in.iloc[:,1] = mod_bhe.Type_1U_BHE_cal_singel(
                Result_df_BHE_power.iloc[0,1], T0)[0]
        Result_df_fluid_out.iloc[:,1] = mod_bhe.Type_1U_BHE_cal_singel(
                Result_df_BHE_power.iloc[0,1], T0)[1]
        #soil
        #global sourceterm dataframe in [W/m] in module ILS initialise ab timestep = 1
        mod_ILS.st_dataframe(1,0, Result_df_BHE_power.iloc[0,1]/BHE_length)
        #update global dataframe soil temperature
        for j in range(BHE_num):
            Result_df_soil.iloc[j,1] = mod_ILS.ILS_solver(step,j)
    else:
        #picard iteration until Tout achieves converge
        for i in range(max_iter):
            print('Iteration %d :' % i)
            if i == max_iter - 1:
                raise Exception('The iteration could not achieve converge within %d steps' % max_iter)
            #1st: TESPy solver
            if_converge, f_r, T_in = mod_nw.nw_solver(t,
                                      Result_df_fluid_in.iloc[:,step-1],
                                      Result_df_fluid_out.iloc[:,step-1])
            #2nd: BHE solver
            for j in range(BHE_num):#loop all BHEs
#                TODO: mod_bhe two calculation sort
                #get each BHE's Tout
                Result_df_fluid_out.iloc[j,step] = mod_bhe.Type_1U_BHE_cal(
                Result_df_fluid_in.iloc[j,step], Result_df_soil.iloc[j,step-1])[0]
                #get each BHE's power
                Result_df_BHE_power.iloc[j,step] = mod_bhe.Type_1U_BHE_cal(
                Result_df_fluid_in.iloc[j,step], Result_df_soil.iloc[j,step-1])[1]
                #update the global sourceterm dataframe in module ILS
                mod_ILS.st_dataframe(step,j, Result_df_BHE_power.iloc[j,step]/BHE_length)
            #determin if the Tout is converged
            if (if_converge):
                break
        #3nd: ILS solver
        #update global dataframe soil temperature
        for j in range(BHE_num):
            Result_df_soil.iloc[j,step] = mod_ILS.ILS_solver(step,j)
                   
#solver time counter end
time_solver_end = time.clock()
print('total solver execution took', (time_solver_end - time_solver_start)/60, 'min' )
print('The whole computation terminated on', time.ctime() )
