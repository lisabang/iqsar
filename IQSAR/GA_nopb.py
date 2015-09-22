
import random
import numpy as np
import itertools as itert
import copy as cp
from deap import creator, base, tools, algorithms
import functools
import sys
import signal
import time
import sys
import time
import mlr3 as m

def hash_ind_list(i):
    return hash(tuple(i))
randomnum=np.random.uniform(1,100,1)
#arguments:  ngen, basetable, y, popsize, indsize, crossoverrate, #mutprob, evaluation function, selection function
toolbox=base.Toolbox()
class GAdescsel():
    def __init__(self,basetable,y,ngen=1000, popsize=100, indsize=5, cx=.5, mut=.05, seed="12345"):
        from deap import creator, base, tools, algorithms
        creator.create("Fitness", base.Fitness, weights=(1.0,))
        
        creator.create("Individual", list, fitness=creator.Fitness, __hash__=hash_ind_list)
        creator.create("Population", list, fitness=creator.Fitness, __hash__=hash_ind_list)
        #toolbox=base.Toolbox() 
        global toolbox
        #global evalq2loo
        self.seed=seed
        self.basetable=basetable
        self.y=y
        self.ngen=ngen
        self.popsize=popsize
        self.indsize=indsize
        self.cx=cx
        self.mut=mut
    def ct_calls(func):
        @functools.wraps(func)
        def decor(*args, **kwargs):
            decor.count += 1
            return func(*args, **kwargs)
        decor.count = 0
        return decor
    def mkeindrand(self,desc_in_ind=5):#,datatable):
        import random
        while str(type(self.basetable)) !="<class 'pandas.core.frame.DataFrame'>":
            raise TypeError("The type of descriptor table should be a Pandas dataframe.")
        while type(desc_in_ind) is not int:
            try: 
                print "converting non-int to int"
                desc_in_ind=int(desc_in_ind)
                break
            except:
                raise ValueError("The number of descriptors per individual should be of type int")  
        smple=random.sample(self.basetable.columns,desc_in_ind)
        return smple
    @ct_calls
    def mkeindseed(self,desc_in_ind=5):
        import random
        from numpy.random import RandomState
        if self.mkeindseed.count<=100:
            prng=RandomState(self.seed+self.mkeindseed.count)
        if self.mkeindseed.count>100:
            prng=RandomState(self.seed+(self.mkeindseed.count%100))
        smple=prng.choice(self.basetable.columns,size=desc_in_ind, replace=False)
        return list(smple)
    def mutaRan(self,ind):
   # mutpool=[str(i) for i in ndesc.index if i not in ind]
        for descriptor in ind:
            if np.random.binomial(1,self.mut,1)==1:
                choices=[x for x in list(self.basetable.columns) if x not in ind]
                ind[ind.index(descriptor)]=random.choice(choices)
        return ind,
    def evalr2(self,ind):
        return m.mlr(self.basetable[ind],self.y)[2].astype(float),
    def evalr2adj(self,ind):
        return m.mlr(self.basetable[ind],self.y)[3].astype(float),
    def evalq2loo(self,ind):
        
        return m.q2loo_mlr(self.basetable[ind],self.y),

    def evalq2lmo(self,ind):
        def factors(n):    
            return list(set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))[1]
        #import mlr3
#        print self.basetable[ind][1]
        return m.q2lmo_mlr(self.basetable[ind],self.y, kfolds=factors(len(self.y))),
    def printq2fitness(self,pop):
        q2s=[]
        for ind in pop:
            q2s.append(IQSAR.mlr3.q2loo_mlr(self.basetable[ind],self.y))
        return q2s  
    def evolveparallel(self):
        from scoop import futures
        toolbox.register("genind", self.mkeind,self.indsize)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genind)
        toolbox.register("population",tools.initRepeat, list, toolbox.individual, n=self.popsize)

        toolbox.register("evaluate", self.evalr2)
        toolbox.register("mate", tools.cxOnePoint) #Uniform, indpb=0.5)
        toolbox.register("mutate", self.mutaRan)#, indpb=self.mut)
        toolbox.register("select", tools.selBest)
        population=toolbox.population()
        
        #print population
        fits=toolbox.map(toolbox.evaluate, population)

        for fit, ind in zip(fits,population):
            ind.fitness.values=fit
            #print fit, ind
            #print fit
        #offspring=algorithms.varOr(population, toolbox, lambda_=100, cxpb=.5, mutpb=.05)    
        #print toolbox.map(toolbox.evaluate, offspring)
        
        avgfitnesses=[]
        for gen in range(self.ngen):
            
            offspring=algorithms.varOr(population, toolbox, lambda_=self.popsize, cxpb=self.cx, mutpb=self.mut)   
            #print "offspring",offspring
            fits=futures.map(toolbox.evaluate, offspring)
            for fit, ind in zip(fits,population):
                ind.fitness.values=fit
            
