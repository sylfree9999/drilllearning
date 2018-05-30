# coding: utf-8
"""
Created on May 28 2018

@author: Riona.Zhang
"""

import numpy as np

    
def par_title (funcs,var_media):
    par_cr=["cr_"+ x for x in var_media]
    par_power=["par_"+ x for x in var_media]
    par_s_1=["par_a_"+ x for x in var_media]
    par_s_2=["par_b_"+ x for x in var_media]  
    
    if funcs == "log_y":
        par_title = par_cr
    elif funcs == "Simple Power":
        par_title = np.concatenate([par_cr,par_power])        
    elif funcs == "S curves":
        par_title = np.concatenate([par_cr,par_s_1,par_s_2])        
    elif funcs == "log_log":
        par_title = par_cr
        
    return par_title

