import numpy as np
import math
from Transformation import TransformationOrbitalEarth
import time
'''
INPUTS:
Spacecraft 1 (S/C1)
Attitude: yaw1, roll1, pitch1 [rad] #Order Z->X->Y
Position: lat1,lon1,h1
Bright pixel: alpha1 (around y axis), beta1 (around x axis) [rad]

Spacecraft 2 (S/C2)
Attitude: yaw2, roll2, pitch2 
Position: lat2,lon2,h2
Bright pixel: alpha2 (around y axis), beta2 (around x axis) [rad]

OUTPUTS:
Distance between Spacecraft1 and Spacecraft2: d
Position1: xp1, yp1, zp1
Position2: xp2, yp2, zp2
Distance between Position1 and Position2: d
FinalPoint: xp, yp, zp 
'''

#Inputs for FOCUS payload
h = 500 #[km]

###S/C1###
#Longitude and latitude
lat1 = np.pi/2 #[rad]
lon1 = 0 #[rad]
#Attutide angles
yaw1 = np.pi/4 #[rad]
roll1 = 0 #[rad]
pitch1 = np.pi #[rad]

#Angles of the bright pixel in radians
alpha1 = 0 #[rad]
beta1 = 0 #[rad]

###S/C2###
#Longitude and latitude
lat2 = np.pi/180*68.018 #[rad]
lon2 = np.pi/2 #[rad]

#Attitude angles
yaw2 = np.pi #[rad]
roll2 = np.pi/180*(180-68.018) #[rad]
pitch2 = 0 #[rad]     (90+18.32) #[rad] #Test 170deg

#Angles of the bright pixel in radians
alpha2 = 0 #[rad]
beta2 = np.pi/180*38.018 #[rad]

def Triangulation3D(h,lat1,lon1,yaw1,roll1,pitch1,alpha1,beta1,lat2,lon2,yaw2,roll2,pitch2,alpha2,beta2):
    start_time = time.time()

    Re = 6378 #[km]
    radius = Re+h #Sum between earth radius and altitude

    #S/C1 position in km
    spacecraftlocation1 = radius*np.array([np.cos(lon1)*np.cos(lat1),np.sin(lon1)*np.cos(lat1),np.sin(lat1)])
    print("S/C1 Location [km]: ",spacecraftlocation1)

    #Representation of vector in 3D using the two angles given (alpha and beta)
    v1 = np.array([np.sin(alpha1),np.cos(alpha1)*np.sin(beta1),np.cos(alpha1)*np.cos(beta1)])
    print("Vector1 Camera: ",v1)

    #Transformation of vector into Earth fixed coordinate system
    vector1 = np.dot(TransformationOrbitalEarth(yaw1,pitch1,roll1),v1)

    print("Vector1 Attitude: ",vector1,'\n')

    #S/C2 position in km
    spacecraftlocation2 = radius*np.array([np.cos(lon2)*np.cos(lat2),np.sin(lon2)*np.cos(lat2),np.sin(lat2)])
    print("S/C2 Location [km]: ",spacecraftlocation2)

    #Representation of vector in #D using the two angles given (alpha and beta)
    v2 = np.array([np.sin(alpha2),np.cos(alpha2)*np.sin(beta2),np.cos(alpha2)*np.cos(beta2)])
    print("Vector2 Camera: ",v2)

    #Transformation of vector into Earth fixed coordinate system
    vector2 = np.dot(TransformationOrbitalEarth(yaw2,pitch2,roll2),v2)

    print("Vector2 Attitude: ",vector2,'\n')

    print("Distance between location S/C1 and S/C2 [km]: ",np.linalg.norm(spacecraftlocation1-spacecraftlocation2),'\n')

    #Nearest points
    n = np.cross(vector1,vector2)
    n1 = np.cross(vector1,n)
    n2 = np.cross(vector2,n)

    #Nearest point for the line of the S/C1
    point1 = spacecraftlocation1+(np.dot((spacecraftlocation2-spacecraftlocation1),n2)/np.dot(vector1,n2))*vector1

    #Nearest point for the line of the S/C2
    point2 = spacecraftlocation2+(np.dot((spacecraftlocation1-spacecraftlocation2),n1)/np.dot(vector2,n1))*vector2

    #Printing the two points and the
    print("Point1 [km]: ",point1)
    print("Point2 [km]: ",point2)

    #Distance for Error
    n_normalized = n/np.linalg.norm(n)
    distance1 = np.abs(np.dot(n_normalized,(spacecraftlocation2-spacecraftlocation1)))
    distance2 = np.linalg.norm(point2-point1)
    print("Distance between Point1 and Point2 [km]: ",distance1,"or ",distance2,'\n')

    final_point = (point1+point2)/2
    print("Final Point [km]:",final_point,'\n')
    print("--- Computational Time: %s seconds ---" % (time.time() - start_time))
    return final_point

#Example: print(Triangulation3D(h,lat1,lon1,yaw1,roll1,pitch1,alpha1,beta1,lat2,lon2,yaw2,roll2,pitch2,alpha2,beta2))

#%%

#PLAYING AROUND TO TRY TO GET 3D POLYGON OF INTERSECTING PIXELS
xbright = 3
ybright = 3
npixx = 5
npixy = 5
FOVx = 10
FOVy = 10

#getting the angles that form the four vertices of the bright pixel
pixbetas = np.linspace(-FOVx/2,FOVx/2,npixx+1)
pixalphas = np.linspace(-FOVy/2,FOVy/2,npixy+1)
#for the bottom left vertix (a)
abeta = pixbetas[ybright-1]
aalpha = pixalphas[xbright-1]
#for the bottom right (b)
bbeta = pixbetas[ybright]
balpha = pixalphas[xbright-1]
#for the top right (c)
cbeta = pixbetas[ybright]
calpha = pixalphas[xbright]
#for the top left (d)
dbeta = pixbetas[ybright-1]
dalpha = pixalphas[xbright]
#they only have as starting point the spacecraft position