#            for ind in offspring:
#                ind.fitness.values=toolbox.evaluate(ind)


            
            population=toolbox.select([k for k,v in itert.groupby(sorted(offspring+population))], k=100)
            popfits = futures.map(toolbox.evaluate, population)
            avgfitnesses.append(np.mean(popfits))
        #plot(len(avgfitnesses), list(avgfitnesses))
        #print avgfitnesses
        
    def evolvepara(self):
        #import multiprocessing
        #pool = multiprocessing.Pool()
        #toolbox.register("map", pool.map)
        toolbox.register("genind", self.mkeind,self.indsize)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genind)
        toolbox.register("population",tools.initRepeat, list, toolbox.individual, n=self.popsize)

        toolbox.register("evaluate", self.evalr2)
        toolbox.register("mate", tools.cxOnePoint) #Uniform, indpb=0.5)
        toolbox.register("mutate", self.mutaRan)#, indpb=self.mut)
        toolbox.register("select", tools.selBest)
        population=toolbox.population()
        #print population
        fits=toolbox.map(toolbox.evaluate, population)

        for fit, ind in zip(fits,population):
            ind.fitness.values=fit
            #print fit, ind
            #print fit
        #offspring=algorithms.varOr(population, toolbox, lambda_=100, cxpb=.5, mutpb=.05)    
        #print toolbox.map(toolbox.evaluate, offspring)
        
        avgfitnesses=[]
        for gen in range(self.ngen):
            
            offspring=algorithms.varOr(population, toolbox, lambda_=self.popsize, cxpb=self.cx, mutpb=self.mut)   
            #print "offspring",offspring
            #fits=toolbox.map(toolbox.evaluate, offspring)
            for ind in offspring:
                ind.fitness.values=toolbox.evaluate(ind)
            #for fit, ind in zip(fits,population):
            #    ind.fitness.values=fit
            
            population=toolbox.select([k for k,v in itert.groupby(sorted(offspring+population))], k=100)
            popfits = toolbox.map(toolbox.evaluate, population)
            avgfitnesses.append(np.mean(popfits))
        #plot(len(avgfitnesses), list(avgfitnesses))
