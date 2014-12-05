import random
import numpy as np

def mutRan(ind,indpb):
   # mutpool=[str(i) for i in ndesc.index if i not in ind]
    for descriptor in ind:
        if np.random.binomial(1,indpb,1)==1:
            ind[ind.index(descriptor)]=random.choice(ndesc.index)#[str(i) for i in ndesc.index if i not in ind])
            #np.random.choice(ind.remove(descriptor))
            #ind[np.random.choice(zeroindexes,1,replace=False)]=1
    return ind,
def hash_ind_list(self):
    return hash(tuple(self))

def makeind(basetable,desc_in_ind):#,datatable):
    import random
    while str(type(basetable)) !="<class 'pandas.core.frame.DataFrame'>":
        raise TypeError("The type of descriptor table should be a Pandas dataframe.")
    while type(desc_in_ind) is not int:
        try:
            print "converting non-int to int"
            desc_in_ind=int(desc_in_ind)
            break
        except ValueError("The number of descriptors per individual should be of type int")  
    smple=random.sample(basetable.columns,desc_in_ind)
    return smple
    

#arguments:  ngen, basetable, y, popsize, indsize, crossoverrate, #mutprob, evaluation function, selection function

class GAdescsel():
    
    def __init__(basetable,y,ngen=1000, popsize=100, indsize=5, cx=.5, mut=.05):
        from deap import creator, base, tools, algorithms
        creator.create("Fitness", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.Fitness, __hash__=hash_ind_list)
        toolbox=base.Toolbox() 
        self.basetable=basetable
        self.y=y
        self.ngen=ngen
        self.popsize=popsize
        self.indsize=indsize
        self.cx=cx
        self.mut=mut
#    def randstartpop(self):
        toolbox.register("genind", makeind, self.indsize)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genind)
        toolbox.register("population",tools.initRepeat, list, toolbox.individual, n=100)
        self.population=toolbox.population()
    def _evalr2(self,ind):
        import mlr3
        return mlr3.mlr(self.basetable[ind],self.y)[2].astype(float),
    def _evalr2adj(self,ind):
        import mlr3
        return mlr3.mlr(self.basetable[ind],self.y)[3].astype(float),
    def _evalq2loo(self,ind):
        import mlr3
        return mlr3.q2loo_mlr(self.basetable[ind],self.y),
    def by_r2(self,evalfunc="q2loo"):
 

        toolbox=base.Toolbox() 
        toolbox.register("evaluate", _evalr2)
        toolbox.register("mate", tools.cxOnePoint) #Uniform, indpb=0.5)
        toolbox.register("mutate", mutRan, indpb=self.mut)
        toolbox.register("select", tools.selBest)
    def by_r2adj():

    def by_q2loo():
        



output: end population, descriptor frequency stats, average fitness
