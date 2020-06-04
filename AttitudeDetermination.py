import math
import numpy as np

#Mass in kg
mass = 24 #[kg]

#Dimensions of the 12U
width = 23.94204 * 10**(-2) #[m]
height = 36.3474 * 10**(-2) #[m]
depth = 22.91334 * 10**(-2) #[m]

#Moments of inertia, assuming is symmetric
I = np.array([[1/12*mass*(height**2+depth**2),0,0],   #Ixx
              [0,1/12*mass*(width**2+depth**2),0],    #Iyy
              [0,0,1/12*mass*(width**2+height**2)]])  #Izz

#alpha around y
#beta around x

def AttitudeDeterminationTime(Ixx,Iyy,Torque,alpha,beta):
    time1 = math.sqrt(4*beta*Ixx/Torque)
    time2 = math.sqrt(4*alpha*Iyy/Torque)
    time = time1 + time2
    return time

Ixx = I[0][0]
Iyy = I[1][1]
Torque = 0.25 #[Nm]
alpha = np.pi/180*20 #[rad]
beta = np.pi/180*20 #[rad]

print(AttitudeDeterminationTime(Ixx,Iyy,Torque,alpha,beta))