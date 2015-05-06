import numpy as np
from sklearn import cross_validation
def mlr(x_of_trainingset,y_actual):
    
    columnnames=list(x_of_trainingset.columns.values)
    npones=np.ones(len(y_actual), float)
    A_sl=x_of_trainingset.as_matrix()
    A=np.column_stack([A_sl,npones])
    lstsq,residuals,rank,something=np.linalg.lstsq(A, y_actual)
    degfreedom=y_actual.size-1
    
    r2=1-residuals/(y_actual.size*y_actual.var())
    r2adj=1-(((1-r2)*degfreedom)/(y_actual.size-rank-2))
    RMSE=np.sqrt(1-r2)*np.std(y_actual)

    #fitness=collections.namedtuple([x_of_trainingset],[r2,r2adj,RMSE])
    return lstsq, rank, r2, r2adj, RMSE


    #y_predicted=(lstsq[0]*liu_train(0))+(lstsq[1]*liu_train(1))+(lstsq[2])+(lstsq[3])+(lstsq[4])+(lstsq[5])+lstsq[6]
    #print "y-predicted:"
    #print y_predicted
def mlrr(x_of_trainingset,y_actual):
    import numpy as np
    npones=np.ones(len(x_of_trainingset), float)

    A_sl=x_of_trainingset
    A=np.column_stack([A_sl,npones])

    lstsq,residuals,rank,something=np.linalg.lstsq(A, y_actual)
    return lstsq
def kfoldmlr(xi,yi,nfolds):
    '''gives the y-hats for a q2LOO calculation'''
    x=xi.values
    y=yi.values
    
    kf = cross_validation.KFold(len(y), n_folds=nfolds)#indices=None, shuffle=False, random_state=None)
    y_hats=[]
    for train_index, test_index in kf:
        x_train, x_test = x[train_index], x[test_index]
        y_train=y[train_index]
        coefficients=mlrr(x_train,y_train)
        #x_train=x_train
        #y_train=y_train
        yhat=coefficients[-1]
 
        for index in range(x_test.size):
            slopetimesx=x_test[0][index]*coefficients[index]
            yhat=yhat+slopetimesx
        y_hats.append(float(yhat))
        
    #cleanyhats=[]
    #for e in y_hats:
    #    cleanyhats.append(float(e))
    stack=np.asarray(y_hats)
    return stack
def q2loo_mlr(x,y):
    '''calculates q2loo of a linear regression of x and y where both x and y are 1-d'''
    yhats=kfoldmlr(x,y,len(x))
    PRESS=np.sum((y-yhats)**2)
    y_mean = np.mean(y)
    TSS=np.sum((y - y_mean)**2)
    #TSS=sum((y-np.mean(y))**2)
    r2cv=(TSS-PRESS)*(TSS**(-1))#1-(PRESS/TSS)
    return r2cv
def q2lmo_mlr(x,y,kfolds=5):
    '''calculates q2loo of a linear regression of x and y where both x and y are 1-d'''
    if type(kfolds)!=int:
        raise TypeError
    else:
        yhats=kfoldmlr(x,y,kfolds)
        PRESS=sum((y-yhats)**2)
        TSS=sum((y-np.mean(y))**2)
        r2cv=1-(PRESS/TSS)
    return r2cv

