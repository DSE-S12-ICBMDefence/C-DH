import numpy as np
import math as m
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate

#ASSUMPTION: rate of propellant use is constant; all useable propellant is consumed
#during the burn. Empty rocket body is jettisonees adrer the burn out

#----------MASS AS A FUNCTION OF TIME----------------


# note : total mass = usable propellant mass per stage + payload mass

total_mass = 30674 + 3079 + 907 + 404
mass = [total_mass]
Mp = [20411, 6125, 3306]
tb = [61, 18, 61]
mb = [3079, 907, 404]

dtmass = 0.0001
tmasslist = [0,61,61+dtmass,79,79+dtmass,140,140+dtmass]
masslist = [total_mass, total_mass-Mp[0],total_mass-Mp[0]-mb[0],total_mass-Mp[0]-Mp[1]-mb[0],total_mass-Mp[0]-mb[0]-Mp[1]-mb[1],\
    total_mass-Mp[0]-Mp[1]-Mp[2]-mb[0]-mb[1],total_mass-Mp[0]-Mp[1]-Mp[2]-mb[0]-mb[1]-mb[2]]
massfunction = sp.interpolate.interp1d(tmasslist,masslist,fill_value=(masslist[0],masslist[-1]),assume_sorted=True)


def Mass_t(missile,t):
    if missile == 'minuteman':
        total_mass = 20411 + 6125 + 3306 + 200 + 271 + 362  +3079 +907+404   # kg
        Mp = [20411, 6125, 3306]                                             # kg useable propellant mass per stage
        mb = [3079, 907, 404]                                                # kg burnout mass
        tb = [61, (61+18), (61+18+61)]                                       # s
        mp = 200 + 271 + 362                                                 # kg payload mass (shroud + bus + pay)


        #STAGE 1
        if t< tb[0]:
            m = total_mass - Mp[0]*(t/tb[0])
            return m

        #STAGE 2
        elif tb[0]<=t<=tb[1]:
            m = total_mass - Mp[1]*((t-tb[0])/(tb[1]-tb[0]))  - Mp[0] - mb[0]
            return m

        #STAGE 3
        elif tb[1]<t<= tb[2]:
            m = total_mass - Mp[2]*((t-tb[1])/(tb[2]-tb[1])) - Mp[0] - Mp[1] - mb[0] - mb[1]

            return m
        else:
            return total_mass - Mp[0] - Mp[1] - Mp[2] - mb[0] - mb[1] - mb[2]

    elif missile == 'SS-18':
        total_mass = 147900 + 36740 + 287 + 5000 + 500 + 13620 +  4374+3179        # kg
        Mp = [147900, 36740, 287]                                                  # kg useable propellant mass per stage
        mb = [13620, 4374, 3179]                                                   # kg
        tb = [109, (109+161), (109+161+475)]                                       # s
        mp = 5000 + 500                                                            # kg payload mass

        # STAGE 1
        if t < tb[0]:
            m = total_mass - Mp[0] * (t / tb[0])
            return m

         # STAGE 2
        elif tb[0] <= t <= tb[1]:
            m = total_mass - Mp[1]*((t-tb[0])/(tb[1]-tb[0]))  - Mp[0] - mb[0]
            return m

        # STAGE 3
        elif tb[1] < t <= tb[2]:
            m = total_mass - Mp[2]*((t-tb[1])/(tb[2]-tb[1])) - Mp[0] - Mp[1] - mb[0] - mb[1]

            return m
        else:
            return total_mass - Mp[0] - Mp[1] - Mp[2] - mb[0] - mb[1] - mb[2]
#
# mass = []
# times = list(range(0,140))
# for time in times:
#     mass.append(Mass_t('minuteman',time))
#
# plt.plot(times,mass)
# plt.show()
# print(mass)
# print(times)
#

