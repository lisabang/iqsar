import GA2 as G
import pandas as pd
import time
import numpy as np
#data import
df=pd.read_csv("/home/lisabang/Documents/iqsar_GA/descriptors422_incliu.csv", index_col=0)

#data cleanup
#df=df.drop('No.', 1)
def shuffle(adf):
    return adf.iloc[np.random.permutation(np.arange(len(adf)))].copy()
    
yexp=shuffle(df["Y Exp."])
xtable=df.drop('Y Exp.', 1)

#seting up the GA
def doGA(rseed):
    run=G.GAdescsel(xtable,yexp,ngen=10000,popsize=100, indsize=6, cx=.5, mut=.05, seed=rseed)
    firstresult=run.evolve()
    #recurresult=run01.evolverecur(pops=3)
    now = time.strftime("%x")+"_"+time.strftime("%X")
    now=''.join(e for e in now if e.isalnum())
    origpopfilename=str(rseed)+"_"+now+"a.txt"
    finapopfilename=str(rseed)+"_"+now+"z.txt"
    f=open(origpopfilename,"w")
    f.write(str(firstresult[0:1]))
    hi=open(finapopfilename,"w")
    hi.write(str(firstresult[2:]))
    f.close()
    hi.close()
    return firstresult


#write to file using datetime as name of file
#import time
#now = time.strftime("%x")+"_"+time.strftime("%X")
#now=''.join(e for e in now if e.isalnum())
#filename=str("runtime"+now)
#f=open(filename+"a.txt", "w")
#f.write(str(firstresult[0]))
#f.close()
#h=open(filename+"z.txt", "w")
#h.write(str(firstresult[1:]))
#h.close()



#f=open("recuroriginalpop.txt", "w")
#f.write(str(recurresult[0]))
#f.close()

#h=open("recurendpop.txt", "w")
#h.write(str(recurresult[1:]))
#h.close()

#print firstresult[2], recurresult
#print run01.evolverecur(pops=3)


if __name__ == "__main__":
    import sys
    doGA(int(sys.argv[1]))
    
