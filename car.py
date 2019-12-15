"""
Created on Tue Dec 10 10:38:46 2019

@author: Yash Mittal
"""

from pygame.math import Vector2
import numpy as np

class Car:
    def __init__(self,x,y,angle=0.0,velocity = Vector2(3.0, 0.0),ppu=32,length=2,max_steering=30) :
        self.position = Vector2(x, y)
        self.velocity = velocity
        self.angle =  angle
        self.length = length
        self.max_steering = max_steering
        self.steering = 0.0
        self.ppu=ppu
        self.on=True
        self.is_finished=False
        self.velocity = self.velocity.rotate(-self.angle)

    def update(self, dt):
        if self.on:
            if self.steering:
                if(self.steering>0):
                    self.angle+=2
                elif(self.steering<0):
                    self.angle-=2
            self.position += self.velocity.rotate(-self.angle) * dt 
        
    def reset(self,x,y,angle=0.0,velocity= Vector2(3.0, 0.0)):
        self.position = Vector2(x, y)
        self.velocity = velocity
        self.angle =  angle
        self.steering = 0.0
        self.on=True
        self.velocity = self.velocity.rotate(-self.angle)