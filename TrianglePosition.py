import numpy as np
import math
from Transformation import *
#hello
'''
INPUTS:
Spacecraft 1 (S/C1)
Attitude: yaw1, roll1, pitch1 [rad] #z,x,y
Position: x1. y1. z1 [km]
Bright pixel: n [pixel position]

Spacecraft 2 (S/C2)
Attitude: yaw2, roll2, pitch2 
Position: x2, y2, z2
Bright pixel: m

OUTPUTS:
Position: xp, yp, zp
'''

#Inputs for FOCUS
h = 500 #[km]
Re = 6378 #[km]
radius = Re+h
factorsize = 15*10**(-3) #[km]

#S/C1
lat1 = np.pi/4
lon1 = np.pi/6

spacecraftlocation1 = radius*np.array([np.cos(lon1)*np.cos(lat1),np.sin(lon1)*np.cos(lat1),np.sin(lat1)])

yaw1 = 0
roll1 = np.pi/180*5
pitch1 = np.pi/180*10

alpha1,beta1 = [np.pi/3,np.pi/4]
vector1 = np.array([np.sin(alpha1)*np.cos(beta1),np.sin(alpha1)*np.sin(beta1),np.cos(beta1)])

#S/C2
lat2 = np.pi/4
lon2 = np.pi/6

yaw2 = 0
roll2 = np.pi/180*5
pitch2 = np.pi/180*10

alpha2,beta2 = [np.pi/3,np.pi/4]
vector2 = np.array([np.sin(alpha2)*np.cos(beta2),np.sin(alpha2)*np.sin(beta2),np.cos(beta2)])

#alpha1 = roll1+n[0] #x rotation
#beta1 = pitch1+n[1] #y rotation
#gamma1 = yaw1 #z rotation
