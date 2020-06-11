import math
import numpy as np
import matplotlib.pyplot as plt

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

#Determine the time sum of two attitude manouvres
def AttitudeDeterminationTime(Ixx,Iyy,Izz,Torque,Momentum,alpha,beta,gamma):
    time1 = math.sqrt(4*alpha*Ixx/Torque)
    time2 = math.sqrt(4*beta*Iyy/Torque)
    time3 = math.sqrt(4*gamma*Izz/Torque)

    plt.figure(1)
    plt.title("X-Axis")
    plt.xlabel("Time [s]")
    plt.ylabel("Angular Velocity [rad/s]")
    if Momentum/Ixx>Torque/(2*Ixx)*time1:
        velocity1 = Torque/(2*Ixx)*time1
        plt.plot([0,time1/2,time1],[0,velocity1,0],'r-')
        print("Time1: {0}[s] & Velocity1: {1}[deg/s]".format(time1,velocity1*180/np.pi))
    else:
        accelaration1 = Torque/Ixx
        velocity1 = Momentum/Ixx
        time1_triangle = velocity1/accelaration1
        time1_rectangle = (alpha-time1_triangle*velocity1)/velocity1
        time1 = 2*time1_triangle+time1_rectangle
        plt.plot([0,time1_triangle,time1_triangle+time1_rectangle,time1],[0,velocity1,velocity1,0],'b-')
        print("Time1: {0}[s] & Velocity1: {1}[deg/s]".format(time1, velocity1*180/np.pi))

    plt.figure(2)
    plt.title("Y-Axis")
    plt.xlabel("Time [s]")
    plt.ylabel("Angular Velocity [rad/s]")
    if Momentum/Iyy>Torque/(2*Iyy)*time2:
        velocity2 = Torque/(2*Iyy)*time2
        plt.plot([0, time2 / 2, time2], [0, velocity2, 0], 'r-')
        print("Time2: {0}[s] & Velocity2: {1}[deg/s]".format(time2, velocity2 * 180 / np.pi))
    else:
        accelaration2 = Torque/Iyy
        velocity2 = Momentum/Iyy
        time2_triangle = velocity2/accelaration2
        time2_rectangle = (beta-time2_triangle/velocity2)/velocity2
        time2 = 2*time2_triangle+time2_rectangle
        plt.plot([0,time2_triangle,time2_triangle+time2_rectangle,time2],[0,velocity2,velocity2,0],'b-')
        print("Time2: {0}[s] & Velocity2: {1}[deg/s]".format(time2, velocity2 * 180 / np.pi))

    plt.figure(3)
    plt.title("Z-Axis")
    plt.xlabel("Time [s]")
    plt.ylabel("Angular Velocity [rad/s]")
    if Momentum/Izz>Torque/(2*Izz)*time3:
        time3 = math.sqrt(4*gamma*Izz/Torque)
        velocity3 = Torque/(2*Izz)*time3
        plt.plot([0, time3 / 2, time3], [0, velocity3, 0], 'r-')
        print("Time3: {0}[s] & Velocity3: {1}[deg/s]".format(time3, velocity3 * 180 / np.pi))
    else:
        accelaration3 = Torque/Izz
        velocity3 = Momentum/Izz
        time3_triangle = velocity3/accelaration3
        time3_rectangle = (gamma-time3_triangle*velocity3)/velocity3
        time3 = 2*time3_triangle+time3_rectangle
        plt.plot([0, time3_triangle, time3_triangle + time3_rectangle, time3], [0, velocity3, velocity3, 0], 'b-')
        print("Time3: {0}[s] & Velocity3: {1}[deg/s]".format(time3, velocity3 * 180 / np.pi))

    time = time1 + time2 + time3
    maxradialvelocity = max(velocity1,velocity2,velocity3)
    return time, maxradialvelocity

Ixx = I_solarpanel[0][0]
Iyy = I_solarpanel[1][1]
Izz = I_solarpanel[2][2]
Momentum = 0.1 #[Nms]
Torque = 0.007 #[Nm]
alpha = np.pi/180*170 #[rad]
beta = np.pi/180*180 #[rad]
gamma = np.pi/180*360 #[rad]

print0,print1 = AttitudeDeterminationTime(Ixx,Iyy,Izz,Torque,Momentum,alpha,beta,gamma)
print("Total Time: {0}[s] & Maximum Radial Velocity: {1}[deg/s]".format(print0,print1*180/np.pi))
print("Momentum Velocities: {0}[deg/s], {1}[deg/s], {2}[deg/s]".format(Momentum/Ixx*180/np.pi,Momentum/Iyy*180/np.pi,Momentum/Izz*180/np.pi))
plt.show()