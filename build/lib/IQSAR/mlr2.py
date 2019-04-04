"""some crap here in the docstring"""

import pandas as pd
from pylab import *
import numpy as np
from numpy import linalg

from collections import deque

import collections


def mlr(x_of_trainingset,y_actual):
    import numpy as np
    npones=np.ones(len(y_actual), float)

    A_sl=x_of_trainingset.as_matrix()
    A=np.column_stack([A_sl,npones])

    lstsq,residuals,rank,something=np.linalg.lstsq(A, y_actual)
    #print "coefficient output:"
    #print lstsq

    r2=1-residuals/(y_actual.size*y_actual.var())
    #print "r2:"
    #print r2

    degfreedom=y_actual.size-1
    #print "degrees of freedom:"
    #print degfreedom
    y_actual.var()

    r2adj=1-(((1-r2)*degfreedom)/(y_actual.size-rank-1))
    #print "r2adj:"
    #print r2adj

    RMSE=np.sqrt(1-r2)*np.std(y_actual)
    #print "RMSE:"
    #print RMSE


    
    #fitness=collections.namedtuple([x_of_trainingset],[r2,r2adj,RMSE])
    return lstsq, r2, r2adj, RMSE


    #y_predicted=(lstsq[0]*liu_train(0))+(lstsq[1]*liu_train(1))+(lstsq[2])+(lstsq[3])+(lstsq[4])+(lstsq[5])+lstsq[6]
    #print "y-predicted:"
    #print y_predicted

    """
    LOOdict={}
    for n in range(0,len(liu_train(0))):
    #if n in x1.keys():
        #leaveoneout=((lstsq[0]*x1[n])+(lstsq[1]*x2[n])+(lstsq[2]*x3[n])+(lstsq[3]*x4[n])+(lstsq[4]*x5[n])+(lstsq[5]*x6[n])+lstsq[6])
        #leaveoneout=y_predicted[n]
        Aloo=np.delete(A, (n), axis=0)
        zloo=np.delete(z, (n), axis=0)
        #print zloo
        lstsqLOO,residualsLOO,rankLOO,somethingLOO=linalg.lstsq(Aloo,zloo)
        LOOdict[n]=lstsqLOO
    #else:
        pass
    #
    #
#yiminusyili=sum(y_predicted)-leaveoneout

#print LOOdict[0], LOOdict[1]

for f in range(0,len(x1)):
    gsloo=LOOdict[f][0]*x1+LOOdict[f][1]*x2+LOOdict[f][2]*x3+LOOdict[f][3]*x4+LOOdict[f][4]*x5+LOOdict[f][5]*x6
    #print LOOdict[f][0]*x1+LOOdict[f][1]*x2
    constantloo=LOOdict[f][6]
    loo=gsloo+constantloo
    #print constantloo
#print constantloo
    #for d in range(0,6):
        #print givensampleloo[d]
    #    gsloo[d]*x1+gsloo[d+1]*x2+gsloo[d+2]*x3+gsloo[d+3]+gsloo[d+4]*x4+gsloo[d+5]*x5+gsloo[d+6]
#leaveoneout=((lstsq[0]*x1[n])+(lstsq[1]*x2[n])+(lstsq[2]*x3[n])+(lstsq[3]*x4[n])+(lstsq[4]*x5[n])+(lstsq[5]*x6[n])+lstsq[6])

#import numpy as np
#from numpy import linalg
#A = np.column_stack([x1, x2, x3, x4, x5, x6, np.ones(64, float)])
#lstsq,residuals,rank,something=linalg.lstsq(A, z)


# In[77]:

ssss=(liu_train["Y-Pred"]-loo)


# In[78]:

diff=((liu_train["Y-Pred"]-liu_train["Y-Pred"].mean()))


# In[79]:

q_squared=1-((sum(np.square(ssss)))/sum(np.square(diff)))


# In[79]:




# In[80]:
print "q_squaredLOO:"
print q_squared
"""
