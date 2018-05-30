
# coding: utf-8
"""
Created on May 28 2018

@author: Riona.Zhang
"""

import numpy as np
import pandas as pd

#Adstock
from util_adstock import Adstock
#parameter creating
from random_parlist_create import ram_par_create
#regression modelling
from sklearn.linear_model import BayesianRidge



def rand_search_lm(funcs,df,var_y,var_media,var_nonmedia,n):    
    
    clf = BayesianRidge(compute_score=True,fit_intercept=True)

    my_coefs=np.zeros((n,len(var_media)+ len(var_nonmedia)+1))
    my_scores=np.zeros((n,1))
 
    par_list=ram_par_create(funcs,df,var_media,n)
        
    df_var=df.loc[:,var_y+var_nonmedia+var_media]
    if funcs == "log_y":
        y=np.log(df[var_y]/(100-df[var_y])).values
    elif funcs == "Simple Power":
        y=df[var_y].values
    elif funcs == "S curves":
        y=df[var_y].values
    elif funcs == "log_log":
        y=np.log(df[var_y]).values       
    
    
    ###modeling
    for iteration in range(par_list.shape[0]):
        
        X = df_var.iloc[:,1:].values        
        for j in range(len(var_media)):
           
            if funcs == "log_y":
                X[:,j+len(var_nonmedia)]=Adstock(df[var_media[j]],par_carryover=par_list[iteration][j])
            elif funcs == "Simple Power":
                X[:,j+len(var_nonmedia)]=Adstock(df[var_media[j]],par_carryover=par_list[iteration][j])**par_list[iteration][j+len(var_media)]
            elif funcs == "S curves":
                X[:,j+len(var_nonmedia)]=np.exp(par_list[iteration][j+len(var_media)]-par_list[iteration][j+2*len(var_media)]/(Adstock(df[var_media[j]],par_carryover=par_list[iteration][j])+0.00001))
            elif funcs == "log_log":
                X[:,j+len(var_nonmedia)]=np.log(Adstock(df[var_media[j]],par_carryover=par_list[iteration][j])+0.00001)
                        
        clf.fit(X, y)
        my_coefs[iteration,0]=clf.intercept_
        my_coefs[iteration,1:]=clf.coef_
        my_scores[iteration,0]=clf.score(X,y)
                               

    return my_coefs,my_scores,par_list

