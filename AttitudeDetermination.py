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
def AttitudeDeterminationTime(Ixx,Iyy,Izz,Torque,Momentum,alpha,beta,gamma):
    time1 = math.sqrt(4*alpha*Ixx/Torque)
    time2 = math.sqrt(4*beta*Iyy/Torque)
    time3 = math.sqrt(4*gamma*Izz/Torque)

    if Momentum/Ixx>Torque/(2*Ixx)*time1:
        velocity1 = Torque/(2*Ixx)*time1
    else:
        accelaration1 = Torque/Ixx
        velocity1 = Momentum/Ixx
        time1_triangle = velocity1/accelaration1
        time1_rectangle = (alpha-time1_triangle/2*velocity1)/velocity1
        time1 = time1_triangle+time1_rectangle

    if Momentum/Iyy>Torque/(2*Iyy)*time2:
        velocity2 = Torque/(2*Iyy)*time2
    else:
        accelaration2 = Torque/Iyy
        velocity2 = Momentum/Iyy
        time2_triangle = velocity2/accelaration2
        time2_rectangle = (beta-time2_triangle/2*velocity2)/velocity2
        time2 = time2_triangle+time2_rectangle

    if Momentum/Izz>Torque/(2*Izz)*time3:
        time3 = math.sqrt(4*gamma*Izz/Torque)
        velocity3 = Torque/(2*Izz)*time3
    else:
        accelaration3 = Torque/Izz
        velocity3 = Momentum/Izz
        time3_triangle = velocity3/accelaration3
        time3_rectangle = (gamma-time3_triangle/2*velocity3)/velocity3
        time3 = time3_triangle+time3_rectangle
        
    time = time1 + time2 + time3
    maxradialvelocity = max(velocity1,velocity2,velocity3)
    return time, maxradialvelocity

Ixx = I_solarpanel[0][0]
Iyy = I_solarpanel[1][1]
Izz = I_solarpanel[2][2]
Momentum = 0.1 #[Nms]
Torque = 0.007 #[Nm]
alpha = np.pi/180*0 #[rad]
beta = np.pi/180*0 #[rad]
gamma = np.pi/180*360 #[rad]

print("Total Time: ",AttitudeDeterminationTime(Ixx,Iyy,Izz,Torque,Momentum,alpha,beta,gamma)[0]," [s]")
print("Maximum Radial Velocity: ",AttitudeDeterminationTime(Ixx,Iyy,Izz,Torque,Momentum,alpha,beta,gamma)[1]*180/np.pi," [deg/s]")