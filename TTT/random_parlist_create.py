# coding: utf-8
"""
Created on May 28 2018

@author: Riona.Zhang
"""

import numpy as np
import pandas as pd


def ram_par_create(funcs,df,var_media,n,
                     cr_min=0,cr_max=1,
                     power_alpha_min=0,power_alpha_max=1,
                     par_min=0.01,par_max=1.5):  
    
    xs_n=len(var_media)
    
    cr=np.random.uniform(cr_min,cr_max,size=[n,xs_n])   

    power_alpha=np.random.uniform(power_alpha_min,power_alpha_max,size=[n,xs_n])    

    s_alpha_min=1
    s_alpha_max=10
    s_alpha=np.random.uniform(s_alpha_min,s_alpha_max,size=[n,xs_n])

    s_beta_min=[par_min*df[x].min() for x in var_media]
    s_beta_max=[par_max*df[x].max() for x in var_media]
    s_beta=np.random.uniform(s_beta_min,s_beta_max,size=[n,xs_n])    

    if funcs == "log_y":
        par_list=cr
    elif funcs == "Simple Power":
        par_list=np.concatenate([cr,power_alpha],axis=1)
    elif funcs == "S curves":
        par_list=np.concatenate([cr,s_alpha,s_beta],axis=1)
    elif funcs == "log_log":
        par_list=cr
        
    return par_list

