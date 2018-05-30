# coding: utf-8
"""
Created on May 28 2018

@author: Riona.Zhang
"""

import numpy as np

def Adstock(data_in,par_carryover):
    
    data_carried= np.zeros_like(data_in)
    data_out = np.zeros_like(data_in)    
    
    for i in range(1,len(data_in)):
        data_carried[i] = (data_in[i-1] + data_carried[i-1]) * par_carryover        
    data_out=data_in + data_carried   
    
    return data_out

