import numpy as np
import math as m
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate


def AvgThurst(missile, stage) :
    g = 9.81 #m/s^2
    if missile == 'minuteman':

        #----stage 1 parameters-------------
        tb_1  = 61 #s
        Isp_1 = 270  # s
        Mp_1  = 20411 #kg
        mb_1  = 3079 #kg

        # ----stage 2 parameters------------
        tb_2  = 18 #s
        Isp_2 = 287 #s
        Mp_2  = 6125 #kg
        mb_2  = 907 #kg

        # ----stage 3 parameters------------
        tb_3  = 61 #s
        Isp_3 = 285 #s
        Mp_3  = 3306 #kg
        mb_3  = 404 #kg

    elif missile == 'SS-18':
        # ----stage 1 parameters-------------
        tb_1  = 109  # s
        Isp_1 = 339  # s
        Mp_1  = 147900  # kg
        mb_1  = 13620  # kg

        # ----stage 2 parameters------------
        tb_2  = 161# s
        Isp_2 = 340  # s
        Mp_2  = 36740  # kg
        mb_2  = 4374  # kg

        # ----stage 3 parameters------------
        tb_3  = 475  # s
        Isp_3 = 309  # s
        Mp_3  = 287 # kg
        mb_3  = 3179# kg

    #---thrust calculation---------------
    T_avg_1 = g * Isp_1 * (Mp_1 / tb_1)
    T_avg_2 = g * Isp_2 * (Mp_2 / tb_2)
    T_avg_3 = g * Isp_3 * (Mp_3 / tb_3)

    if stage == 1:
        return T_avg_1

    elif stage == 2:
        return T_avg_2
    else:
        return T_avg_3


