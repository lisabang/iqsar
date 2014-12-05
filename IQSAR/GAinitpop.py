import random
import numpy as np
class genind():
    """sumtable is generated from IQSAR.filter.desc()"""
    def __init__(self,basetable):#,datatable):
        self.basetable=basetable
        #self.datatable=datatable
    def random(self,desc_in_ind):
        #this generates a random set of samples from a list.  
        #argument should be an integer of desired individual size
        while type(desc_in_ind) is not int:
            try:
                desc_in_ind=int(desc_in_ind)
                break
            except ValueError:
                print "The number of descriptors per individual should be of type int"
        #elif type(desc_in_ind)==int:
        smple=random.sample(self.basetable.columns,desc_in_ind)
        return smple
    
    
"""
def mutRan(ind,indpb):
   # mutpool=[str(i) for i in ndesc.index if i not in ind]
    for descriptor in ind:
        if np.random.binomial(1,indpb,1)==1:
            ind[ind.index(descriptor)]=random.choice(ndesc.index)#[str(i) for i in ndesc.index if i not in ind])
            #np.random.choice(ind.remove(descriptor))
            #ind[np.random.choice(zeroindexes,1,replace=False)]=1
    return ind,


def fromlist(somelist,numsamples,sizeofsamples):
 
    samples=[]
    import random
    import pandas
    for x in xrange(numsamples):
        samples.append(random.sample(somelist.columns,sizeofsamples))
    return samples
        #print random.sample(somelist,sizeofsamples)
    #return samples.append(x)
   
def fromdict(somedict,numsamples,sizeofsamples):
    samples=[]
    import random
    for x in xrange(numsamples):
        samples.append(random.sample(somedict.keys(),sizeofsamples))
    return samples

"""
