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
from Main_Trajectory import TrajectoryData




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
            for theta_x in x_trans:
                for dt in delta_t:

                    x0 = Re * cos(theta_x)
                    y0 = Re * sin(theta_x)

                    if y0 != 0:

                        x, y, h, vx, vy, v,t = TrajectoryData(alt, angle+ theta_x - pi/2,x0,y0,theta_x - pi/2)


                        temp_x.append(x)
                        temp_y.append(y)
                        temp_t.append(t-dt)


    return temp_x,temp_y,temp_t

x,y,t = generate_trajectories(5,2,5, 10)
# for i in range(len(x)):
#     plt.plot(x[i],y[i])
# plt.show()
