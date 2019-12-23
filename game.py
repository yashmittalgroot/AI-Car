"""
Created on Tue Dec 10 13:00:30 2019

@author: Yash Mittal
"""

import os
import pygame
from pygame.math import Vector2
import car 

# setting up pygame environment
pygame.init()
pygame.display.set_caption("AI Car")
width = 1500
height = 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
ticks = 60
end = False
ppu = 32 # pixel per unit

# Loading image of track and car
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "car1.png")
track = pygame.image.load('track.png')
car_image = pygame.image.load(image_path) #car of length 2 and width 1

# Initialization of car location, car and Neural Network 
x=1
y=1.5
car = car.Car(x,y)
    
# Code for collision
# Checking only front corners of car 
p1=Vector2(1.0, 0.5)*ppu #vector to top front cornor from centre
p2=Vector2(1.0, -0.5)*ppu #vector to bottom front cornor from centre
# colours used in track
black=(0,0,0,255)
green=(0,255,0,255)
red=(255,0,0,255)
white=(255,255,255,255)


#Game Loop
while not end:
    dt = clock.get_time() / 1000
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
    
    key = pygame.key.get_pressed()
    if(key[pygame.K_ESCAPE]):
        end=True  
    screen.blit(track,[0,0])

    car.steering = 0
    if key[pygame.K_RIGHT]:
        car.steering -= 30 * dt
    elif key[pygame.K_LEFT]:
        car.steering += 30 * dt
    elif(key[pygame.K_r]):
        car.on = True
        car.velocity = Vector2(3.0, 0.0)
    car.steering = max(-car.max_steering, min(car.steering, car.max_steering))
    car.update(dt)
    
    rotated = pygame.transform.rotate(car_image, car.angle)
    rect = rotated.get_rect()
    screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))

# =============================================================================
    # Checking whether car is on track or not or finished the track
    try:
        p1_rotated= car.position * ppu  + p1.rotate(-car.angle)
        p2_rotated= car.position * ppu  + p2.rotate(-car.angle)
        temp1=(int(p1_rotated.x),int(p1_rotated.y))
        temp2=(int(p2_rotated.x),int(p2_rotated.y))
        if ((track.get_at(temp1) == black) or (track.get_at(temp2) == black)) :                  
            car.on = False
            car.velocity = Vector2(0.0, 0.0)
        elif ((track.get_at(temp1) == red) or (track.get_at(temp2) == red)) :                  
            car.on = False
            car.velocity = Vector2(0.0, 0.0)
            car.is_finished = True
            end = True
                
    except IndexError as error:
        car.velocity = Vector2(0.0, 0.0)
        car.on = False
# =============================================================================         

    pygame.display.flip()
    clock.tick(ticks)
    
pygame.display.quit()

pygame.quit()



