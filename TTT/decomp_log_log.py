
# coding: utf-8

# In[ ]:


# import scipy.integrate as sci
# from decomp import *
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 12:53:29 2018

@author: Franklin.Fu
"""

import numpy as np
import pandas as pd
import scipy.integrate as sci


### partial derivative of each x in regressions, and default version is for log-log tranformed regression
### you have to revise this function for other kinds of non-linear regression

#t: x for integrable function, t must be from 0 to 1
#j: row index in matrix p for the driver selected for partial derivative calculation
#p: breakpoint in the assumed line for integral calculation
#coefs_p: coefs of the regression

def pd_log_log(t,j,p,coefs_p):
    
    x=p[:,0]+(p[:,1]-p[:,0])*t
    
    k=np.exp(coefs_p[0,0])
    for i in range(p.shape[0]):
        if (i==j):
            k=k*coefs_p[i+1,0]*((x[i]+0.01)**(coefs_p[i+1,0]-1)) 
        else:
            k=k*((x[i]+0.01)**coefs_p[i+1,0])
            
    return k*(p[j,1]-p[j,0])


### integral calculation algorithm for contribution decomposition

#ind: the row number selected for calculation (in time series,it's the period selected)
#iteration: interation number in calculation
#xs: predictors (Xs) dataframe for calculation
#coefs_p: coefs in regression (including intercept as the first element)

def cont_est_log_log(ind,division,xs,coefs_p):
    
    ncols=xs.shape[1]
    
    x=np.zeros((ncols,3))
    x[:,1]=xs.iloc[ind,:].values
    x[:,2]=(x[:,1]-x[:,0])/division    
    y=np.zeros((division,ncols))
    
    temp=np.zeros((ncols,2))
    for j in range(temp.shape[0]):
        temp[j,0]=x[j,0]
        temp[j,1]=x[j,0]+x[j,2]
        def f(t):
            return pd_log_log(t,j,temp,coefs_p)
        y[0,j]=sci.romberg(f,0,1)

    for i in range(1,y.shape[0]):
        for j in range(temp.shape[0]):
            temp[j,0]=temp[j,1]
            temp[j,1]=temp[j,0]+x[j,2]
            def f(t):
                return pd_log_log(t,j,temp,coefs_p)
            y[i,j]=sci.romberg(f,0,1)

    return y.sum(axis=0)

