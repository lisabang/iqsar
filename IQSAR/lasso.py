from sklearn import linear_model
import pandas as pd
def doit(xfiltered, y, _alpha=.005, _tol=.1):
    
    lasso=linear_model.Lasso(
    #    this version works to get it down to 672
        alpha=_alpha, tol=_tol, max_iter=100000, normalize=True).fit(xfiltered, y)
    #    alpha=.01, tol=.025,max_iter=100000, normalize=True).fit(xfiltered, y)
    doesthismatter=list(lasso.coef_!=0)
    indexes=[]
    for i, j in enumerate(doesthismatter):
        if j==True:
            indexes.append(i)#doesthismatter.index(i)
#        print xtrain[i]
    lassocols=xfiltered[xfiltered.columns[indexes]].columns
    return pd.DataFrame(lassocols, index=lassocols)
