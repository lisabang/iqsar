class data():
    '''splits a dataset into test and training sets by one of three methods: completely random,
    by values of a given column, and by selecting interactively thru an ipynb SelectMultiple widget'''
    def __init__(self,dataset):
        self.dataset=dataset
    def random(self,n_training):
        '''This splits the data into testset and training set randomly.  Just specify the number of compounds you would like to be in the training set.  The first return is the training set, the second is the test set.'''
        if type(n_training) != int:
            raise TypeError("n_training must be of type int")
        else:
            allrows=self.dataset.index.values
            trainrows = np.random.choice(allrows,n_training)
            testrows= [x for x in self.dataset.index.values if x not in trainrows]
            trainingset,testset= self.dataset.ix[trainrows],self.dataset.ix[testrows]
            return trainingset, testset
    def by_col(self,columnname,traincolval):
        '''This splits the dataset according to the values of a given column.  Essentially, this is a manual technique.  For example, one may have a column "Set" which has the a value of 0 or 1 for each column.  One wants the "1"s to be in the training set.  If one uses the by_col method of IQSAR.split.data object, you would specify *.by_col("Set",1)'''
        splitter=self.dataset.copy()[columnname]
        #splitter=splitter
        trainingset=self.dataset[splitter==traincolval]
        testset=self.dataset[splitter!=traincolval]
        return trainingset,testset
    def manuallist(self, trainrows):
        '''If you have a list of rows that you would like to be in the training set, you can do this by passing a list of indexes for those rows into the manuallist method.'''
        if type(trainrows) !=list:
            raise TypeError("trainrows must be of type list")
        else:
            train=pd.DataFrame(sodf.ix[list(trainrows)])
            testrows= [x for x in sodf.index.values if x not in trainrows]
            test=pd.DataFrame(sodf.ix[list(testrows)])
            return test,train


