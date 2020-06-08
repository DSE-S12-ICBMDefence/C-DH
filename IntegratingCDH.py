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
