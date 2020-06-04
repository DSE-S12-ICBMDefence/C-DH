import math
import numpy as np

mass = 24 #[kg]
width = 23.94204 * 10**(-2) #[m]
height = 36.3474 * 10**(-2) #[m]
depth = 22.91334 * 10**(-2) #[m]

#Moments of inertia, assuming is symmetric
I = np.array([[1/12*mass*(height**2+depth**2),0,0],
              [0,1/12*mass*(width**2+depth**2),0],
              [0,0,1/12*mass*(width**2+height**2)]])

print(I)