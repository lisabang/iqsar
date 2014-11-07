
def fromlist(somelist,numsamples,sizeofsamples):
    """this generates a random set of samples from a list"""
    samples=[]
    import random
    import pandas
    for x in xrange(numsamples):
        samples.append(random.sample(somelist.columns,sizeofsamples))
    return samples
        #print random.sample(somelist,sizeofsamples)
    #return samples.append(x)
   
def fromdict(somedict,numsamples,sizeofsamples):
    """this generates a random set of samples from a dict"""
    samples=[]
    import random
    for x in xrange(numsamples):
        samples.append(random.sample(somedict.keys(),sizeofsamples))
    return samples
