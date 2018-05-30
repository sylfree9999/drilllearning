# coding: utf-8
"""
Created on May 28 2018

@author: Riona.Zhang
"""

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


def plot_scatter_trend(target,trend,cycle,fn_plotoutput):      
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(211)
    target.plot(ax=ax, fontsize=16,color='blue')
    trend.plot(ax=ax, fontsize=16,color='pink')
    legend = ax.get_legend()
    plt.title("y_trend")

    ax = fig.add_subplot(212)
    cycle.plot(ax=ax, fontsize=16,color='pink')
    plt.title( "y_cycle")
    fig.savefig(fn_plotoutput)

