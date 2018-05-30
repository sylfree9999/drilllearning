
# coding: utf-8
"""
Created on May 28 2018

@author: Riona.Zhang
"""

from util_adstock import Adstock
import numpy as np
import pandas as pd

def auto_corr_window(df,var_media,var_y,cr):    
    df_Xs = df[var_media]
    corr=np.zeros((len(cr),len(var_media)))
    
    for i in range(len(var_media)):
        corr_tmp=[]
        for c in cr:
            df_Xs = df_Xs.apply(Adstock,par_carryover=c,axis=0)
            df_Xs_filter = pd.DataFrame( df_Xs.loc[(df_Xs.loc[:,var_media[i]]>0),var_media[i]])            
            df_cal = pd.merge(df[var_y],df_Xs_filter,right_index=True, left_index=True)
            corr_tmp = np.concatenate((corr_tmp,df_cal[[var_media[i]]].corrwith(df_cal[",".join(var_y)]).values))
        corr[:,i]=corr_tmp
        
    return corr

