

import numpy as np
from collections import Counter
#data import
import ast
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
#RESULT_DIR="/home/lisabang/1qsardb/2011IECR11337.qdb/"


def read_dir(directory, complete=False, outs=True):
    outfiles=os.listdir(directory)
    outs=[]
    ins=[]
    fulldirs=[]
    for o in outfiles:
        if o.endswith("z.txt"):
            outs.append(directory+o)
        elif o.endswith("a.txt"):
            ins.append(directory+o)
    for item in outfiles:
        fulldirs.append(directory+item)
    #for item in outfiles:
    if complete==True:
        return fulldirs
    if complete==False:
        return ins, outs

#infiles=read_dir(RESULT_DIR)[0]
#outfiles=read_dir(RESULT_DIR)[1]


class eval(object):
    def __init__(self, dir=None):
        if dir == None:
            raise ValueError("Must enter a value for dir as argument!")
        elif type(dir) == str:
           self.dir=dir
        else:
            raise TypeError("Value for dir must be a string with a result directory path!")

    def _eval_inputs(self,i):
        #endpops=pd.read_table(i)
        fp=open(i, "r")
        m =fp.read()
        ewf= ast.literal_eval(m)
        ewf=ewf[0]
          
        compdesc=[item for sublist in ewf for item in sublist]
            #compdesc=[item for sublist in compdesc for item in sublist]
        return [Counter(compdesc), compdesc]
    def _eval_outputs(self,i):
            #endpops=pd.read_table(i)
        fp=open(i, "r")
        m =fp.read()
        #m.split("]]")
        index=m.find("]\n")
        popdata=m[:index+1]
        index2=m.find("BEST = ")
        #metadata_best=m[index2+8:index2+13]#len(m)]
        metadata=m[index2:len(m)]
           
        ewf= ast.literal_eval(popdata)
        compdesc=[item for sublist in ewf for item in sublist]
        return [Counter(compdesc), metadata, compdesc]

# creation of the data
    def get_freq(self):
        infiles=read_dir(self.dir)[0]
        indescpool=[]
        for file in infiles:
            indescpool.append(self._eval_inputs(file)[1])
        indescpool=[item for sublist in indescpool for item in sublist]
        print len(set(indescpool)), "different descriptors in;", len(indescpool), "descs total in"
        incounter=Counter(indescpool)
    
        idict={}
        for key, value in sorted(incounter.iteritems(), key=lambda (k,v): (v,k)):
            idict[key]=value
        outfiles=read_dir(self.dir)[1]
        outdescpool=[]
        for file in outfiles:
            outdescpool.append(self._eval_outputs(file)[2])
        outdescpool=[item for sublist in outdescpool for item in sublist]
    
        print len(set(outdescpool)), "different descriptors out;", len(outdescpool), "descs total out"
        outcounter=Counter(outdescpool)
        olabels=[]
        ovalues=[]
        odict={}
        for key, value in sorted(outcounter.iteritems(), key=lambda (k,v): (v,k)):
            #olabels.append(key)
            #ovalues.append(value)
            odict[key]=value
        idf=pd.Series(idict, index=idict.keys(), name="Inputs")
        odf=pd.Series(odict, index=odict.keys(), name="Outputs")
        idf.index.name="Descriptors"
        idf.reset_index()
        alldf=pd.concat([idf, odf], axis=1)
        alldf=alldf.fillna(0)
        alldf=alldf.sort(columns="Outputs", ascending=False)

        return alldf



    def graph_overlay(self):
        alldf=self.get_freq()
        #plt.figure();
        alldf.plot(kind="bar")
        sdff=alldf.plot(kind="line", title=str(self.dir), stacked=False)
        return sdff
    
    
    
    #pd.DataFrame.plot(alldf, x=alldf.index, y=alldf["Inputs"])
    ##lt.plot(alldf.index, alldf["Inputs"])
    
    #plt.grid()
    #idf=pd.DataFrame(idict, index=idict.keys())
    #return alldf.plot(x=alldf.index, y="Inputs")

    '''ind = np.arange(len(alldf.index))  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    #plt.figure(figsize(12,60), facecolor="white")
    rects1 = ax.barh(ind, alldf["Inputs"], width, color='r')

    rects2 = ax.barh(ind+width, alldf["Outputs"], width, color='y')

# add some text for labels, title and axes ticks
    ax.set_xlabel('Frequencies')
    ax.set_title('Descriptors')
    ax.set_yticks(ind+width)
    ax.set_yticklabels(list(alldf.index))

    ax.legend( (rects1[0], rects2[0]), ('Inputs', 'Outputs') )

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.show()
    #return alldf#odict, idict'''
    

