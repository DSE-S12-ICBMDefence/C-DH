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
factorsize = 15*10**(-3) #[km]

#S/C1
lat1 = np.pi/4
lon1 = np.pi/6

yaw1 = 0
roll1 = np.pi/180*5
pitch1 = np.pi/180*10







#alpha1 = roll1+n[0] #x rotation
#beta1 = pitch1+n[1] #y rotation
#gamma1 = yaw1 #z rotation
