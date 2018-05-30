# coding: utf-8
"""
Created on May 28 2018

@author: Riona.Zhang
"""

import numpy as np
import pandas as pd

from par_title_create import par_title


###for filtering simple bys resulte
#(50% * r2 + 50% * sum(rank of each coef of var_media))

def results_filter(funcs,my_coefs,my_scores,par_list,var_media,var_nonmedia,row_n):
    
    # column title
    par_tit=par_title (funcs,var_media)
    coef_tit=["coefs_"+ x for x in var_nonmedia+var_media]
    
    if funcs == "log_y":
        column_title = np.concatenate([par_tit,np.array(["coefs_intercept"]),coef_tit,np.array(["scores_r2"])])
    elif funcs == "Simple Power":
        column_title = np.concatenate([par_tit,np.array(["coefs_intercept"]),coef_tit,np.array(["scores_r2"])])        
    elif funcs == "S curves":
        column_title = np.concatenate([par_tit,np.array(["coefs_intercept"]),coef_tit,np.array(["scores_r2"])])        
    elif funcs == "log_log":
        column_title = np.concatenate([par_tit,np.array(["coefs_intercept"]),coef_tit,np.array(["scores_r2"])])
      
    
    # combine all the par and convert to df
    my_candidates = np.concatenate([par_list,my_coefs,my_scores],axis=1)
    df_candidates = pd.DataFrame(my_candidates,columns = column_title)

    #ranking    
    rank_index=np.zeros((len(my_coefs),len(var_media)))
    for i, coef in enumerate(coef_tit[len( var_nonmedia):]):
        rank_index[:,i]=df_candidates[coef].rank().values.T
    rank=rank_index.sum(axis=1)
    rank_score=np.array([(val-rank.min())/(rank.max()-rank.min()) for val in rank])
    voting_score=0.5*df_candidates['scores_r2'].values.T+0.5*rank_score
    df_candidates["voting_score"]=voting_score.T
    df_candidates_ranking=df_candidates.sort_values(by='voting_score',ascending=False)[:row_n]
    
    del df_candidates_ranking['voting_score']
    
    '''
    #filter
    for i in range(len(var_media)):
        df_candidates = df_candidates.loc[(df_candidates.iloc[:,i+par_list.shape[1]+len(var_nonmedia)+1] > 0),:]
    
    df_candidate_filtered = df_candidates.sort_values(by='scores_r2',ascending=False)
    '''
    return(df_candidates_ranking)



###for filtering the latest mcmc result
def results_ranking(funcs,r2,dw,var_par_list,roi_idx,contr_pct,var_media,fnl_n):
    
    par_tit=par_title (funcs,var_media)
    EI_tit=["EI_"+ x for x in var_media]
    contr_tit=["contr_"+ x for x in var_media]

    if funcs == "log_y":
        column_title = np.concatenate([np.array(["r2"]),np.array(["dw"]),par_tit,EI_tit,contr_tit])
    elif funcs == "Simple Power":
        column_title = np.concatenate([np.array(["r2"]),np.array(["dw"]),par_tit,EI_tit,contr_tit])        
    elif funcs == "S curves":
        column_title = np.concatenate([np.array(["r2"]),np.array(["dw"]),par_tit,EI_tit,contr_tit])        
    elif funcs == "log_log":
        column_title = np.concatenate([np.array(["r2"]),np.array(["dw"]),par_tit,EI_tit,contr_tit])


    # combine all the par and convert to df
    my_tmp_1=np.column_stack((r2,dw,var_par_list,roi_idx,contr_pct))
    df_candidate_ranked = pd.DataFrame(my_tmp_1,columns = [column_title]).sort_values(by='r2',ascending=False)

    #top50% result
    df_result = df_candidate_ranked[:fnl_n]
    fnl_r2 = df_result["r2"].values
    fnl_dw = df_result["dw"].values
    fnl_var_par_list = df_result[par_tit].values
    fnl_roi_idx = df_result[EI_tit].values
    fnl_contr_pct = df_result[contr_tit].values
    rnk=df_result.index.values
    
    return fnl_r2,fnl_dw,fnl_var_par_list,fnl_roi_idx,fnl_contr_pct,rnk
