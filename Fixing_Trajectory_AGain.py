import numpy as np
from math import *
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate
# from AverageThrust import AvgThurst
# from CdEstimator import Cd
# from ISA_2 import density_at_height
# from TempAlt import  Temp
# from Mass_extract_2 import Mass_t
# from Velocity_Check import pixel_det
# from Velocity_Check import pixel_data
from Better_Main_Trajectory import TrajectoryData
from scipy import spatial

def alitutde_slicer(t,x,y,h):
    # a = list(h.astype(int))
    # rounded = [round(x,-3) for x in a]
    starting_point = np.argmax(h>13000)
    #print(starting_point)
    h_sliced_t = t[(starting_point+1):]
    h_sliced_x = x[(starting_point+1):]
    h_sliced_y = y[(starting_point+1):]
    h_sliced_h = h[(starting_point+1):]

    return h_sliced_t, h_sliced_x, h_sliced_y,h_sliced_h




def slicer(t,x,y,h):
    a = list(t.astype(int))
    starting_point = a.index(0)
    sliced_t = t[(starting_point+1):]
    sliced_x = x[(starting_point+1):]
    sliced_y = y[(starting_point+1):]
    sliced_h = h[(starting_point+1):]

    return  sliced_t, sliced_x, sliced_y,sliced_h



def generate_trajectories(rot_alt_step,rot_angle_step,x_trans_step, y_trans_step):

    Re = 6370 * 1000  # m   #radius of the Earth
<<<<<<< HEAD
    x_trans = np.linspace(-(pi/200),(pi/200),y_trans_step)
=======
    x_trans = np.linspace(-pi/200,pi/200,y_trans_step)
>>>>>>> 4a5b4e7c8cf78c53a3d4e8a0600dd6635c4aaff0
    #theta is defined anti-clockwise from the positive x-axis

    delta_t = np.linspace(35,50,10)

    rot_alts = np.linspace(10000,100000,rot_alt_step)
    rot_angles = np.linspace(15,40,rot_angle_step)*(pi/180)

    temp_x = []
    temp_y = []
    temp_t = []
    temp_h = []

    for alt in rot_alts:
        x, y, h, vx, vy, v, t = TrajectoryData(alt, rot_angles, 0, Re)
        print(x,y)

        for i,angle in enumerate(rot_angles):

            xvector = np.zeros((len(x),3))
            xvector[:,0] = x[:,i]
            xvector[:,1] = y[:,i]
            for theta_x in x_trans:
                for dt in delta_t:
                    transformationmatrix = sp.spatial.transform.Rotation.from_euler('z',theta_x).as_matrix()
                    xvectorrot = np.einsum('ij,kj->ki',transformationmatrix,xvector)

                    xrot = np.copy(xvectorrot[:,0])
                    yrot = np.copy(xvectorrot[:,1])

                    temp_x.append(xrot)
                    temp_y.append(yrot)
                    temp_t.append(t[:,i]-dt)
                    temp_h.append(h[:,i])

    #
    # for i in range(len(temp_h)):
    #     h_sliced_t, h_sliced_x, h_sliced_y,h_sliced_h = alitutde_slicer(temp_t[i],temp_x[i],temp_y[i],temp_h[i])
    #     temp_t[i] = h_sliced_t
    #     temp_x[i] = h_sliced_x
    #     temp_y[i] = h_sliced_y
    #     temp_h[i] = h_sliced_h


    for i  in range(len(temp_t)):
        if temp_t[i][0]<0 :
            sliced_t, sliced_x, sliced_y,sliced_h = slicer(temp_t[i],temp_x[i],temp_y[i],temp_h[i])
            temp_t[i] = sliced_t
            temp_x[i] = sliced_x
            temp_y[i] = sliced_y
            temp_h[i] = sliced_h

    return temp_x,temp_y,temp_t,temp_h

<<<<<<< HEAD
x,y,t,h = generate_trajectories(5,10,5, 10)
for i in range(len(x)):
     plt.plot(x[i],y[i])
plt.show()
=======

x,y,t,h = generate_trajectories(5,10,5, 9)
for i in range(len(x)):
     plt.plot(x[i],y[i])
plt.show()

>>>>>>> 4a5b4e7c8cf78c53a3d4e8a0600dd6635c4aaff0




