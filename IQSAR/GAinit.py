from deap import creator, base, tools, algorithms
import GAinitpop
import mlr3

def hash_ind_list(self):
    return hash(tuple(self))
def evalr2(ind):
    return mlr3.mlr(lls[ind],z)[2].astype(float),
def evalr2adj(ind):
    return mlr3.mlr(lls[ind],z)[3].astype(float),
def evalq2loo(ind):
    return mlr3.q2loo_mlr(lls[ind],z),

def mutRan(ind,indpb):
   # mutpool=[str(i) for i in ndesc.index if i not in ind]
    for descriptor in ind:
        if np.random.binomial(1,indpb,1)==1:
            ind[ind.index(descriptor)]=random.choice(ndesc.index)#[str(i) for i in ndesc.index if i not in ind])
            #np.random.choice(ind.remove(descriptor))
            #ind[np.random.choice(zeroindexes,1,replace=False)]=1
    return ind,
def makeind(table,size=5):
    GAinitpop.genind(table).random(size)


creator.create("Fitness", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.Fitness, __hash__=hash_ind_list)
toolbox=base.Toolbox() 
#fitness evaluation function
toolbox.register("evaluate", evalq2loo)
#specify variation operators
toolbox.register("mate", tools.cxOnePoint) #Uniform, indpb=0.5)
#toolbox.register("mutate", tools.mutFlipBit, indpb=.05)
toolbox.register("mutate", mutRan, indpb=.05)
#toolbox.register("select", tools.selTournament,k=1,tournsize=2)
toolbox.register("select", tools.selBest)

toolbox.register("genind", makeind,)

toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genind)
toolbox.register("population",tools.initRepeat, list, toolbox.individual, n=100)

population =toolbox.population()

fits=toolbox.map(toolbox.evaluate, population)
for fit, ind in zip(fits,population):
    ind.fitness.values=fit

import random
from itertools import groupby


from deap import algorithms
avgfitnesses=[]
for gen in range(100):
    offspring=algorithms.varOr(population, toolbox, lambda_=100, cxpb=.5, mutpb=.05)
#    offspring=algorithms.varAnd(population, toolbox, cxpb=.5, mutpb=.05)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
         ind.fitness.values=fit
    population=toolbox.select([k for k,v in groupby(sorted(offspring+population))], k=100)
    popfits = toolbox.map(toolbox.evaluate, population)
    avgfitnesses.append(numpy.mean(popfits))

