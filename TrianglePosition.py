import numpy as np
import math
from Transformation import TransformationOrbitalEarth
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

#Inputs for FOCUS payload
h = 500 #[km]
Re = 6378 #[km]
radius = Re+h #Sum between earth radius and altitude
factorsize = 15*10**(-3) #[km]

###S/C1###

#Longitude and latitude 
lat1 = np.pi/2 #[rad]
lon1 = 0 #[rad]

#S/C1 position in km
spacecraftlocation1 = radius*np.array([np.cos(lon1)*np.cos(lat1),np.sin(lon1)*np.cos(lat1),np.sin(lat1)])
print("S/C1 Location: ",spacecraftlocation1)

#Attutide angles
yaw1 = 0 #[rad]
roll1 = 0 #[rad]
pitch1 = np.pi #[rad]

#Angles of the bright pixel in radians
alpha1,beta1 = [0,0]

#Representation of vector in 3D using the two angles given (alpha and beta)
v1 = np.array([np.sin(alpha1),np.cos(alpha1)*np.sin(beta1),np.cos(alpha1)*np.cos(beta1)])
print("Vector1 Camera:",v1)

#Transformation of vector into Earth fixed coordinate system
vector1 = np.dot(TransformationOrbitalEarth(yaw1,pitch1,roll1),v1)

print("Vector1 Attitude:",vector1,'\n')

###S/C2###

#Longitude and latitude
lat2 = np.pi/180*80 #[rad]
lon2 = 0 #[rad]

#S/C2 position in km
spacecraftlocation2 = radius*np.array([np.cos(lon2)*np.cos(lat2),np.sin(lon2)*np.cos(lat2),np.sin(lat2)])
print("S/C2 Location: ",spacecraftlocation2)

#Attitude angles
yaw2 = 0 #[rad]
roll2 = 0 #[rad]
pitch2 = np.pi/180*170 #[rad]

#Angles of the bright pixel in radians
alpha2,beta2 = [0,0]

#Representation of vector in #D using the two angles given (alpha and beta)
v2 = np.array([np.sin(alpha2),np.cos(alpha2)*np.sin(beta2),np.cos(alpha2)*np.cos(beta2)])
print("Vector2 Camera",v2)

#Transformation of vector into Earth fixed coordinate system
vector2 = np.dot(TransformationOrbitalEarth(yaw2,pitch2,roll2),v2)
print("Vector2 Attitude",vector2,'\n')

#Nearest points
n = np.cross(vector1,vector2)
n1 = np.cross(vector1,n)
n2 = np.cross(vector2,n)

#Nearest point for the line of the S/C1
point1 = spacecraftlocation1+(np.dot((spacecraftlocation2-spacecraftlocation1),n2)/np.dot(vector1,n2))*vector1

#Nearest point for the line of the S/C2
point2 = spacecraftlocation2+(np.dot((spacecraftlocation1-spacecraftlocation2),n1)/np.dot(vector2,n1))*vector2

#Printing the two points and the
print("Point1: ",point1)
print("Point2: ",point2)

#Distance for Error
n_normalized = n/np.linalg.norm(n)
distance1 = np.abs(np.dot(n_normalized,(spacecraftlocation2-spacecraftlocation1)))
distance2 = np.linalg.norm(point2-point1)
print("Distance between Point1 and Point2: ",distance1,"or ",distance2)