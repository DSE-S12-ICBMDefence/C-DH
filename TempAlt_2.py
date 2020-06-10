import numpy as np
import math as m
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate

alts = np.array([-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80])*1000  #km
temps = [21.5, 15.00, 8.50, 2.00, -4.49, -10.98, -17.47, -23.96, -30.45, -36.94, -43.42,
             -49.90, -56.50, -56.50, -51.60, -46.64, -22.80 , -2.5, -26.13, -53.57, -74.51]  #celcius
temps_k =[]
for temp in temps:
        temps_k.append(temp+ 273.15)

TFromH = sp.interpolate.interp1d(alts, temps_k, fill_value='extrapolate',assume_sorted=True)