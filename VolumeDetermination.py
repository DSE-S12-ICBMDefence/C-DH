import numpy as np
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from TrianglePosition import Triangulation3D
import scipy.spatial as ss


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
pointsc1 = pointsc1_x,pointsc1_y,pointsc1_z = np.array([0,0,4])

camera1sc1 = camera1sc1_x,camera1sc1_y,camera1sc1_z = np.array([1,0,0])
camera2sc1 = camera2sc1_x,camera2sc1_y,camera2sc1_z = np.array([0,-1,0])
camera3sc1 = camera3sc1_x,camera3sc1_y,camera3sc1_z = np.array([-1,0,0])
camera4sc1 = camera4sc1_x,camera4sc1_y,camera4sc1_z = np.array([0,1,0])

pointsc2 = pointsc2_x,pointsc2_y,pointsc2_z = np.array([0.5,0.5,4])

camera1sc2 = camera1sc2_x,camera1sc2_y,camera1sc2_z = np.array([1.5,0.5,0])
camera2sc2 = camera2sc2_x,camera2sc2_y,camera2sc2_z = np.array([0.5,-0.5,0])
camera3sc2 = camera3sc2_x,camera3sc2_y,camera3sc2_z = np.array([-0.5,0.5,0])
camera4sc2 = camera4sc2_x,camera4sc2_y,camera4sc2_z = np.array([0.5,1.5,0])

def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

#Flat Plane
def plane(point0,point1,point2,rgb):
    ux, uy, uz = u = point1-point0
    vx, vy, vz = v = point2-point0

    cp = np.cross(u, v)
    a, b, c = cp

    d = np.dot(cp, point2)

    print('The equation is {0}x + {1}y + {2}z = {3}'.format(a, b, c, d))

    X,Y = np.meshgrid(np.linspace(0.25,0.75,2),np.linspace(0.25,0.75,2))

    Z = (d-a*X- b*Y) * 1. / c
    rgb = np.random.rand(3, )
    ax.plot_surface(X, Y, Z, color=rgb)
    return a,b,c,d

a0_1,b0_1,c0_1,d0_1 = plane(camera1sc1,camera2sc1,camera3sc1,'yellow')
a1_1,b1_1,c1_1,d1_1 = plane(pointsc1,camera1sc1,camera2sc1,'green')
a2_1,b2_1,c2_1,d2_1 = plane(pointsc1,camera2sc1,camera3sc1,'black')
a3_1,b3_1,c3_1,d3_1 = plane(pointsc1,camera3sc1,camera4sc1,'orange')
a4_1,b4_1,c4_1,d4_1 = plane(pointsc1,camera4sc1,camera1sc1,'gray')

a0_2,b0_2,c0_2,d0_2 = plane(camera1sc2,camera2sc2,camera3sc2,'yellow')
a1_2,b1_2,c1_2,d1_2 = plane(pointsc2,camera1sc2,camera2sc2,'green')
a2_2,b2_2,c2_2,d2_2 = plane(pointsc2,camera2sc2,camera3sc2,'black')
a3_2,b3_2,c3_2,d3_2 = plane(pointsc2,camera3sc2,camera4sc2,'orange')
a4_2,b4_2,c4_2,d4_2 = plane(pointsc2,camera4sc2,camera1sc2,'gray')

##Intersection point
#A = np.array([[a0,b0,c0],
#              [a1,b1,c1],
#              [a2,b2,c2]])
#B = np.transpose(np.array([d0,d1,d2]))
#print(np.linalg.solve(A,B))

ax.scatter3D(pointsc1_x,pointsc1_y,pointsc1_z,color = 'red')
ax.scatter3D(camera1sc1_x,camera1sc1_y,camera1sc1_z,color = 'red')
ax.scatter3D(camera2sc1_x,camera2sc1_y,camera2sc1_z,color = 'red')
ax.scatter3D(camera3sc1_x,camera3sc1_y,camera3sc1_z,color = 'red')
ax.scatter3D(camera4sc1_x,camera4sc1_y,camera4sc1_z,color = 'red')

ax.plot3D([pointsc1_x,camera1sc1_x],[pointsc1_y,camera1sc1_y],[pointsc1_z,camera1sc1_z],color = 'red')
ax.plot3D([pointsc1_x,camera2sc1_x],[pointsc1_y,camera2sc1_y],[pointsc1_z,camera2sc1_z],color = 'red')
ax.plot3D([pointsc1_x,camera3sc1_x],[pointsc1_y,camera3sc1_y],[pointsc1_z,camera3sc1_z],color = 'red')
ax.plot3D([pointsc1_x,camera4sc1_x],[pointsc1_y,camera4sc1_y],[pointsc1_z,camera4sc1_z],color = 'red')
ax.plot3D([camera1sc1_x,camera2sc1_x,camera3sc1_x,camera4sc1_x,camera1sc1_x],
          [camera1sc1_y,camera2sc1_y,camera3sc1_y,camera4sc1_y,camera1sc1_y],
          [camera1sc1_z,camera2sc1_z,camera3sc1_z,camera4sc1_z,camera1sc1_z],color = 'red')

ax.scatter3D(pointsc2_x,pointsc2_y,pointsc2_z,color = 'blue')

ax.scatter3D(camera1sc2_x,camera1sc2_y,camera1sc2_z,color = 'blue')
ax.scatter3D(camera2sc2_x,camera2sc2_y,camera2sc2_z,color = 'blue')
ax.scatter3D(camera3sc2_x,camera3sc2_y,camera3sc2_z,color = 'blue')
ax.scatter3D(camera4sc2_x,camera4sc2_y,camera4sc2_z,color = 'blue')

ax.plot3D([pointsc2_x,camera1sc2_x],[pointsc2_y,camera1sc2_y],[pointsc2_z,camera1sc2_z],color = 'blue')
ax.plot3D([pointsc2_x,camera2sc2_x],[pointsc2_y,camera2sc2_y],[pointsc2_z,camera2sc2_z],color = 'blue')
ax.plot3D([pointsc2_x,camera3sc2_x],[pointsc2_y,camera3sc2_y],[pointsc2_z,camera3sc2_z],color = 'blue')
ax.plot3D([pointsc2_x,camera4sc2_x],[pointsc2_y,camera4sc2_y],[pointsc2_z,camera4sc2_z],color = 'blue')
ax.plot3D([camera1sc2_x,camera2sc2_x,camera3sc2_x,camera4sc2_x,camera1sc2_x],
          [camera1sc2_y,camera2sc2_y,camera3sc2_y,camera4sc2_y,camera1sc2_y],
          [camera1sc2_z,camera2sc2_z,camera3sc2_z,camera4sc2_z,camera1sc2_z],color = 'blue')


plt.show()

