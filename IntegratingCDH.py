import numpy as np
import math as m
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
from Velocity_Check import pixel_data
from Main_Trajectory import TrajectoryData


def generate_trajectories(rot_alt,rot_angle):
    x, y, h, vx, vy, v = TrajectoryData(rot_alt,rot_angle)
    rot_alts = np.linspace(10000,100000,50)
    rot_angles = np.linspace

def generate_trajectories(rot_alt_step,rot_angle_step):

    rot_alts = np.linspace(10000,100000,rot_alt_step)
    rot_angles = np.linspace(15,40,rot_angle_step)

    temp_x = []
    temp_y = []
    temp_t = []
    for alt in rot_alts:
        for angle in rot_angles:
            x, y, h, vx, vy, v,t = TrajectoryData(alt, angle)
            temp_x.append(x)
            temp_y.append(y)
            temp_t.append(t)


    return temp_x,temp_y,temp_t


def compile_matrix(t,x,y):

    #data_base = np.array([0,0,0])
    #for item in range(len(x)):
    piece = np.array([[t],[x],[y]])
    #print(piece)

    return piece

x,y,t = generate_trajectories(5,2)

t_new = np.array(t)
x_new = np.array(x)
y_new = np.array(y)

lala = compile_matrix(t_new[0],x_new[0],y_new[0])
print(lala)

print(pixel_data)

def velocity_check(pixel_data, piece, x_new):

# pix, grad1, int1, grad2, int2, mu, p = pixel_det(theta, spot, FOV_l, FOV_

    for row in range(len(pixel_data)):
        for i in range(len(x_new)):
        #y = mx+b

            y1 = pixel_data[row, 1]*x_new[i] + pixel_data[row,2]