#        print avgfitnesses
        print toolbox.map(toolbox.evaluate, population)
        return population


    def evolve(self,evalfunc="q2loo",startpop=None):
     
        toolbox.register("genind", self.mkeindseed, self.indsize)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genind)
        toolbox.register("population",tools.initRepeat, list, toolbox.individual, n=self.popsize)
        
        if evalfunc=="q2loo":
            toolbox.register("evaluate", self.evalq2loo)

        elif evalfunc=="q2lmo":
            toolbox.register("evaluate", self.evalq2lmo)
        elif evalfunc=="r2":
            toolbox.register("evaluate", self.evalr2)
        elif evalfunc=="r2adj":
            toolbox.register("evaluate", self.evalr2adj)
        else:
            raise ValueError("not a valid evaluation function specified; use evalr2adj, evalr2, q2lmo, or q2loo")
        
        toolbox.register("mate", tools.cxOnePoint) #Uniform, indpb=0.5)
        toolbox.register("mutate", self.mutaRan)#, indpb=self.mut)
        toolbox.register("select", tools.selBest)
        if startpop==None:
             origpop=toolbox.population()
        else:
             origpop=startpop
        #self.mkeindseed.count=0
        population=cp.deepcopy(origpop)
        fits=toolbox.map(toolbox.evaluate, population)
        for fit, ind in zip(fits,population):
            ind.fitness.values=fit
        
        avgfitnesses=[]
        popfits=0
        for gen in range(self.ngen):
            try:
                offspring=algorithms.varOr(population, toolbox, lambda_=self.popsize, cxpb=self.cx, mutpb=self.mut)   
                for ind in offspring:
                    ind.fitness.values=toolbox.evaluate(ind)
                population=toolbox.select([k for k,v in itert.groupby(sorted(offspring+population))], k=100)
                popfits = toolbox.map(toolbox.evaluate, population)
            except (KeyboardInterrupt, SystemExit):
                return [origpop, toolbox.map(toolbox.evaluate, origpop), population, toolbox.map(toolbox.evaluate, population)]
            except:
                return [origpop, toolbox.map(toolbox.evaluate, origpop), population, toolbox.map(toolbox.evaluate, population)]

        return [origpop, toolbox.map(toolbox.evaluate, origpop), population, toolbox.map(toolbox.evaluate, population)]
        print "Done!"
            
    def evolverf(self,evalfunc="q2loo"):
        #toolbox.register("map", pool.map)
        toolbox.register("genind", self.mkeindrf,self.indsize)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genind)
        toolbox.register("population",tools.initRepeat, list, toolbox.individual, n=self.popsize)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genind)
        toolbox.register("population",tools.initRepeat, list, toolbox.individual, n=self.popsize)
        if evalfunc=="q2loo":
            toolbox.register("evaluate", self.evalq2loo)
        elif evalfunc=="r2":
            toolbox.register("evaluate", self.evalr2)
        elif evalfunc=="r2adj":
            toolbox.register("evaluate", self.evalr2adj)
        else:
            raise ValueError("not a valid evaluation function specified; use evalr2adj, evalr2, or q2loo")
        
        toolbox.register("mate", tools.cxOnePoint) #Uniform, indpb=0.5)
        toolbox.register("mutate", self.mutaRan)#, indpb=self.mut)
        toolbox.register("select", tools.selBest)
        population=toolbox.population()
        #print population
        fits=toolbox.map(toolbox.evaluate, population)

        for fit, ind in zip(fits,population):
            ind.fitness.values=fit
        
        avgfitnesses=[]
        for gen in range(self.ngen):
            
            offspring=algorithms.varOr(population, toolbox, lambda_=self.popsize, cxpb=self.cx, mutpb=self.mut)   
            for ind in offspring:
                ind.fitness.values=toolbox.evaluate(ind)
            
            population=toolbox.select([k for k,v in itert.groupby(sorted(offspring+population))], k=100)
            popfits = toolbox.map(toolbox.evaluate, population)
            avgfitnesses.append(np.mean(popfits))
        return population
            
    def evolverecur(self, rf=False,pops=10):
        totalpop=[]
        origpops=[]
        if rf==False:
            for n in range(pops):
            #feedpop[n]=self.evolve()
                subpop=self.evolve()
                origpop=subpop[0]
                origpops.append(origpop)
                meh=subpop[2]
                for ind in meh:
                    totalpop.append(ind)
        elif rf==True:
            
            for n in range(pops):
            #feedpop[n]=self.evolve()
                meh=self.evolverf()
                for ind in meh:
                    totalpop.append(ind)
        else:
            raise TypeError("Random Forest (rf) arg must be a boolean, True or False")
                
        #print totalpop
        toolbox.register("evaluate", self.evalq2loo)
        toolbox.register("select", tools.selBest)
        for ind in totalpop:
            ind.fitness.values=toolbox.evaluate(ind)
        population=toolbox.select([k for k,v in itert.groupby(sorted(totalpop))], k=100)
        return [origpops, population, toolbox.map(toolbox.evaluate, population)]
    #zip(fits,population)
    def debug_eval(self):
        toolbox.register("evaluate", evalr2, self.y, self.basetable)
        toolbox.register("mate", tools.cxOnePoint) #Uniform, indpb=0.5)
        toolbox.register("mutate", mutRan, indpb=self.mut)
        toolbox.register("select", tools.selBest)
        population=toolbox.population()
        fits=toolbox.map(toolbox.evaluate, population)

        for fit, ind in zip(fits,population):
            ind.fitness.values=fit
        offspring=algorithms.varOr(population, toolbox, lambda_=100, cxpb=.5, mutpb=.05)   
            #print "offspring",offspring
            #fits=toolbox.map(toolbox.evaluate, offspring)
        print offspring
        for ind in offspring:
            ind.fitness.values=toolbox.evaluate(ind)
            print ind
            print ind.fitness.values
            #for fit, ind in zip(fits,population):
            #    ind.fitness.values=fit
        

  #  def by_r2adj():
  #  def by_q2loo():

#output: end population, descriptor frequency stats, average fitnes
