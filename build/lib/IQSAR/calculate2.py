
import scipy.stats as scst

from sklearn import cross_validation
import math
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier


class dataset():
    '''create a dataset object by declaring dataset(pandas dataframe,activity)'''
    def __init__(self,dataframe,y):
        self.dataframe=dataframe
        self.y=y
        
        
    def r2(self,columnname):#,dataframe,y):
        m, b, r_value, p_value, SE = scst.linregress(self.dataframe[columnname],self.y)
        return r_value**2
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
    
    #fit and kfold functions are used to perform the calculation of q2.
    def fit(self,X, Y):
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

    def kfold(self,xi,yi,nfolds):
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
            ab=self.fit(x_train,y_train)[::-1]
            y_hats.append(np.polyval(ab, x_test))

        cleanyhats=[]
        for yhat in y_hats:
            cleanyhats.append(float(yhat))
        stack=np.asarray(cleanyhats)
        return stack
    def q2loo_lr(self,columnname):
        '''calculates q2loo of a linear regression of x and y where both x and y are 1-d'''
        yhats=self.kfold((self.dataframe[columnname]),self.y,(len(self.y)))
        PRESS=sum((self.y-yhats)**2)
        TSS=sum((self.y-np.mean(self.y))**2)
        r2cv=1-(PRESS/TSS)
        return r2cv
    def stentropy(self,columnname):
        lv=list(self.dataframe[columnname])
        Hi=0.0
        for i in set(lv):
            #Hi=Hi+float(lv.count(i))/float(len(lv))
        
            Hi=Hi+float(lv.count(i)/float(len(lv)))*np.log(float(lv.count(i)/float(len(lv))))
        Hi=(-1*Hi)/math.log(float(len(lv)),2)
        return float(Hi)
    def rffeats(self):
        #dataset = lls[list(sumtable.index)]
        #datatarget=z
        # fit an Extra Trees model to the data
        model=RandomForestClassifier()
        #model = ExtraTreesClassifier()
        df32=self.dataframe.astype('float32')
        model.fit(df32, self.y)
        # display the relative importance of each attribute
        rf_feats=pd.DataFrame(model.feature_importances_, index=self.dataframe.columns)
        return rf_feats
    def summarizedesc(self):
        '''this will take 1-5 minutes depencing on dataframe size'''
        asdf=pd.DataFrame(columns=["kurtosis","entropy", "r2","q2"], index=self.dataframe.columns)
        kurtosisadd=[float(scst.kurtosis(self.dataframe[a])) for a in self.dataframe[self.dataframe.columns]]
        r2add=[]
        q2add=[] 
        entropyadd=[]#[self.stentropy(self.dataframe[a]) for a in self.dataframe.columns]
        #rffadd=[]
        for column in self.dataframe.columns:
            x=self.dataframe[column]
            #r2add.append(self.r2(x,self.y))
            r2add.append(self.r2(column))
            q2add.append(self.q2loo_lr(column))#self.y))
            entropyadd.append(self.stentropy(column))
            #rffadd.append(self.rffeats(column))
        #rffadd=self.rffeats()
        asdf["kurtosis"]=kurtosisadd
        asdf["entropy"]=entropyadd
        asdf["r2"]=r2add
        asdf["q2"]=q2add
        #asdf["rf_feats"]=rffadd

        return asdf

    def expl_graph(self,columnname):
    # Fit the model to the sample with a straight line model
        import matplotlib.pyplot as plt
        poly_order = 1
        ab = np.polyfit(self.dataframe[columnname], self.y, poly_order)
        # Evalute the estimated model
        y_fit = np.polyval(ab, self.dataframe[columnname])
        ax=plt.subplot(title=str(self.dataframe[columnname].name)+" vs. "+str(self.y.name))
        
        ax.scatter(self.dataframe[columnname],self.y)
        ax.plot(self.dataframe[columnname], y_fit);
        #ax.figtext
        #ax.title(str(x.name)+" vs. "+str(y.name))
        ax.figure.show()
        print "r2: "+str(self.r2(columnname))

        
        #self.summarizedesc=summarizedesc(self.dataframe,y)
    def scmat(self):
        from IPython.html import widgets # Widget definitions
        from IPython.display import display # Used to display widgets in the notebook

        #self.dataframe

        seldescs = widgets.SelectMultiple(options=list(self.dataframe.columns),description='Selected Descriptors:',)
        display(seldescs)
        def chandler(val): 
            dfsels=pd.DataFrame(self.dataframe[list(val)])
            return pd.scatter_matrix(dfsels, alpha=0.2, diagonal='hist')

        

        button = widgets.Button(description="Get scatter matrix")
        display(button)
        def on_button_clicked(b):
            return chandler(list(seldescs.value))
        
        button.on_click(on_button_clicked)
   

        
