# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 15:31:26 2019

@author: yash mittal
"""
# Code for checking parameters
import os
import pygame
import numpy as np
from pygame.math import Vector2
import nn
import car
from sensor import Sensor
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

population_size=1
car_image = pygame.image.load(image_path) #car of length 2 and width 1
x=1
y=1.5
cars = car.Car(x,y)
nNet = nn.nn([5,4,3,2])
parameters_count = nNet.parameters_count
parameters=np.load("data.npy")
nNet.setParameters(parameters)
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

        # =============================================================================
        # sensor
    inputNN=np.zeros(5) # 5 direction of detecting obstacles 
    pixels = Sensor(cars.position * ppu,cars.angle)
    try:
        for k in range(len(pixels)):
            for j in range(len(pixels[k])):
                if(track.get_at(pixels[k][j]) == white or track.get_at(pixels[k][j]) == red):
                    inputNN[k] +=1/len(pixels[k]);
                else:
                    break   
    except IndexError as error:
        q=1
    output=nNet.output(np.matrix(inputNN))
# =============================================================================
        #print(output.shape)
    cars.steering = 0
    if output[0][0]>output[0][1]:
        cars.steering -= 30 * dt
    else:
        cars.steering += 30 * dt
    cars.steering = max(-cars.max_steering, min(cars.steering, cars.max_steering))
    cars.update(dt)
       
    rotated = pygame.transform.rotate(car_image, cars.angle)
    rect = rotated.get_rect()
    screen.blit(rotated, cars.position * ppu - (rect.width / 2, rect.height / 2))
# =============================================================================
    try:
        p1_rotated= cars.position * ppu  + p1.rotate(-cars.angle)
        p2_rotated= cars.position * ppu  + p2.rotate(-cars.angle)
        temp1=(int(p1_rotated.x),int(p1_rotated.y))
        temp2=(int(p2_rotated.x),int(p2_rotated.y))
        if ((track.get_at(temp1) == black) or (track.get_at(temp2) == black)) :                  
            cars.on = False
            cars.velocity = Vector2(0.0, 0.0)
        elif ((track.get_at(temp1) == red) or (track.get_at(temp2) == red)) :                  
            cars.on = False
            cars.velocity = Vector2(0.0, 0.0)
            cars.is_finished = True
            print(nNet.getParameters())
            end = True
                
    except IndexError as error:
        cars.velocity = Vector2(0.0, 0.0)
        cars.on = False
# =============================================================================    
      
    
    pygame.display.flip()
    clock.tick(ticks)
    
pygame.display.quit()

pygame.quit()

