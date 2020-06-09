import numpy as np
from math import *
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate
from AverageThrust import AvgThurst
from CdEstimator import Cd
#from ISA_2 import mass_time
from ISA_2 import density_at_height
from TempAlt import  Temp
from Mass_extract_2 import Mass_t
from Velocity_Check import pixel_det
# from Velocity_Check import pixel_data
from Velocity_Check import get_pixel_data
# from Velocity_Check import theta
from Main_Trajectory import TrajectoryData

rot_alt_step = 5
rot_angle_step = 2
x_trans_step = 5
y_trans_step = 10
FOV_l   = -10*pi/180 #rad
FOV_r   = +10*pi/180 #rad
Re   = 6371 #km
n_pix = 21
h = 1000 #km
grav_c = 398600 #km^3 s^-2

spot = np.array([0,Re])
theta_0 = 1*pi/180 + pi/2 #rad



# def generate_trajectories(rot_alt_step,rot_angle_step):
#
#     rot_alts = np.linspace(10000,100000,rot_alt_step)
#     rot_angles = np.linspace(15,40,rot_angle_step)
#
#     temp_x = []
#     temp_y = []
#     temp_t = []
#     for alt in rot_alts:
#         for angle in rot_angles:
#             x, y, h, vx, vy, v,t = TrajectoryData(alt, angle)
#             temp_x.append(x)
#             temp_y.append(y)
#             temp_t.append(t)
#
#
#     return temp_x,temp_y,temp_t
#
#


def generate_trajectories(rot_alt_step,rot_angle_step,x_trans_step, y_trans_step):

    Re = 6370 * 1000  # m   #radius of the Earth
    x_trans = np.linspace(0,2*pi-0.01,y_trans_step)
    #theta is defined anti-clockwise from the positive x-axis

    delta_t = np.linspace(0,10,10)

    rot_alts = np.linspace(10000,100000,rot_alt_step)
    rot_angles = np.linspace(15,40,rot_angle_step)*(pi/180)

    temp_x = []
    temp_y = []
    temp_t = []
    for alt in rot_alts:
        for angle in rot_angles:
            x, y, h, vx, vy, v, t = TrajectoryData(alt, angle, 0, Re)
            xvector = np.zeros((len(x),3))
            xvector[:,0] = x
            xvector[:,1] = y
            for theta_x in x_trans:
                for dt in delta_t:
                    transformationmatrix = sp.spatial.transform.Rotation.from_euler('z',theta_x).as_matrix()
                    xvectorrot = np.einsum('ij,kj->ki',transformationmatrix,xvector)

                    xrot = np.copy(xvectorrot[:,0])
                    yrot = np.copy(xvectorrot[:,1])

                    temp_x.append(xrot)
                    temp_y.append(yrot)
                    temp_t.append(t-dt)


    return temp_x,temp_y,temp_t

def compile_matrix(t,x,y):
    piece = np.array([[t],[x],[y]])

    return piece


x,y,t = generate_trajectories(rot_alt_step,rot_angle_step, x_trans_step, y_trans_step)

t_new = np.array(t)
x_new = np.array(x)
y_new = np.array(y)

iterations = rot_alt_step*rot_angle_step* x_trans_step*y_trans_step
i = 0
matrix = np.empty([iterations,3,1,92])

while i<iterations:
    piece = compile_matrix(t_new[i],x_new[i],y_new[i])
    matrix[i,:,:,:] = piece

    i += 1

pixel_data = get_pixel_data(0, running=True)
pixel_data = pixel_data[1:]

for row in range(len(pixel_data)):
    print(pixel_data[row,0])
    theta = pixel_data[row,-1]
    pix, m1, b1, m2, b2, mu, p = pixel_det(theta, spot, FOV_l, FOV_r, h, n_pix)
    i = 0
    while i < len(matrix):

        y1 = (pixel_data[row, 1]*matrix[i,1,0, row] + pixel_data[row,2])*1000
        y2 = (pixel_data[row, 3]*matrix[i,1,0, row] + pixel_data[row,4])*1000
        y_traj = matrix[i,2,0, row]
        #
        # y1 = 3
        # y2 = 2
        # y_traj = 2.5


        # if statement on field of view
        if mu<0 and y_traj>y1 and y_traj<y2:
           matrix = np.delete(matrix,i,0)

        if mu>0 and y_traj < y1 and y_traj > y2:
            matrix = np.delete(matrix,i,0)

        i = i+1

    #print(matrix)
    print(len(matrix))



















