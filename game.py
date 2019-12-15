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

pygame.init()
pygame.display.set_caption("AI Car")
width = 1500
height = 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
ticks = 60
end = False
ppu = 32 # pixel per unit

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "car1.png")
track = pygame.image.load('track.png')

population_size=10
car_image = pygame.image.load(image_path) #car of length 2 and width 1
cars = []
for i in range(population_size):
    cars.append(car.Car(1,2+.1*i))
    
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
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
    
    key = pygame.key.get_pressed()
    if(key[pygame.K_ESCAPE]):
        end=True  
    screen.blit(track,[0,0])


    for i in range(len(cars)):

# =============================================================================
        # sensor
        inputNN=np.zeros(5) # 5 direction of detecting obstacles 
        pixels = Sensor(cars[i].position * ppu,cars[i].angle)
        try:
            for k in range(len(pixels)):
                for j in range(len(pixels[k])):
                    if(track.get_at(pixels[k][j]) == white):
                        inputNN[k] +=1/len(pixels[k]);
                    
        except IndexError as error:
            print("sensor out of screen")

# =============================================================================

        cars[i].steering = 0
        if key[pygame.K_RIGHT]:
            cars[i].steering -= 30 * dt
        elif key[pygame.K_LEFT]:
            cars[i].steering += 30 * dt
        elif(key[pygame.K_r]):
            cars[i].velocity = Vector2(3.0, 0.0)
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
                cars[i].velocity = Vector2(0.0, 0.0)
        except IndexError as error:
            cars[i].velocity = Vector2(0.0, 0.0)
# =============================================================================        
    
      
    
    pygame.display.flip()
    clock.tick(ticks)
    
pygame.display.quit()

pygame.quit()