import scipy.stats as scst

def lst(dataframe,y):
    """This geneates a list of variables whose r2 and kurtosis values are as specified and are therefore not in the tabu list.  These variables should go into the genetic algorithm"""
    nontabulist=[]
    import chemcraft2
    for column in dataframe:
        x=dataframe[column]
        #print z
        #r2=float((scst.pearsonr(x,z)[0])**2)
        #print r2
        kurtosis=float(scst.kurtosis(x))
        r2=chemcraft2.calculate.r2(x,y)
        #r2=rsquared(x,z)
        #if r2> .1:
        #     nontabudict[column]=r2
        if kurtosis<=kurtosisthreshold.value and r2>=r2threshold.value:
              nontabulist.append(column)
    return nontabulist
#print "Non-tabudict size:"
#print len(nontabudict)
#    q2=1-sum(np.square(z-(yexp-x[column])))/(sumoftotsquares)
#    print q2
    #1-((np.square(n-1))*(z-(x*m+c))/(numpy.square(n)(n*z.var())))



