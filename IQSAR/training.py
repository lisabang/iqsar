import pandas as pd
import numpy as np
class trainingset:

#    def __init__(object, split_column=0):
#        object.sp = split_column
    description = "This splits the dataset into training and test sets."

    def __init__(self,dataset):
        self.dataset=dataset
    def manual(self,column):
        #self.dataset=dataset.groupby(column)
        return self.dataset.groupby(column)
        #return self.groupby(column)
    def random(self,tssize):
        #self.index=dataset.index
        rows = np.random.choice(self.dataset.index.values,tssize)
        #self.dataset = self.dataset.ix[rows]
        return self.dataset.ix[rows]
        #return sampled_df    
