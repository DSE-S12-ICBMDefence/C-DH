import numpy as np
import math as m
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate

#data on V2 missile is going to be used to return the appropriate Cd value
V2_v = 0.0, 0.5, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0
V2_cd = 0.25, 0.18, 0.28, 0.36, 0.26, 0.17, 0.15, 0.14, 0.12, 0.11, 0.10
CDfromM = sp.interpolate.interp1d(V2_v, V2_cd, fill_value='extrapolate',assume_sorted=True)





