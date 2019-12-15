import pygame
from pygame.math import Vector2
''' 
Total sensor are 30, distributed in 5 direction(6 sensor in each direction)
Direction 1 -Start with pixcel position 130,62 and next sensor is 8,-8 pixcel away and so on
Direction 2 -Start with pixcel position 132,70 and next sensor is 10,-5 pixcel away and so on
Direction 3 -Start with pixcel position 135,80 and next sensor is 10,0 pixcel away and so on
Direction 4 -Start with pixcel position 132,90 and next sensor is 10,5 pixcel away and so on
Direction 5 -Start with pixcel position 130,98 and next sensor is 8,8 pixcel away and so on
centre of car is at 96,80
'''
def Sensor(car_pos,car_angle):
    start_pix=[Vector2(130,62),Vector2(132,70),Vector2(135,80),Vector2(132,90),Vector2(130,98)]
    change_pix=[Vector2(8,-8),Vector2(10,-5),Vector2(10,0),Vector2(10,5),Vector2(8,8)]
    car_centre_pos=Vector2(96,80)
    d=[[],[],[],[],[]]
    for i in range(len(d)):
        for j in range(6):
            d[i].append(start_pix[i]+j*change_pix[i] - car_centre_pos)
            d[i][j]=d[i][j].rotate(-car_angle) + car_pos       
            d[i][j] = (int(d[i][j].x),int(d[i][j].y))
    return d


# =============================================================================
# d=Sensor(Vector2(96,80),10)
# print(d)
# 
# =============================================================================
