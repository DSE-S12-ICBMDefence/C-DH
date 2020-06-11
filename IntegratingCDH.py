import numpy as np
from math import *
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate
# from AverageThrust import AvgThurst
# from CdEstimator import Cd
# #from ISA_2 import mass_time
# from ISA_2 import density_at_height
# from TempAlt import  Temp
# from Mass_extract_2 import Mass_t
from Velocity_Check import pixel_det
# from Velocity_Check import pixel_data
from Velocity_Check import get_pixel_data
# from Velocity_Check import theta
from Main_Trajectory import TrajectoryData
from Fixing_Trajectory_AGain import generate_trajectories
from Velocity_Check import FOV_l,FOV_r,Re,n_pix,h,grav_c,spot,theta_0

rot_alt_step = 1000
rot_angle_step = 10
x_trans_step = 1
y_trans_step = 101
# FOV_l   = -20*pi/180 #rad
# FOV_r   = +20*pi/180 #rad
# Re   = 6371 #km
# n_pix = 1001
# h = 1000 #km
# grav_c = 398600 #km^3 s^-2
#
# spot = np.array([0,Re])
# theta_0 = -3*pi/180 + pi/2 #rad



def compile_matrix(t,x,y):
    piece = np.array([[t],[x],[y]])

    return piece


x,y,t,h_fun = generate_trajectories(rot_alt_step,rot_angle_step, x_trans_step, y_trans_step)

#looking at what trajectories we have
# for i in range(len(x)):
#      plt.plot(x[i],y[i])
# plt.show()


t_new = np.array(t)
x_new = np.array(x)
y_new = np.array(y)

iterations = rot_alt_step*rot_angle_step*y_trans_step
i = 0
matrix = np.empty([iterations,3,1,53])
#len(t_new[0])+2
len_mat = []
time = []


while i<iterations:

    a = np.shape(t_new[i])

    # while a != np.shape(np.empty(91)):
    #     t_new[i]=np.append(t_new[i], 0)
    #     x_new[i]=np.append(x_new[i], 0)
    #     y_new[i]=np.append(y_new[i], 0)
    #     a = np.shape(t_new[i])


    piece = compile_matrix(t_new[i], x_new[i], y_new[i])
    # print(piece)

    matrix[i,:,:,:] = piece

    i += 1



pixel_data = get_pixel_data(0, running=True)
pixel_data = pixel_data[1:]

shape = np.shape(matrix[0]) #shape of the new matrix we want

for row in range(len(pixel_data)):

    new_matrix = [np.zeros((shape[0],shape[1],shape[2]))] #new matrix so we can fill it with valid trajectories
    print("t=", pixel_data[row,0]) #printing time stamp

    time.append(pixel_data[row,0]) #list of time
    len_mat.append(len(matrix)) #list of time
    theta = pixel_data[row,-1] #theta for pixel_det

    pix, m1, b1, m2, b2, mu, p = pixel_det(theta, spot, FOV_l, FOV_r, h, n_pix) #pixel det for mu
    # print(matrix)
    # print('theta is',theta*180/pi)
    for trajectory in matrix:
        # print('here goes the new one')
        # print(trajectory)

        y1 = (pixel_data[row, 1]*trajectory[1,0, row] + pixel_data[row,2])*1000
        y2 = (pixel_data[row, 3]*trajectory[1,0, row] + pixel_data[row,4])*1000

        y10 = (pixel_data[row, 1] * trajectory[1, 0, row]*0 + pixel_data[row, 2]) * 1000
        y20 = (pixel_data[row, 3] * trajectory[1, 0, row]*0 + pixel_data[row, 4]) * 1000
        # print(trajectory[1,0, row],trajectory[2,0, row])
        # print('the range in which it can fall is ',y2-y1,'meters big')
        # print('between',y10,'and',y20)
        y_traj = trajectory[2,0, row]

        # y_traj = Re*1000


        # print(y1,y2,y_traj)

        # if statement on field of view
        if mu < 0:
            if y_traj < y1 and y_traj > y2:
                new_matrix = np.vstack((new_matrix, [trajectory])) #adding the good trajectories to the matrix

        if mu > 0:
            if y_traj > y1 and y_traj < y2:
                new_matrix = np.vstack((new_matrix, [trajectory])) #adding the good trajectories to the matrix


    matrix = new_matrix[1:] #removing first line bc it's all zeroes and then renaming it as the matrix so the loop can run again


    # print(matrix)
    print(len(matrix))
#
# plt.plot(time, len_mat)
# plt.show()
#
# print(y_t - y_1)
# print(y_t - y_2)
# print(y_t)











#------------------old stuff ------------------------


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




