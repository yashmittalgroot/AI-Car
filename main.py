# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:00:30 2019

@author: Yash Mittal
"""

import os
import pygame
import numpy as np
from pygame.math import Vector2
import nn
import car
import genotype 
from sensor import Sensor
import geneticAlgoModified as ga
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

pygame.init()
pygame.display.set_caption("AI Car")
width = 1500
height = 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font(None,24)
ticks = 60
end = False
ppu = 32 # pixel per unit
total_time = 0

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "car1.png")
track = pygame.image.load('track.png')

population_size=10
car_image = pygame.image.load(image_path) #car of length 2 and width 1
cars = []
nNet = []
flag = []
x=1
y=1.5
for i in range(population_size):
    flag.append(0)
    cars.append(car.Car(x,y))
    nNet.append(nn.nn([5,4,3,2]))
parameters_count = nNet[0].parameters_count
gAlgo=ga.GA(parameters_count,population_size)
for i in range(population_size):
    nNet[i].setParameters(gAlgo.currentPopulation[i].parameters)
    #gAlgo.currentPopulation[i].parameters = nNet[i].getParameters()
    
# =============================================================================
# code for collision
# checking both front corner
p1=Vector2(1.0, 0.5)*ppu
p2=Vector2(1.0, -0.5)*ppu
black=(0,0,0,255)
green=(0,255,0,255)
red=(255,0,0,255)
white=(255,255,255,255)
# =============================================================================

while not end:
    dt = clock.get_time() / 1000
    total_time += dt
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
    
    key = pygame.key.get_pressed()
    if(key[pygame.K_ESCAPE]):
        end=True  
    screen.blit(track,[0,0])

    all_stop = 0
    for i in range(len(cars)):
        if(cars[i].on == False):
            all_stop +=1
        # =============================================================================
        # sensor
        inputNN=np.zeros(5) # 5 direction of detecting obstacles 
        pixels = Sensor(cars[i].position * ppu,cars[i].angle)
        try:
            for k in range(len(pixels)):
                for j in range(len(pixels[k])):
                    if(track.get_at(pixels[k][j]) == white or track.get_at(pixels[k][j]) == red):
                        inputNN[k] +=1/len(pixels[k]);
                    
        except IndexError as error:
            q=1
        output=nNet[i].output(np.matrix(inputNN))
# =============================================================================
        #print(output.shape)
        cars[i].steering = 0
        if output[0][0]>output[0][1]:
            cars[i].steering -= 30 * dt
        else:
            cars[i].steering += 30 * dt
        cars[i].steering = max(-cars[i].max_steering, min(cars[i].steering, cars[i].max_steering))
        cars[i].update(dt)
       
        rotated = pygame.transform.rotate(car_image, cars[i].angle)
        rect = rotated.get_rect()
        screen.blit(rotated, cars[i].position * ppu - (rect.width / 2, rect.height / 2))
# =============================================================================
        try:
            p1_rotated= cars[i].position * ppu  + p1.rotate(-cars[i].angle)
            p2_rotated= cars[i].position * ppu  + p2.rotate(-cars[i].angle)
            temp1=(int(p1_rotated.x),int(p1_rotated.y))
            temp2=(int(p2_rotated.x),int(p2_rotated.y))
            if ((track.get_at(temp1) == black) or (track.get_at(temp2) == black)) :
                if(flag[i]==0):
                    flag[i]=1                   
                    gAlgo.currentPopulation[i].fitness = total_time
                cars[i].on = False
                cars[i].velocity = Vector2(0.0, 0.0)
            elif ((track.get_at(temp1) == red) or (track.get_at(temp2) == red)) :
                if(flag[i]==0):
                    flag[i]=1                   
                    gAlgo.currentPopulation[i].fitness = total_time
                cars[i].on = False
                cars[i].velocity = Vector2(0.0, 0.0)
                cars[i].is_finished = True
                print(i,nNet[i].getParameters())
                np.save("data",nNet[i].getParameters())
                end = True
                
        except IndexError as error:
            cars[i].velocity = Vector2(0.0, 0.0)
            cars[i].on = False
# =============================================================================    
    screen.blit(font.render(("Gen Count : %s " % gAlgo.GenCount),1,(250,250,250)),(1,300))
    if(all_stop == population_size):
        total_time = 0
        print(gAlgo.GenCount)
        gAlgo.GenCount += 1
        for i in range(population_size):
            print(gAlgo.currentPopulation[i].fitness)
        newPopulation = gAlgo.RecombinationOperator()
        newPopulation = gAlgo.MutationOperator(newPopulation)
        gAlgo.currentPopulation = newPopulation
        for i in range(population_size):
            #print(gAlgo.currentPopulation[i].fitness)
            flag[i]=0
            nNet[i].setParameters(gAlgo.currentPopulation[i].parameters)
            cars[i].reset(x,y)
      
    
    pygame.display.flip()
    clock.tick(ticks)
    
pygame.display.quit()

pygame.quit()