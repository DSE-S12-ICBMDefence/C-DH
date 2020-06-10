import numpy as np
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from TrianglePosition import Triangulation3D
import scipy.spatial as ss

#Flat Plane
def Plane(point0,point1,point2,rgb):
    u = point1-point0
    v = point2-point0

    cp = np.cross(u, v)
    a, b, c = cp

    d = np.dot(cp, point2)

    print('The equation is {0}x + {1}y + {2}z = {3}'.format(a, b, c, d))

    X,Y = np.meshgrid(np.linspace(-0.25,0.25,2),np.linspace(-0.25,0.25,2))

    Z = (d-a*X- b*Y) * 1. / c
    rgb = np.random.rand(3, )
    #ax.plot_surface(X, Y, Z, color=rgb)
    return a,b,c,d

def PerpendicularPlane(vector,point):
    a,b,c = vector
    d = a*point[0]+b*point[1]+c*point[2]
    X, Y = np.meshgrid(np.linspace(-0.25, 0.25, 2), np.linspace(-0.25, 0.25, 2))

    Z = (d - a * X - b * Y) * 1. / c
    rgb = np.random.rand(3, )
    ax.plot_surface(X, Y, Z, color=rgb)
    return a,b,c,d

##Intersection point
def Intersection(coeff0,coeff1,coeff2):

    A = np.array([[coeff0[0],coeff0[1],coeff0[2]],
                  [coeff1[0],coeff1[1],coeff1[2]],
                  [coeff2[0],coeff2[1],coeff2[2]]])
    B = np.transpose(np.array([coeff0[3],coeff1[3],coeff2[3]]))
    finalpoint = np.linalg.solve(A,B)
    print('The intersection is [x:{0},y:{1},z:{2}]'.format(finalpoint[0],finalpoint[1],finalpoint[2]))
    #ax.scatter3D(finalpoint[0],finalpoint[1],finalpoint[2],'black')
    return finalpoint

#Transformation FoV
def TransformationFoV(alpha,beta):
    #Transformation in x axis
    Trans_in_x=np.array([[1,0,0],
                         [0,np.cos(alpha),np.sin(alpha)],
                         [0,-np.sin(alpha),np.cos(alpha)]])
    # Transformation in y axis
    Trans_in_y=np.array([[np.cos(beta),0,-np.sin(beta)],
                         [0,1,0],
                         [np.sin(beta),0,np.cos(beta)]])

    Final_result = np.dot(Trans_in_x,Trans_in_y)
    return Final_result

def PointPerpendicularPlane(point,vector,normal):
    d = np.dot((normal-point),normal)/(np.dot(vector,normal))
    intersection = point+d*vector
    return intersection

#Inputs for FOCUS payload
Re = 6378 #[km]
hsat = 1000 #[km]
hbright = 0 #[km]
FoV = 20 * np.pi/(180 * 3600) #[rad]

###S/C1###
#Longitude and latitude
lat1 = np.pi/2 #[rad]
lon1 = 0 #[rad]

###S/C2###
#Longitude and latitude
lat2 = np.pi/180*65.2 #[rad]
lon2 = 0 #[rad]

###Bright Pixel###
latbright = np.pi/180*70 #[rad]
lonbright = 0 #[rad]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

radiussat = Re+hsat #[km]
radiusbright = Re + hbright #[km]

pointsc1 = pointsc1_x,pointsc1_y,pointsc1_z = radiussat*np.array([np.cos(lon1)*np.cos(lat1),np.sin(lon1)*np.cos(lat1),np.sin(lat1)])
pointsc2 = pointsc2_x,pointsc2_y,pointsc2_z = radiussat*np.array([np.cos(lon2)*np.cos(lat2),np.sin(lon2)*np.cos(lat2),np.sin(lat2)])
pointpixel = pointpixel_x,pointpixel_y,pointpixel_z = radiusbright*np.array([np.cos(lonbright)*np.cos(latbright),np.sin(lonbright)*np.cos(latbright),np.sin(latbright)])

ax.set_xlim([pointpixel_x-1,pointpixel_x+1])
ax.set_ylim([pointpixel_y-1,pointpixel_y+1])
ax.set_zlim([pointpixel_z-1,pointpixel_z+1])

ax.scatter3D(pointsc1_x,pointsc1_y,pointsc1_z,color = 'red')
ax.scatter3D(pointsc2_x,pointsc2_y,pointsc2_z,color = 'blue')
ax.scatter3D(pointpixel_x,pointpixel_y,pointpixel_z,color = 'black')

print(pointpixel)

ax.plot3D([pointsc1_x,pointpixel_x],[pointsc1_y,pointpixel_y],[pointsc1_z,pointpixel_z],color = 'red')
ax.plot3D([pointsc2_x,pointpixel_x],[pointsc2_y,pointpixel_y],[pointsc2_z,pointpixel_z],color = 'blue')

vectorsc1 = pointsc1-pointpixel
vectorsc2 = pointsc2-pointpixel

camera1vector1 = camera1vector1_x,camera1vector1_y,camera1vector1_z= np.dot(TransformationFoV(FoV/2,FoV/2),vectorsc1)
camera2vector1 = camera2vector1_x,camera2vector1_y,camera2vector1_z= np.dot(TransformationFoV(-FoV/2,FoV/2),vectorsc1)
camera3vector1 = camera3vector1_x,camera3vector1_y,camera3vector1_z= np.dot(TransformationFoV(FoV/2,-FoV/2),vectorsc1)
camera4vector1 = camera4vector1_x,camera4vector1_y,camera4vector1_z= np.dot(TransformationFoV(-FoV/2,-FoV/2),vectorsc1)

