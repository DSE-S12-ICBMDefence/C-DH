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
# from Velocity_Check import pixel_det
# from Velocity_Check import pixel_data

#----------SOLVING EOMs USING EULERS FORWARD INTEGRATION----------------------

#making the missile do a thing
rot_alt = 14000    #m
rot_angle = -15



#---parameters
Re = 6370*1000                   #m   #radius of the Earth
G = 6.67*10**(-20)*1000**3       #m^3s^-2 #gravitational constant
Me = 5.97*10**24                 #kg   #mass of the Earth
A_m = m.pi*0.25*1.68**2          #m^2 cross sectional area minutemann
A_s = m.pi*0.25*3.05**2          #m^2 cross sectional area ss-18

#x and y coordinated are measured from the center of the Earth
density_alt = density_at_height(50)    #input in km; outputs density in kg/m^3

#NO LONGER USED
# #----------SUPPLEMENTARY FUNCTION TO RETRIEVE INTERPOLATED MISSILE MASS-----------
# time_m,  mass_m  = mass_time('minuteman')
# time_ss, mass_ss = mass_time('ss18')
# def collect_mass(time,mass, t):
#     closest_mass = sp.interpolate.interp1d(time, mass, fill_value='extrapolate')
#
#     M = closest_mass(t)
#
#     return M

#---------SUPPLEMENTARY FUNCTION TO RETRIEVE CORRECT STAGE THRUST INPUT TIME-------
def collect_thrust(missile, t):
    if missile == 'minuteman':
        if t<61 :
            return AvgThurst('minuteman', 1)
        elif 61<=t<79:
            return AvgThurst('minuteman', 2)
        elif 79<=t<140:
            return AvgThurst('minuteman', 3)
        else:
            return 0

    elif missile == 'ss-18':
        if t<109 :
            return AvgThurst('ss-18', 1)
        elif 109<=t<270:
            return AvgThurst('ss-18', 2)
        elif 270<=t<745:
            return AvgThurst('ss-18', 3)
        else:
            return 0

def mtomach(v,h):
    R = 8.314
    gamma = 1.4
    a = m.sqrt(gamma*R*Temp(h))

    return (v/a)

#----------------SETTING UP DIFFERENTIAL EQUATIONS----------------------------
#EOMS

#missile origin
x0 = 0
y0 = Re

def TrajectoryData(rot_alt,rot_angle,x0,y0):

    turn = False

    dt = 1 #s

     #initial conditions
    # x and y coordinates are measured from the center of the earth
    v0 = 0.001       #km/s # starting with a neglibele initial  velocity
    phi0 = 0
    # x0 = 0
    # y0 = Re   # do we integrate till the y coordinate is Re again? that makes sense
    h0 = 0 #km

    #Initially there would be no horizontal velocity or accellleration as the missile
    #typically has a very small angle of attack

    t0 = 0.0
    vx0 = v0*m.sin(phi0)
    vy0 = v0*m.cos(phi0)


    dvx0 = ((collect_thrust('minuteman',0) - 0.5*density_at_height(0.0)*A_m*Cd(0)*v0**2)/Mass_t('minuteman',0))\
           *(vx0/v0) - (G*Me*x0)/(x0**2+y0**2)**(3/2)

    dvy0 = ((collect_thrust('minuteman',0) - 0.5*density_at_height(0.0)*A_m*Cd(0)*v0**2)/Mass_t('minuteman',0))\
           *(vy0/v0) - (G*Me*y0)/(x0**2+y0**2)**(3/2)



    #you need to convert the input for the Cd approximate to mach
    # create a temperture altitude tool

    #the EOMs need to be integrated till z = Re - wtf
    y   = [y0]       #km
    x   = [x0]       #km
    h   = [h0]       #km
    v   = [v0]       #km/s
    vx  = [vx0]      #km/s
    vy  = [vy0]      #km/s
    dvx = [dvx0]     #km/s^2
    dvy = [dvy0]     #km/s^2
    timestamp = [t0] #s

    i = 0
    t = t0
    while t<= 90 and h[i]>-1:
        t = timestamp[i] +  dt
        timestamp.append(t)



        if h[i]<=80000:
            dvx_new =  ((collect_thrust('minuteman',t) - 0.5*density_at_height(h[i])*A_m*Cd(mtomach(v[i],h[i]))*v[i]**2)/Mass_t('minuteman',t))\
               *(vx[i]/v[i]) - (G*Me*x[i])/(x[i]**2+y[i]**2)**(3/2)

            dvx.append(dvx_new)

            dvy_new = ((collect_thrust('minuteman', t) - 0.5 * density_at_height(h[i]) * A_m * Cd(mtomach(v[i], h[i])) * v[
                i] ** 2) / Mass_t('minuteman',t)) \
                      * (vy[i] / v[i]) - (G * Me * y[i]) / (x[i] ** 2 + y[i] ** 2) ** (3 / 2)

            dvy.append(dvy_new)

        else: #-----------beyond 80km drag becomes neglibible thus we set Cd = 0
            dvx_new = ((collect_thrust('minuteman', t) - 0.5 * density_at_height(h[i]) * A_m * 0 * v[
                i] ** 2) / Mass_t('minuteman',t)) \
                      * (vx[i] / v[i]) - (G * Me * x[i]) / (x[i] ** 2 + y[i] ** 2) ** (3 / 2)

            dvx.append(dvx_new)

            dvy_new = ((collect_thrust('minuteman', t) - 0.5 * density_at_height(h[i]) * A_m * 0 * v[
                i] ** 2) / Mass_t('minuteman',t)) \
                      * (vy[i] / v[i]) - (G * Me * y[i]) / (x[i] ** 2 + y[i] ** 2) ** (3 / 2)

            dvy.append(dvy_new)

        vx_new = vx[i] + dvx_new*dt
        vy_new = vy[i] + dvy_new * dt


        x_new = x[i] + vx_new*dt
        y_new = y[i] + vy_new*dt

        h_new = m.sqrt(x_new**2 + y_new**2) - Re

        v_new = m.sqrt(vx_new**2 + vy_new**2)


        # #trying to incorporate a control input for trajectory
        if h[i] > rot_alt and turn == False:
            phi_new = rot_angle *(m.pi/180)
            vx_new = v_new*m.sin(phi_new)
            vy_new = v_new * m.cos(phi_new)
            turn=True


        x.append(x_new)
        y.append(y_new)
        h.append(h_new)
        vx.append(vx_new)
        vy.append(vy_new)
        v.append(v_new)


        i+=1
    return [x,y,h,vx,vy,v,timestamp]







