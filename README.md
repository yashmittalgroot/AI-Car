# AI car
This project is to apply AI to make autonomous car. The job of car is to finish the track without hitting the walls. Car is trained with the help of feedfordward Neural Network and Genetic Algorithm(with some modification).

## Libraries, Tools and Algorithms used
* Python3 
* Keras
* Pygame
* Spyder
* Paint
* PhotoShop
* Neural Network
* Genitic Algorithm

## Approach
 ![Car](car1.png "Car") ![NN](network.png "NN") ![Output](movement1.png "Car")
 
 We have designed a car which detect THE WALL with the help of sensors which can be seen in the above image. These sensor's data act as a input to the neural netuork and output of neural network provide direction to car. Now for Neural Network to work properly we need correct set of weights. Here come Genetic Algorithm in picture. Links are provided,in the end, of the sites and videos that inspired and helped us.
 
## Details of files in repo 

* car.py -	Class of car.
* car1.png -	Car image
* check_solution.py	- This file is to check a perticular set of neural weights. This take data(values of weights) from data.npy file.  
* data.npy	- File that store weights of the car that finished the track.
* game.py	- Normal game file to play with left and right arrow keys.
* geneticAlgoModified.py	- Genetic Algo class.
* genotype.py	- Genotype(gene) class.(Usual term used)
* main.py -	This is the file to run the code. Training is done in this file and if any car finishes the track than it store that particular set of weights in data.npy file.
* movement1.png -	Image used in documentation.
* network.png - Image used in documentation.
* nn.py	- neural network class. Although we used keras but need to create some functions.
* sensor.py	- Used to get pixel of each sensor.
* track.png - Track to train car.

## Problems we faced and solutions
* HyperParameters tuning - Probablity of mutation should not be high nor low.  
* Neural Network may not be perfect(number of layers and nodes and also activation functions)- Used relu and softmax function instead of sigmoid.  
* Velocity and turning angle of car - After some tuning we get right set of velocity and angle for a particular track.


## Issues
* Used fix set of colour for track.
* Sensor is at discrete locations, so will not get exact location of wall.
* Car not stable(Wobble too much).
* Sensor angle and range.

## Future Improvements
* Control velocity itself.
* Make car stable.
* Sensor should cover more angle for sharp turns.

## Useful Links
* [Deep Learning Cars(Unity based)](https://www.youtube.com/watch?v=Aut32pR5PQA)
* Fundamentals of the New Artificial Intelligence (Book chapter 4)