camera1vector2 = camera1vector2_x,camera1vector2_y,camera1vector2_z= np.dot(TransformationFoV(FoV/2,FoV/2),vectorsc2)
camera2vector2 = camera2vector2_x,camera2vector2_y,camera2vector2_z= np.dot(TransformationFoV(-FoV/2,FoV/2),vectorsc2)
camera3vector2 = camera3vector2_x,camera3vector2_y,camera3vector2_z= np.dot(TransformationFoV(FoV/2,-FoV/2),vectorsc2)
camera4vector2 = camera4vector2_x,camera4vector2_y,camera4vector2_z= np.dot(TransformationFoV(-FoV/2,-FoV/2),vectorsc2)

ax.plot3D([pointsc1_x,pointsc1_x-camera1vector1_x],[pointsc1_y,pointsc1_y-camera1vector1_y],[pointsc1_z,pointsc1_z-camera1vector1_z],color = 'black')
ax.scatter3D(pointsc1_x-camera1vector1_x,pointsc1_y-camera1vector1_y,pointsc1_z-camera1vector1_z,color = 'black')
ax.scatter3D(pointsc1_x-camera2vector1_x,pointsc1_y-camera2vector1_y,pointsc1_z-camera2vector1_z,color = 'green')
ax.scatter3D(pointsc1_x-camera3vector1_x,pointsc1_y-camera3vector1_y,pointsc1_z-camera3vector1_z,color = 'yellow')
ax.scatter3D(pointsc1_x-camera4vector1_x,pointsc1_y-camera4vector1_y,pointsc1_z-camera4vector1_z,color = 'pink')

ax.plot3D([pointsc2_x,pointsc2_x-camera1vector2_x],[pointsc2_y,pointsc2_y-camera1vector2_y],[pointsc2_z,pointsc2_z-camera1vector2_z],color = 'black')
ax.scatter3D(pointsc2_x-camera1vector2_x,pointsc2_y-camera1vector2_y,pointsc2_z-camera1vector2_z,color = 'black')
ax.scatter3D(pointsc2_x-camera2vector2_x,pointsc2_y-camera2vector2_y,pointsc2_z-camera2vector2_z,color = 'green')
ax.scatter3D(pointsc2_x-camera3vector2_x,pointsc2_y-camera3vector2_y,pointsc2_z-camera3vector2_z,color = 'yellow')
ax.scatter3D(pointsc2_x-camera4vector2_x,pointsc2_y-camera4vector2_y,pointsc2_z-camera4vector2_z,color = 'pink')

plane1sc1 = a1sc1,b1sc1,c1sc1,d1sc1 = Plane(pointsc1,pointsc1-camera1vector1,pointsc1-camera2vector1,'black')
plane2sc1 = a2sc1,b2sc1,c2sc1,d2sc1 = Plane(pointsc1,pointsc1-camera2vector1,pointsc1-camera3vector1,'green')
plane3sc1 = a3sc1,b3sc1,c3sc1,d3sc1 = Plane(pointsc1,pointsc1-camera3vector1,pointsc1-camera4vector1,'yellow')
plane4sc1 = a4sc1,b4sc1,c4sc1,d4sc1 = Plane(pointsc1,pointsc1-camera4vector1,pointsc1-camera1vector1,'pink')

plane1sc2 = a1sc2,b1sc2,c1sc2,d1sc2 = Plane(pointsc2,pointsc2-camera1vector2,pointsc2-camera2vector2,'black')
plane2sc2 = a2sc2,b2sc2,c2sc2,d2sc2 = Plane(pointsc2,pointsc2-camera2vector2,pointsc2-camera3vector2,'green')
plane3sc2 = a3sc2,b3sc2,c3sc2,d3sc2 = Plane(pointsc2,pointsc2-camera3vector2,pointsc2-camera4vector2,'yellow')
plane4sc2 = a4sc2,b4sc2,c4sc2,d4sc2 = Plane(pointsc2,pointsc2-camera4vector2,pointsc2-camera1vector2,'pink')

intersection1 = Intersection(plane1sc1,plane1sc2,plane2sc1)
intersection2 = Intersection(plane1sc1,plane1sc2,plane2sc2)
intersection3 = Intersection(plane1sc1,plane1sc2,plane4sc1)
intersection4 = Intersection(plane1sc1,plane1sc2,plane4sc2)
intersection5 = Intersection(plane1sc1,plane3sc2,plane2sc1)
intersection6 = Intersection(plane1sc1,plane3sc2,plane2sc2)
intersection7 = Intersection(plane1sc1,plane3sc2,plane4sc1)
intersection8 = Intersection(plane1sc1,plane3sc2,plane4sc2)
intersection9 = Intersection(plane3sc1,plane1sc2,plane2sc1)
intersection10 = Intersection(plane3sc1,plane1sc2,plane2sc2)
intersection11 = Intersection(plane3sc1,plane1sc2,plane4sc1)
intersection12 = Intersection(plane3sc1,plane1sc2,plane4sc2)
intersection13 = Intersection(plane3sc1,plane3sc2,plane2sc1)
intersection14 = Intersection(plane3sc1,plane3sc2,plane2sc2)
intersection15 = Intersection(plane3sc1,plane3sc2,plane4sc1)
intersection16 = Intersection(plane3sc1,plane3sc2,plane4sc2)

def InsidePoint(point,coeff,direction):
    epsilon = 10 ** (-5)
    a,b,c,d = coeff
    x,y,z = point
    value = a*x+b*y+c*z+d
    if direction=='right':
        if value>-epsilon:
            return True
        else:
            return False
    elif direction=='left':
        if value<epsilon:
            return True
        else:
            return False


print(InsidePoint(intersection1))


plt.show()

