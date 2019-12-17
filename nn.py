# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 15:11:37 2019

@author: Yash Mittal
"""
import numpy as np
from keras.models import Sequential
from keras.layers import Dense


class nn:
    def __init__(self,layerNodes=[5,4,3,2]):
        self.layerNodes=np.array(layerNodes)
        self.model = Sequential()
        self.model.add(Dense(self.layerNodes[1], input_dim=self.layerNodes[0], activation='relu'))
        for i in range(2,len(self.layerNodes)-1):
            self.model.add(Dense(self.layerNodes[i], activation='relu'))
        self.model.add(Dense(self.layerNodes[3], activation='softmax'))
        self.parameters_count = np.sum(self.layerNodes) - self.layerNodes[0] 
        for i in range(len(self.layerNodes)-1):
            self.parameters_count += self.layerNodes[i]*self.layerNodes[i+1]
        
    def setParameters(self,parameters):
        ind=[0]
        x=[]
        for i in range (len(self.layerNodes)-1):
            x.append(self.layerNodes[i]*self.layerNodes[i+1]+self.layerNodes[i+1])
            ind.append(sum(x))
        i=0
        a=self.layerNodes
        for layer in self.model.layers:
            l=[]
            l.append(parameters[ind[i]:ind[i+1]-a[i+1]].reshape(a[i],a[i+1]))
            l.append(parameters[ind[i+1]-a[i+1]:ind[i+1]])
            layer.set_weights(l)
            i+=1
            
    def getParameters(self):
        parameters=[]
        for layer in self.model.layers:
            weights = layer.get_weights()
            parameters.append(np.concatenate([weights[0].flatten(),weights[1]]))
        return np.concatenate(parameters)
    
    def output(self,data):
        return self.model.predict(data)
