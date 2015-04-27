import random
import numpy as np
import itertools as itert
import copy as cp
from deap import creator, base, tools, algorithms
def hash_ind_list(i):
    return hash(tuple(i))
randomnum=np.random.uniform(1,100,1)
#arguments:  ngen, basetable, y, popsize, indsize, crossoverrate, #mutprob, evaluation function, selection function
toolbox=base.Toolbox()
class GAdescsel():
    def __init__(self,basetable,y,ngen=1000, popsize=100, indsize=5, cx=.5, mut=.05, seed=randomnum):
        from deap import creator, base, tools, algorithms
        creator.create("Fitness", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.Fitness, __hash__=hash_ind_list)
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
#    def randstartpop(self):
      #  toolbox.register("genind", makeind,self.basetable, self.indsize)
      #  toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genind)
      #  toolbox.register("population",tools.initRepeat, list, toolbox.individual, n=self.popsize)
        #self.population=toolbox.population()
    def mkeind(self,desc_in_ind=5):#,datatable):
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
        #this is what's used to generate the start population
        np.random.seed(seed=self.seed)
        smple=np.random.choice(self.basetable.columns,size=desc_in_ind, replace=False)
        #smple=random.sample(self.basetable.columns,desc_in_ind)
        return smple
    def mkeindrf(self,desc_in_ind=5):
        from sklearn import datasets
        from sklearn import metrics
        from sklearn.ensemble import RandomForestClassifier
        # load the iris datasets
        # fit an Extra Trees model to the data
        model=RandomForestClassifier()
        #model = ExtraTreesClassifier()
        model.fit(self.basetable, self.y)
        # the relative importance of each attribute
        rf_feats=pd.DataFrame(model.feature_importances_, index=self.basetable.columns)#!!!FITABLE!!??
        #print rf_feats
        pos=rf_feats[0].to_dict()
        return list(np.random.choice(list(pos.keys()), desc_in_ind, p=list(pos.values())))
    def mkeindlogrf(self,desc_in_ind=5):
        from sklearn import datasets
        from sklearn import metrics
        from sklearn.ensemble import RandomForestClassifier
        import math
        # load the iris datasets
        # fit an Extra Trees model to the data
        model=RandomForestClassifier()
        #model = ExtraTreesClassifier()
        model.fit(self.basetable, self.y)
        # the relative importance of each attribute
        rf_feats=pd.DataFrame(model.feature_importances_, index=self.basetable.index)#!!!FITABLE!!??
        #print rf_feats
        pos=rf_feats[0].to_dict()
        import math
        for key, value in pos.items():
            # do something with value
            pos[key] = math.exp(value)
        print pos
        return list(np.random.choice(list(pos.keys()), desc_in_ind, p=list(math.exp(pos.values()))))
        print list(np.random.choice(list(pos.keys()), desc_in_ind, p=list(math.exp(pos.values()))))
    def mutaRan(self,ind):
   # mutpool=[str(i) for i in ndesc.index if i not in ind]
        for descriptor in ind:
            if np.random.binomial(1,self.mut,1)==1:
                choices=[x for x in list(self.basetable.columns) if x not in ind]
                ind[ind.index(descriptor)]=random.choice(choices)
        return ind,
    def evalr2(self,ind):
        import mlr3 as m
        return m.mlr(self.basetable[ind],self.y)[2].astype(float),
    def evalr2adj(self,ind):
        import mlr3 as m
        return m.mlr(self.basetable[ind],self.y)[3].astype(float),
    def evalq2loo(self,ind):
        #import mlr3
#        print self.basetable[ind][1]
        import mlr3 as m
        return m.q2loo_mlr(self.basetable[ind],self.y),
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
        print avgfitnesses
        return population
            #print toolbox.map(toolbox.evaluate, offspring)
            #print ofits
#            fits = toolbox.map(toolbox.evaluate, offspring)
#            print fits
            
          #  for fit, ind in zip(ofits, offspring):
          #      ind.fitness.values=fit
          #      print fit
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
    def evolve(self,evalfunc="q2loo"):
        #toolbox.register("map", pool.map)
        toolbox.register("genind", self.mkeind,self.indsize)
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

        origpop=toolbox.population()
        population=cp.deepcopy(origpop)
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
            #avgfitnesses.append(np.mean(popfits))

        #plot(len(avgfitnesses), list(avgfitnesses))
#        print avgfitnesses
        #print toolbox.map(toolbox.evaluate, population)
        return [origpop, toolbox.map(toolbox.evaluate, origpop), population, toolbox.map(toolbox.evaluate, population)]
            #print toolbox.map(toolbox.evaluate, offspring)
            #print ofits
#            fits = toolbox.map(toolbox.evaluate, offspring)
#            print fits
            
          #  for fit, ind in zip(ofits, offspring):
          #      ind.fitness.values=fit
          #      print fit
            
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
        #print toolbox.map(toolbox.evaluate, population)
        return population
            #print toolbox.map(toolbox.evaluate, offspring)
            #print ofits
#            fits = toolbox.map(toolbox.evaluate, offspring)
#            print fits
            
          #  for fit, ind in zip(ofits, offspring):
          #      ind.fitness.values=fit
          #      print fit
            
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
        #print feedpop
        #totalpop=[]
        #for pop in feedpop:
        #    totalpop.append(pop.items)
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

#output: end population, descriptor frequency stats, average fitness
