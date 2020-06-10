import numpy as np
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from TrianglePosition import Triangulation3D
import scipy.spatial as ss

#Flat Plane
def plane(point0,point1,point2,rgb):
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

def perpendicularplane(vector,point):
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
    return np.linalg.solve(A,B)

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

#uEarth, vEarth = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
#xEarth = Re*np.cos(uEarth)*np.sin(vEarth)
#yEarth = Re*np.sin(uEarth)*np.sin(vEarth)
#zEarth = Re*np.cos(vEarth)
#ax.plot_wireframe(xEarth, yEarth, zEarth, color="k")

radiussat = Re+hsat #[km]
radiusbright = Re + hbright #[km]

pointsc1 = pointsc1_x,pointsc1_y,pointsc1_z = radiussat*np.array([np.cos(lon1)*np.cos(lat1),np.sin(lon1)*np.cos(lat1),np.sin(lat1)])
pointsc2 = pointsc2_x,pointsc2_y,pointsc2_z = radiussat*np.array([np.cos(lon2)*np.cos(lat2),np.sin(lon2)*np.cos(lat2),np.sin(lat2)])
pointpixel = pointpixel_x,pointpixel_y,pointpixel_z = radiusbright*np.array([np.cos(lonbright)*np.cos(latbright),np.sin(lonbright)*np.cos(latbright),np.sin(latbright)])

#ax.set_xlim([pointpixel_x-1,pointpixel_x+1])
#ax.set_ylim([pointpixel_y-1,pointpixel_y+1])
#ax.set_zlim([pointpixel_z-1,pointpixel_z+1])

ax.scatter3D(pointsc1_x,pointsc1_y,pointsc1_z,color = 'red')
ax.scatter3D(pointsc2_x,pointsc2_y,pointsc2_z,color = 'blue')
ax.scatter3D(pointpixel_x,pointpixel_y,pointpixel_z,color = 'black')

ax.plot3D([pointsc1_x,pointpixel_x],[pointsc1_y,pointpixel_y],[pointsc1_z,pointpixel_z],color = 'red')
ax.plot3D([pointsc2_x,pointpixel_x],[pointsc2_y,pointpixel_y],[pointsc2_z,pointpixel_z],color = 'blue')

vectorsc1 = pointsc1-pointpixel
vectorsc2 = pointsc2-pointpixel
#coeff0 = a0,b0,c0,d0 = perpendicularplane(pointpixel-0,pointpixel)

camera1vector1 = np.dot(np.array([[1/np.sin(FoV/2),0,0],[0,np.sin(FoV/2),0],[0,0,np.cos(FoV/2)*np.cos(FoV/2)]]),vectorsc1)
print(camera1vector1)
camera1sc1 = camera1sc1_x,camera1sc1_y,camera1sc1_z = PointPerpendicularPlane(pointsc1,camera1vector1,pointpixel)
ax.plot3D([pointsc1_x,camera1sc1_x],[pointsc1_y,camera1sc1_y],[pointsc1_z,camera1sc1_z],color = 'black')

camera2vector1 = np.dot(TransformationFoV(-FoV/2,FoV/2),vectorsc1)
camera2sc1 = camera2sc1_x,camera2sc1_y,camera2sc1_z = PointPerpendicularPlane(pointsc1,camera2vector1,pointpixel)
#ax.plot3D([pointsc1_x,camera2sc1_x],[pointsc1_y,camera2sc1_y],[pointsc1_z,camera2sc1_z],color = 'black')

camera3vector1 = np.dot(TransformationFoV(FoV/2,-FoV/2),vectorsc1)
camera3sc1 = camera3sc1_x,camera3sc1_y,camera3sc1_z = PointPerpendicularPlane(pointsc1,camera3vector1,pointpixel)
#ax.plot3D([pointsc1_x,camera3sc1_x],[pointsc1_y,camera3sc1_y],[pointsc1_z,camera3sc1_z],color = 'black')

camera4vector1 = np.dot(TransformationFoV(-FoV/2,-FoV/2),vectorsc1)
camera4sc1 = camera4sc1_x,camera4sc1_y,camera4sc1_z = PointPerpendicularPlane(pointsc1,camera4vector1,pointpixel)
#ax.plot3D([pointsc1_x,camera4sc1_x],[pointsc1_y,camera4sc1_y],[pointsc1_z,camera4sc1_z],color = 'black')

#print(vectorsc1,TransformationFoV(FoV/2,FoV/2)*vectorsc1)
#pointsc1 = pointsc1_x,pointsc1_y,pointsc1_z = np.array([0,0,4])

#camera1sc1 = camera1sc1_x,camera1sc1_y,camera1sc1_z = np.array([1,0,0])
#camera2sc1 = camera2sc1_x,camera2sc1_y,camera2sc1_z = np.array([0,-1,0])
#camera3sc1 = camera3sc1_x,camera3sc1_y,camera3sc1_z = np.array([-1,0,0])
#camera4sc1 = camera4sc1_x,camera4sc1_y,camera4sc1_z = np.array([0,1,0])

#pointsc2 = pointsc2_x,pointsc2_y,pointsc2_z = np.array([0.5,0.5,4])

