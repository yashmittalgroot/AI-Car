# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 13:10:53 2019

@author: Yash Mittal

"""
import numpy as np
import genotype 

class GA:
    def __init__(self,parameters_count,population_size):
        #genes
        self.parameters_count=parameters_count
        #population
        self.population_size=population_size
        #min value of inital population parameters.
        self.minValue = -3.0
        #max value of initial population parameters.
        self.maxValue = 3.0
        #probability of a parameter being swapped during crossover.
        self.CrossSwapProb = .6
        #probability of a parameter being mutated.
        self.MutationProb = 0.4
        #amount by which parameters may be mutated.
        self.MutationAmount = 2.0
        #percent of genotypes in a new population that are mutated
        self.MutationPerc = 0.8
        
        self.currentPopulation = []
        for i in range (population_size):
            self.currentPopulation.append(genotype.Genotype(parameters_count,self.minValue,self.maxValue))
           
        self.GenCount = 1
        self.Running = False
        
     
    
    def crossover(self,parent1,parent2):
        n=self.parameters_count
        para1=np.zeros(n)
        para2=np.zeros(n)
        CrossSwapProb=self.CrossSwapProb
        ppara1=parent1.parameters
        ppara2=parent2.parameters
        offspring1 = genotype.Genotype(n,self.minValue,self.maxValue)
        offspring2 = genotype.Genotype(n,self.minValue,self.maxValue)
        for i in range(n):
            if np.random.random() < CrossSwapProb :
                para1[i]=ppara2[i]
                para2[i]=ppara1[i]
            else:
                para1[i]=ppara1[i]
                para2[i]=ppara2[i]
        offspring1.update(para1,0)
        offspring2.update(para2,0)
        return offspring1, offspring2
        
    def MutateGenotype(self,genotype):
        for  i in range (genotype.parameters_count) :
            if np.random.random() < self.MutationProb :
                genotype.parameters[i] += np.random.random()*(self.MutationAmount*2) - self.MutationAmount 
        return genotype

            
    def findBestTwo(self):
        temp=self.currentPopulation
        if(temp[0].fitness<temp[1].fitness):
            best1=temp[1]
            best2=temp[0]
        else:
            best1=temp[1]
            best2=temp[0]
        for i in range(2,self.population_size):
            if(temp[i].fitness >= best1.fitness):
                best1=temp[i]
                best2=best1
            elif(temp[i].fitness > best2.fitness):
                best2=temp[i]
            
        return [best1,best2]
    
    def RecombinationOperator(self):
        n=self.population_size
        intermediatePopulation = self.findBestTwo()
        newPopulation = []
        
        while (len(newPopulation) < n):
            
            offspring1, offspring2 =  self.crossover(intermediatePopulation[0], intermediatePopulation[1])
            newPopulation.append(offspring1)
            if (len(newPopulation) < n):
                newPopulation.append(offspring2)

        return newPopulation
    
    def MutationOperator(self,newPopulation):
        n = self.population_size
        for i in range (n):
            if (np.random.random() < self.MutationPerc):
                newPopulation[i] = self.MutateGenotype(newPopulation[i])
        return newPopulation
        
    
