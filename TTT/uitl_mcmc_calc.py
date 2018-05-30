
# coding: utf-8
"""
Created on May 28 2018

@author: Riona.Zhang
"""

import numpy as np
import pandas as pd

import gc
import datetime

#Adstock
from util_adstock import Adstock

from sklearn.metrics import r2_score
import statsmodels.api as sm

# contribution
from decomp_logistic import cont_est_logistic
from decomp_log_log import cont_est_log_log


import pickle
my_sm = pickle.load(open('mcmc_pystan.pkl', 'rb'))

def get_coef_pys(df,var_y,var_nonmedia,var_media,par_list,funcs,start_date,end_date,cal_mean):  

    K1=len(var_nonmedia)
    K2=len(var_media)
    N=df[var_y].shape[0]

    out_contr_pct=np.zeros((len(par_list),len(var_media)),dtype='float32')
    out_r2=np.zeros(len(par_list))
    out_dw=np.zeros(len(par_list))
    rate = np.arange(0,10,0.1)#########################################可调节参数
    rate_li = rate.tolist()
    act_index = rate_li.index(1)
    y_summary = np.zeros((len(par_list),len(var_media),len(rate)))
    X_summary = np.zeros((len(par_list),len(var_media),len(rate)))

    ###modeling
    for iteration in range(par_list.shape[0]):
        print(iteration,datetime.datetime.now())
        
        y=df[df.columns[0]].values
        ################################################################################################## 
        if funcs == "log_y":
            y=np.log(y/(100-y))  
        elif funcs == "log_log":
            y=np.log(y)
        ################################################################################################## 
        
        X = df[df.columns[1:]].values       
        for i in range(0,len(var_media)): #loop for each media variable only
            #get_adstock(X[:,i+len(var_nonmedia)],par_list[iteration,i]) #obj.copy()
            X[:,i+len(var_nonmedia)]=Adstock(X[:,i+len(var_nonmedia)],par_list[iteration,i]) #obj.copy()
            ##################################################################################################         
            if funcs == "Simple Power":
                X[:,i+len(var_nonmedia)]=X[:,i+len(var_nonmedia)]**par_list[iteration][i+len(var_media)]
            elif funcs == "S curves":
                X[:,i+len(var_nonmedia)]=np.exp(par_list[iteration][i+len(var_media)]-par_list[iteration][i+2*len(var_media)]/ (X[:,i+len(var_nonmedia)]+0.001))           
            elif funcs == "log_log":
                X[:,i+len(var_nonmedia)]=np.log(X[:,i+len(var_nonmedia)]+0.001)                
            ##################################################################################################             

        #keep data (post adstock processing) at originial scale for later usage
        X_raw=X.copy()
        y_raw=y.copy() 
        
        y = (y-y.mean())/y.std()
        for col in range(0,X.shape[1]):
            X[:,col]=(X[:,col]-X[:,col].mean())/X[:,col].std()

        X1=X[:,:K1];X1.shape=(N,K1)
        X2=X[:,-K2:];X2.shape=(N,K2)
        y=y;y.shape=(N,)

        lin_reg_dat = {
                     'N': N,
                     'K1': K1,
                     'K2': K2,
                     'y': y,
                     'X1': X1,
                     'X2': X2,
                    }
        fit = my_sm.sampling(data=lin_reg_dat,iter=10000,warmup=2000,thin=5)
        

        # convert2original scale: beta first, followed by intercept
        mcoefs= np.concatenate((np.array([fit.extract()['alpha'].mean(0)]),fit.extract()['beta1'].mean(0),fit.extract()['beta2'].mean(0)))
        
        mcoefs_raw = [mcoefs[col+1]*y_raw.std()/X_raw[:,col].std() for col in range(0,X.shape[1])]
        mcoefs_raw_intercept=mcoefs[0]*y_raw.std()+y_raw.mean()-X_raw.dot(mcoefs_raw).mean()
        
        y_raw_hat=X_raw.dot(mcoefs_raw)+mcoefs_raw_intercept
        resids=y_raw-y_raw_hat 

        out_r2[iteration]=r2_score(y_raw, y_raw_hat)                                         
        out_dw[iteration]=sm.stats.durbin_watson(resids, axis=0)

        #decomp################################################################################################ 
        if funcs == "log_y":

            X = df[df.columns[1:]].values
            distr=X
            for i in range(0,len(var_media)): 
                X[:,i+len(var_nonmedia)]=Adstock(X[:,i+len(var_nonmedia)],par_list[iteration,i])

            df_X=pd.DataFrame(X,columns=df.columns[1:])            
            coefs_p=np.expand_dims(np.append(mcoefs_raw_intercept,mcoefs_raw), axis=1)
            for i in range(distr.shape[0]):
                distr[i,:]=cont_est_logistic(ind=i,division=100,xs=df_X,coefs_p=coefs_p)
            contr=distr.sum(axis=0)
            contr_media=contr[len(var_nonmedia):]
            out_contr_pct[iteration,:]=[100*contr_media[col]/sum(contr_media) for col in range(len(contr_media))]


        elif funcs == "Simple Power":
            contr=[sum(X_raw[:,i].dot(mcoefs_raw[i])) for i in range(len(var_nonmedia),X.shape[1])]
            out_contr_pct[iteration,:]=[100*contr[i]/sum(contr) for i in range(0,len(contr))]

        elif funcs == "S curves":
            contr=[sum(X_raw[:,i].dot(mcoefs_raw[i])) for i in range(len(var_nonmedia),X.shape[1])]
            out_contr_pct[iteration,:]=[100*contr[i]/sum(contr) for i in range(0,len(contr))]

        elif funcs == "log_log":

            X = df[df.columns[1:]].values
            distr=X
            for i in range(0,len(var_media)): 
                X[:,i+len(var_nonmedia)]=Adstock(X[:,i+len(var_nonmedia)],par_list[iteration,i])        
            df_X=pd.DataFrame(X,columns=df.columns[1:])            
            coefs_p=np.expand_dims(np.append(mcoefs_raw_intercept,mcoefs_raw), axis=1)
            for i in range(distr.shape[0]):
                distr[i,:]=cont_est_log_log(ind=i,division=100,xs=df_X,coefs_p=coefs_p)
            contr=distr.sum(axis=0)
            contr_media=contr[len(var_nonmedia):]
            out_contr_pct[iteration,:]=[100*contr_media[col]/sum(contr_media) for col in range(len(contr_media))]

        # simulate the curve#################################################################################  

        #calculate X_curve
        for i in range(len(var_media)):
            for j in range(len(rate)):
                #put a flag for calculating the average or sum
                if cal_mean == True:
                    X_summary[iteration,i,j] = rate[j]* df.loc[start_date:end_date,[var_media[i]]].mean()
                else:
                    X_summary[iteration,i,j] = rate[j]* df.loc[start_date:end_date,[var_media[i]]].sum()

        #calculate y_summary
        for i in range(len(var_media)):
            df_sim = df.loc[:end_date,var_y+var_nonmedia+var_media].copy(deep=True)
            y_predict = np.zeros((len(df_sim),len(rate)))  

            for j in range(len(rate)):
                df_sim.loc[start_date:end_date,[var_media[i]]] = rate[j]*df.loc[start_date:end_date,[var_media[i]]]         

                #simulate X with different rating for predict y
                X_sim = df_sim[df_sim.columns[1:]].values

                for t in range(len(var_media)):
                    X_sim[:,t+len(var_nonmedia)]=Adstock(X_sim[:,t+len(var_nonmedia)],par_list[iteration,t]) #obj.copy()
                    if funcs == "Simple Power":
                        X_sim[:,t+len(var_nonmedia)]=X_sim[:,t+len(var_nonmedia)]**par_list[iteration][t+len(var_media)]
                    elif funcs == "S curves":
                        X_sim[:,t+len(var_nonmedia)]=np.exp(par_list[iteration][t+len(var_media)]-par_list[iteration][t+2*len(var_media)]/ (X_sim[:,t+len(var_nonmedia)]+0.001))           
                    elif funcs == "log_log":
                        X_sim[:,t+len(var_nonmedia)]=np.log(X_sim[:,t+len(var_nonmedia)]+0.001)                            

                y_predict[:,j] = X_sim.dot(mcoefs_raw)+ mcoefs_raw_intercept

                if funcs == "log_y":
                    y_predict[:,j] = 100/(np.exp(-(y_predict[:,j]))+1)
                elif funcs == "log_log":
                    y_predict[:,j]= np.exp(y_predict[:,j])

            n = len(df.loc[start_date:end_date]) 
            if cal_mean == True:
                y_summary[iteration,i,:] = y_predict[-n:,:].mean(axis=0)
            else:
                y_summary[iteration,i,:] = y_predict[-n:,:].sum(axis=0)
        y=None
        X=None
        X_1=None
        X_raw=None
        y_raw=None
        X_sim=None
        y_predict=None
        
        del y, X, X_1, X_raw, y_raw, X_sim, y_predict
        gc.collect()
       
    return out_r2,out_dw,out_contr_pct,X_summary,y_summary,act_index

