# Porous-environment

<p align="center"><img src="Picture/Introduction.png"></p align="center">

## Introduction

This program has been created to model the flow of water in a porous environment. Imagine a rock in which there are holes. The probability to have a hole is represented by p. Now, our goal is to determine if the water will pass through this rock or if the water will be stopped inside the rock.

To represent the rock, we have used an array with nxn cells. Holes are represented with a white cell, the rest with a black one.

## Representation
***init***

This function create an array with pxn² white cells (represented by a one). The rest are black cells (represented by a zero).

***remplissage***

This function takes the array of black and white cells created by init function and fills the white cells connected to the top of the array with blue. The blue represents flowing water and the water is propagated between the white cells with a common edge

***Exemple***

This is the representation with p=0.6

<p align="center"><img src="Picture/p=0,6 before.png"></p align="center">
<p align="center"><img src="Picture/p=0,6 after.png"></p align="center">


##  Water's probability to pass

***remplissage1***

This function is used to create the water flow probability curve. It is created like the remplissage function but instead of returning a filled array, it is returning a boolean (true if the water has passed, false otherwise).

***proba***
This function plots the water flow probabilty curve depending on the p, the probability of each cell to be white.

<p align="center"><img src="Picture/probability_curve.png"></p align="center">


## Occupation density

***remplissage2*** 

This function is adapted to calculate the blue cells number. It is usning the remplissage function but instead of returning the filled array, it is returning the blue cells number.

***densite*** 

Function that plots the occupation density depending on the probability p (probability to have a white cell)'''

<p align="center"><img src="Picture/density.png"></p align="center">
 
## Menu

There are three choices in the menu:

 1. The program plots the porous environment before and after the passage of the water 
 2. To see the water flow probability curve
 3. To see the curve of density's water occupation

