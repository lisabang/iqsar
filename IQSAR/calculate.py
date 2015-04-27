#def r2(x,y):
#    """gets the r2 value for array x and array y"""
#    y_mean = sum(x)/float(len(y))
#    ss_tot = sum((yi-y_mean)**2 for yi in y)
#    ss_err = sum((yi-xi)**2 for yi,xi in zip(y,x))
#    r2 = 1 - (ss_err/ss_tot)
#    return r2

import scipy.stats as scst

from sklearn import cross_validation
import math
import numpy as np
import pandas as pd
def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

def r2(x, y):
    """ Return R^2 where x and y are array-like."""

    slope, intercept, r_value, p_value, std_err = scst.linregress(x, y)
    return r_value**2


#DO NOT DELETE CODE IN THIS CELL, THIS IS NEEDED TO CALCULATE Q2LOO!!
def fit(X, Y):
    """when inputting fit (x,y), returns tuple (A, b) where y= b * x + A"""
    def mean(Xs):
        return sum(Xs) / len(Xs)
    m_X = mean(X)
    m_Y = mean(Y)

    def std(Xs, m):
        normalizer = len(Xs) - 1
        return math.sqrt(sum((pow(x - m, 2) for x in Xs)) / normalizer)
    # assert np.round(Series(X).std(), 6) == np.round(std(X, m_X), 6)

    def pearson_r(Xs, Ys):

        sum_xy = 0
        sum_sq_v_x = 0
        sum_sq_v_y = 0

        for (x, y) in zip(Xs, Ys):
            var_x = x - m_X
            var_y = y - m_Y
            sum_xy += var_x * var_y
            sum_sq_v_x += pow(var_x, 2)
            sum_sq_v_y += pow(var_y, 2)
        return sum_xy / math.sqrt(sum_sq_v_x * sum_sq_v_y)
    # assert np.round(Series(X).corr(Series(Y)), 6) == np.round(pearson_r(X, Y), 6)

    r = pearson_r(X, Y)
    b = r * (np.std(Y) / np.std(X))
    #b = r * (std(Y, m_Y) / std(X, m_X))
    A = m_Y - b * m_X

    def line(x):
        return b * x + A
    #return line
    return A, b

def kfold(xi,yi,nfolds):
    x=xi.values
    y=yi.values
    kf = cross_validation.KFold(len(y), n_folds=nfolds)#indices=None, shuffle=False, random_state=None)
    y_hats=[]
    for train_index, test_index in kf:
        x_train, x_test = x[train_index], x[test_index]
        y_train=y[train_index]

        x_train=x_train[np.logical_not(np.isnan(x_train))]
        y_train=y_train[np.logical_not(np.isnan(y_train))]
        #poly_order = 1
        #ab = np.polyfit(x_train, y_train, poly_order)
        ab=fit(x_train,y_train)[::-1]
        y_hats.append(np.polyval(ab, x_test))

    cleanyhats=[]
    for yhat in y_hats:
        cleanyhats.append(float(yhat))
    stack=np.asarray(cleanyhats)
    return stack
def q2loo_lr(x,y):
    '''calculates q2loo of a linear regression of x and y where both x and y are 1-d'''
    yhats=kfold(x,y,len(x))
    PRESS=sum((y-yhats)**2)
    TSS=sum((y-np.mean(y))**2)
    r2cv=1-(PRESS/TSS)
    return r2cv
    
def stentropy(x):
    lv=list(x)
    Hi=0.0
    for i in set(lv):
        #Hi=Hi+float(lv.count(i))/float(len(lv))
        
        Hi=Hi+float(lv.count(i)/float(len(lv)))*np.log(float(lv.count(i)/float(len(lv))))
    Hi=(-1*Hi)/math.log(float(len(lv)),2)
    return float(Hi)

def summarizedesc(dataframe,y):
    '''this will take 1-5 minutes depencing on dataframe size'''
    asdf=pd.DataFrame(columns=["kurtosis","entropy", "r2","q2"], index=dataframe.columns)
    kurtosisadd=[float(scst.kurtosis(dataframe[a])) for a in dataframe[dataframe.columns]]
    r2add=[]
    q2add=[] 
    entropyadd=[stentropy(dataframe[a]) for a in dataframe[dataframe.columns]]
    for column in dataframe:
        x=dataframe[column]
        r2add.append(r2(x,y))
        q2add.append(q2loo_lr(x,y))
        #entropyadd.append(float(stentropy(x)))
        
    asdf["kurtosis"]=kurtosisadd
    asdf["entropy"]=entropyadd
    asdf["r2"]=r2add
    asdf["q2"]=q2add

    return asdf
import matplotlib.pyplot as plt
def expl_graph(x,y):
# Fit the model to the sample with a straight line model
    poly_order = 1
    ab = np.polyfit(x,y, poly_order)
    # Evalute the estimated model
    y_fit = np.polyval(ab, x)
    ax=plt.subplot(title=str(x.name)+" vs. "+str(y.name))
    
    ax.scatter(x,y)
    ax.plot(x, y_fit);
    #ax.figtext
    #ax.title(str(x.name)+" vs. "+str(y.name))
    ax.figure.show()
    print "r2: "+str(r2(x,y))
class scmat():
    def __init__(self, sodf):

        self.sodf=sodf.copy()

        seldescs = widgets.SelectMultiple(options=list(self.sodf.columns),description='Selected Descriptors:',)
        display(seldescs)
        def chandler(val): 
            dfsels=pd.DataFrame(sodf[list(val)])
            return pd.scatter_matrix(dfsels, alpha=0.2, diagonal='hist')

        

        button = widgets.ButtonWidget(description="Get scatter matrix")
        display(button)
        def on_button_clicked(b):
            return chandler(list(seldescs.value))
        
        button.on_click(on_button_clicked)
   

    
   

#seldescs.on_trait_change(chelseahandler, 'value')

