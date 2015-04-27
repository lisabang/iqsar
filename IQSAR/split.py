class data():
    '''splits a dataset into test and training sets by one of three methods: completely random,
    by values of a given column, and by selecting interactively thru an ipynb SelectMultiple widget'''
    def __init__(self,dataset):
        self.dataset=dataset
    def random(self,n_training):
        if type(n_training) != int:
            raise TypeError("n_training must be of type int")
        else:
            allrows=self.dataset.index.values
            trainrows = np.random.choice(allrows,n_training)
            testrows= [x for x in self.dataset.index.values if x not in trainrows]
            trainingset,testset= self.dataset.ix[trainrows],self.dataset.ix[testrows]
            return trainingset, testset
    def by_col(self,columnname,traincolval):
        #columnname
        #liu_train=liu[liu.Seta !=2].copy()
        splitter=self.dataset.copy()[columnname]
        #splitter=splitter
        trainingset=self.dataset[splitter==traincolval]
        testset=self.dataset[splitter!=traincolval]
        return trainingset,testset
    def manuallist(self, trainrows):
        if type(trainrows) !=list:
            raise TypeError("trainrows must be of type list")
        else:
            train=pd.DataFrame(sodf.ix[list(trainrows)])
            testrows= [x for x in sodf.index.values if x not in trainrows]
            test=pd.DataFrame(sodf.ix[list(testrows)])
            return test,train


