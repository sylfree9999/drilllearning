
# coding: utf-8
"""
Created on May 28 2018

@author: Riona.Zhang
"""

import math
import numpy as np
import matplotlib.pyplot as plt


def plot_scatter_corr(x,y,labels,fn_plotoutput):      
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(1,1,1)
    for i in range(0,len(labels)):
        plt.plot(x, y[:,i], label = labels[i] )
    plt.title("Correlation between Adstock and KPI with different Carryover Rate (Time Windows)")
    plt.xticks(x,np.around(x,decimals=2),size='small')
    ax.set_xlabel("Carryover Rate")
    ax.set_ylabel("Correlation")
    plt.legend(loc=1,frameon='True')
    plt.grid(False)
    fig.savefig(fn_plotoutput)


def plot_scatter_ROI(x,y,labels,fn_plotoutput):      
    fig, ax = plt.subplots()
    fig.suptitle('Relative ROI')
    ax.scatter(x, y)
    
    for i, txt in enumerate(labels):
        ax.annotate(txt, (x[i],y[i]))
    ax.plot([0,0], [max(max(x),max(y)),max(max(x),max(y))], ls="--", c=".3")
    plt.xlabel('Support%')
    plt.ylabel('Contribution%')
    ax.set(xlim=(0, max(max(x),max(y))), ylim=(0,max(max(x),max(y))))
    fig.savefig(fn_plotoutput)


def plot_bar_ROI(y,labels,fn_plotoutput):  
    
    fig, ax = plt.subplots()
    fig.suptitle('Media ROI index')
    
    plt.barh(range(len(y)),y)
    plt.xlabel("contr_pct/spend_pct") 
    plt.ylabel("Media")
    plt.yticks(range(len(y)),labels)

    for i,txt in enumerate(y):
        plt.text(txt+0.15,i,'%s' %round(txt,1),ha='center')
    fig.savefig(fn_plotoutput)




def plot_scatter_curve(x,y,cluster,labels,act_index,fn_plotoutput):      
    
    N = math.ceil(x.shape[0]/2)
    n = 1
    fig = plt.figure(figsize=(12,4*N))
    fig.suptitle('Media Response Curve', y=1.05, fontsize=18)

    for i in range(x.shape[0]):
        ax = fig.add_subplot(N,2,n)
        plt.plot(x[i,:], y[i,:], label = labels[i] )
        plt.plot(x[i,act_index], y[i,act_index], '^',color="red" )
        #plt.annotate("(%.1e ,%.1f)" % (x[i,act_index],y[i,act_index]),(x[i,act_index], y[i,act_index]), xytext=(5, 0),textcoords='offset points',ha='left',va='bottom' ,color = "r")
        
        y_cluster=np.zeros_like(cluster)
        for j in range(cluster.shape[1]):
          
            if cluster[i,j].round() in x[i,:].round().tolist():
                id=x[i,:].round().tolist().index(cluster[i,j].round())
            else:
                id=0
                for txt in x[i,:].round().tolist():
                    if txt<cluster[i,j].round():
                        id=id+1
                    else:                      
                        if (txt-x[i,:].round().tolist()[id-1])<(cluster[i,j].round()-txt):
                            id=id-1
                        else:
                            id=id
            y_cluster[i,j]=y[i,id]
            plt.vlines(cluster[i,j], min(y[i,:]),y_cluster[i,j], colors = "goldenrod", linestyles = "dashed")
            
        for xy in zip(cluster[i,:],y_cluster[i,:]):  
            plt.annotate("(%.1e,%.1f)" % xy, xy=xy, xytext=(5, 0), textcoords='offset points', ha='left',va="bottom",color = "goldenrod") 
    
        plt.xlabel("Media Spending/GRP(Imp)")
        plt.ylabel("Awareness")
        plt.legend(loc=1,frameon='True')
        plt.tight_layout()
        n +=1
    fig.savefig(fn_plotoutput)


