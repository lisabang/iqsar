import random
import numpy as np



#arguments:  ngen, basetable, y, popsize, indsize, crossoverrate, #mutprob, evaluation function, selection function
toolbox=base.Toolbox()
def hash_ind_list(i):
    return hash(tuple(i))

class GAdescsel():
    def __init__(self,basetable,y,ngen=1000, popsize=100, indsize=5, cx=.5, mut=.05):
        from deap import creator, base, tools, algorithms
        creator.create("Fitness", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.Fitness, __hash__=hash_ind_list)
        #toolbox=base.Toolbox() 
        global toolbox
        #global evalq2loo
        self.basetable=basetable
        self.y=y
        self.ngen=ngen
        self.popsize=popsize
        self.indsize=indsize
        self.cx=cx
        self.mut=mut
#    def randstartpop(self):
        toolbox.register("genind", makeind,self.basetable, self.indsize)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.genind)
        toolbox.register("population",tools.initRepeat, list, toolbox.individual, n=self.popsize)
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
        smple=random.sample(self.basetable.columns,desc_in_ind)
        return smple
    def mutaRan(self,ind):
       # mutpool=[str(i) for i in ndesc.index if i not in ind]
        for descriptor in ind:
            if np.random.binomial(1,self.mut,1)==1:
                ind[ind.index(descriptor)]=random.choice(self.basetable.columns)
        return ind,
    def evalr2(self,ind):
        import mlr3
        return mlr3.mlr(self.basetable[ind],self.y)[2].astype(float),
    def evalr2adj(self,ind):
        import mlr3
        return mlr3.mlr(self.basetable[ind],self.y)[3].astype(float),
    def evalq2loo(self,ind):
        import mlr3
#        print self.basetable[ind][1]
        return mlr3.q2loo_mlr(self.basetable[ind],self.y),

    def evolve(self):#,evalfunc="q2loo"):
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
            
            population=toolbox.select([k for k,v in groupby(sorted(offspring+population))], k=100)
            popfits = toolbox.map(toolbox.evaluate, population)
            avgfitnesses.append(numpy.mean(popfits))
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
        
'''
            population=toolbox.select([k for k,v in groupby(sorted(offspring+population))], k=100)
            popfits = toolbox.map(toolbox.evaluate, population)
            avgfitnesses.append(numpy.mean(popfits))'''
  #  def by_r2adj():

  #  def by_q2loo():

#output: end population, descriptor frequency stats, average fitness
