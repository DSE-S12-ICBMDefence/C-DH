import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from TrianglePosition import Triangulation3D


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
pointsc1_x,pointsc1_y,pointsc1_z = [0,0,4]

camera1sc1_x,camera1sc1_y,camera1sc1_z = [1,0,0]
camera2sc1_x,camera2sc1_y,camera2sc1_z = [0,-1,0]
camera3sc1_x,camera3sc1_y,camera3sc1_z = [-1,0,0]
camera4sc1_x,camera4sc1_y,camera4sc1_z = [0,1,0]

pointsc2_x,pointsc2_y,pointsc2_z = [0.5,0.5,4]

camera1sc2_x,camera1sc2_y,camera1sc2_z = [1.5,0.5,0]
camera2sc2_x,camera2sc2_y,camera2sc2_z = [0.5,-0.5,0]
camera3sc2_x,camera3sc2_y,camera3sc2_z = [-0.5,0.5,0]
camera4sc2_x,camera4sc2_y,camera4sc2_z = [0.5,1.5,0]

ux, uy, uz = u = [camera2sc1_x-camera1sc1_x, camera2sc1_y-camera1sc1_y, camera2sc1_z-camera1sc1_z]
vx, vy, vz = v = [camera3sc1_x-camera1sc1_x, camera3sc1_y-camera1sc1_y, camera3sc1_z-camera1sc1_z]

u_cross_v = [uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx]

point = [camera1sc1_x,camera1sc1_y,camera1sc1_z]
point  = np.array(point)
normal = np.array(u_cross_v)

d = -point.dot(normal)

xsc1 = np.linspace(-1,1,3)
ysc1 = np.linspace(-1,1,3)

X,Y = np.meshgrid(xsc1,ysc1)

Z = (-normal[0] * xsc1 - normal[1] * ysc1 - d) * 1. / normal[2]
print(Z)

surf = ax.plot_surface(X, Y, Z, color='orange')

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