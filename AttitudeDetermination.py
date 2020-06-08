import math
import numpy as np

#Mass in kg

#mass = 19.94 #[kg] For CATIA
mass = 24 #[kg]

#Dimensions of the 12U
width = 23.94204 * 10**(-2) #[m]
height = 22.91334 * 10**(-2) #[m]
depth = 36.3474 * 10**(-2) #[m]

#Moments of inertia, assuming is symmetric
I = np.array([[1/12*mass*(height**2+depth**2),0,0],   #Ixx
              [0,1/12*mass*(width**2+depth**2),0],    #Iyy
              [0,0,1/12*mass*(width**2+height**2)]])  #Izz

print("MOI (just structure): ",I)

##Moments of Inertia for 12U Cubesat with 2 solar panels attached in the width of the cubesat
#Moments of inertia with solar array

#mass_solarpanel = 0.69 #[kg] for CATIA
mass_solarpanel = 0.728 #[kg]
area_solarpanel = 0.23 #[m^2]
thickness_solarpanel = 3*10**(-3) #[m]
height_solarpanel = area_solarpanel/2/width

#Previous MOI
I_solarpanel = I+np.array([[1/12*mass_solarpanel*(height_solarpanel**2+thickness_solarpanel**2)+mass_solarpanel*((height_solarpanel/2+height/2)**2+(depth/2-thickness_solarpanel/2)**2),0,0],   #Ixx
              [0,1/12*mass_solarpanel*(width**2+thickness_solarpanel**2)+mass_solarpanel*((depth/2-thickness_solarpanel/2)**2),0],    #Iyy
              [0,0,1/12*mass_solarpanel*(width**2+height_solarpanel**2)+mass_solarpanel*(height_solarpanel/2+height/2)**2]])  #Izz

print("MOI including solar arrays: ",I_solarpanel)

#alpha around y
#beta around x

#Determine the time sum of two attitude manouvres
def AttitudeDeterminationTime(Ixx,Iyy,Izz,Torque,alpha,beta,gamma):
    time1 = math.sqrt(4*beta*Ixx/Torque)
    time2 = math.sqrt(4*alpha*Iyy/Torque)
    time3 = math.sqrt(4*gamma*Izz/Torque)
    time = time1 + time2 + time3
    return time

Ixx = I_solarpanel[0][0]
Iyy = I_solarpanel[1][1]
Izz = I_solarpanel[2][2]
Torque = 0.007 #[Nm]
alpha = np.pi/180*0 #[rad]
beta = np.pi/180*0 #[rad]
gamma = np.pi/180*180 #[rad]

print("Total Time: ",AttitudeDeterminationTime(Ixx,Iyy,Izz,Torque,alpha,beta,gamma))