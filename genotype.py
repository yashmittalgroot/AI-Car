# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:27:56 2019

@author: Yash Mittal
"""
import numpy as np

class Genotype:
    
    def __init__(self,parameters_count,minValue,maxValue,fitness=0):
        self.parameters=np.random.random(parameters_count)*(maxValue-minValue)+minValue
        self.parameters_count = parameters_count
        self.fitness = fitness
        

    def update(self,parameters,fitness):
        self.parameters=parameters
        self.fitness=fitness
        
    