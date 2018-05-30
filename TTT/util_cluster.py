# coding: utf-8
"""
Created on May 28 2018

@author: Riona.Zhang
"""

import numpy as np
import pandas as pd
#cluster
from ordinalCluster import *

def Cluster(x,y,k):  
    out=np.zeros((len(x),k-1),dtype='float32')
    for i in range(len(x)):
        simu_cluster=pd.DataFrame(y[i,:],columns=['y'])
        simu_cluster['x']=np.round(x[i,:],0)

        n=simu_cluster["y"].shape[0]
        D,E=vectorOrinalCluster(df=simu_cluster)
        ind=vectorOrinalClusterIndex(n=n,k=k,E=E);
        out[i]=simu_cluster['x'][ind].tolist()
    return out

