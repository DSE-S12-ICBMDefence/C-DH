import numpy as np
from scipy import interpolate
import sys

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def density_at_height(altitude):
    data_height = np.array([0,1,2,3,4,5,6,8,10,15,20,30,40,50,60,80,100,150,200,300])*1000
    data_densities = [1.225, 1.112, 1.007, 0.909, 0.819, 0.736, 0.660, 0.526, 0.414, 0.195,
            0.0889, 0.0184, 0.00400, 0.00103, 3.1**-4, 1.85**-5, 5.6**-7, 2.08**-9, 2.54**-10, 1.92*10**-11]
    density_from_height = interpolate.interp1d(data_height, data_densities, fill_value='extrapolate')
    density = density_from_height(altitude)
    return density


def mass_time(missile):
    if missile == 'minuteman':
        total_mass = 30674+3079+907+404
        mass = [total_mass]
        mp = [20411, 6125, 3306]
        tb = [61, 18, 61]
        mb = [3079,907,404]
    elif missile == 'ss18':
        total_mass = sum([147900,13620,36740,4374,287,3179,500,5000])
        mass = [total_mass]
        #print(total_mass)
        mp = [147900, 36740,287]
        tb = [109,161,475]
        mb = [13620,4374,3179]
    else:
        print("Please give either of the following as input: 'minuteman' or 'ss18'")

    burn_time = 0
    time_to_add = 0
    times_list = [0]
    for i in range(0,len(tb)):
        while burn_time < tb[i]:
            burn_time += 1
            total_mass -= (mp[i]/tb[i])
            mass.append(total_mass)
            time_to_add += 1
            times_list.append(time_to_add)
            if burn_time == tb[i]:
                break
        total_mass -= mb[i]
        times_list.append(time_to_add)
        mass.append(total_mass)
        burn_time = 0
    return times_list, mass