#camera1sc2 = camera1sc2_x,camera1sc2_y,camera1sc2_z = np.array([1.5,0.5,0])
#camera2sc2 = camera2sc2_x,camera2sc2_y,camera2sc2_z = np.array([0.5,-0.5,0])
#camera3sc2 = camera3sc2_x,camera3sc2_y,camera3sc2_z = np.array([-0.5,0.5,0])
#camera4sc2 = camera4sc2_x,camera4sc2_y,camera4sc2_z = np.array([0.5,1.5,0])

#coeff0_1 = a0_1,b0_1,c0_1,d0_1 = plane(camera1sc1,camera2sc1,camera3sc1,'yellow')
#coeff1_1 = a1_1,b1_1,c1_1,d1_1 = plane(pointsc1,camera1sc1,camera2sc1,'green')
#coeff2_1 = a2_1,b2_1,c2_1,d2_1 = plane(pointsc1,camera2sc1,camera3sc1,'black')
#coeff3_1 = a3_1,b3_1,c3_1,d3_1 = plane(pointsc1,camera3sc1,camera4sc1,'orange')
#coeff4_1 = a4_1,b4_1,c4_1,d4_1 = plane(pointsc1,camera4sc1,camera1sc1,'gray')

#coeff0_2 = a0_2,b0_2,c0_2,d0_2 = plane(camera1sc2,camera2sc2,camera3sc2,'yellow')
#coeff1_2 = a1_2,b1_2,c1_2,d1_2 = plane(pointsc2,camera1sc2,camera2sc2,'green')
#coeff2_2 = a2_2,b2_2,c2_2,d2_2 = plane(pointsc2,camera2sc2,camera3sc2,'black')
#coeff3_2 = a3_2,b3_2,c3_2,d3_2 = plane(pointsc2,camera3sc2,camera4sc2,'orange')
#coeff4_2 = a4_2,b4_2,c4_2,d4_2 = plane(pointsc2,camera4sc2,camera1sc2,'gray')

#ax.scatter3D(camera1sc1_x,camera1sc1_y,camera1sc1_z,color = 'red')
#ax.scatter3D(camera2sc1_x,camera2sc1_y,camera2sc1_z,color = 'red')
#ax.scatter3D(camera3sc1_x,camera3sc1_y,camera3sc1_z,color = 'red')
#ax.scatter3D(camera4sc1_x,camera4sc1_y,camera4sc1_z,color = 'red')

#ax.plot3D([pointsc1_x,camera1sc1_x],[pointsc1_y,camera1sc1_y],[pointsc1_z,camera1sc1_z],color = 'red')
#ax.plot3D([pointsc1_x,camera2sc1_x],[pointsc1_y,camera2sc1_y],[pointsc1_z,camera2sc1_z],color = 'red')
#ax.plot3D([pointsc1_x,camera3sc1_x],[pointsc1_y,camera3sc1_y],[pointsc1_z,camera3sc1_z],color = 'red')
#ax.plot3D([pointsc1_x,camera4sc1_x],[pointsc1_y,camera4sc1_y],[pointsc1_z,camera4sc1_z],color = 'red')
#ax.plot3D([camera1sc1_x,camera2sc1_x,camera3sc1_x,camera4sc1_x,camera1sc1_x],
#          [camera1sc1_y,camera2sc1_y,camera3sc1_y,camera4sc1_y,camera1sc1_y],
#          [camera1sc1_z,camera2sc1_z,camera3sc1_z,camera4sc1_z,camera1sc1_z],color = 'red')

#ax.scatter3D(camera1sc2_x,camera1sc2_y,camera1sc2_z,color = 'blue')
#ax.scatter3D(camera2sc2_x,camera2sc2_y,camera2sc2_z,color = 'blue')
#ax.scatter3D(camera3sc2_x,camera3sc2_y,camera3sc2_z,color = 'blue')
#ax.scatter3D(camera4sc2_x,camera4sc2_y,camera4sc2_z,color = 'blue')

#ax.plot3D([pointsc2_x,camera1sc2_x],[pointsc2_y,camera1sc2_y],[pointsc2_z,camera1sc2_z],color = 'blue')
#ax.plot3D([pointsc2_x,camera2sc2_x],[pointsc2_y,camera2sc2_y],[pointsc2_z,camera2sc2_z],color = 'blue')
#ax.plot3D([pointsc2_x,camera3sc2_x],[pointsc2_y,camera3sc2_y],[pointsc2_z,camera3sc2_z],color = 'blue')
#ax.plot3D([pointsc2_x,camera4sc2_x],[pointsc2_y,camera4sc2_y],[pointsc2_z,camera4sc2_z],color = 'blue')
#ax.plot3D([camera1sc2_x,camera2sc2_x,camera3sc2_x,camera4sc2_x,camera1sc2_x],
#          [camera1sc2_y,camera2sc2_y,camera3sc2_y,camera4sc2_y,camera1sc2_y],
#          [camera1sc2_z,camera2sc2_z,camera3sc2_z,camera4sc2_z,camera1sc2_z],color = 'blue')


plt.show()

