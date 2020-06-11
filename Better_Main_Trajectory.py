import numpy as np
import math as m
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate
from AverageThrust_2 import AvgThurst
from CdEstimator_2 import CDfromM
#from ISA_2 import mass_time
from ISA_2_2 import density_from_height
from TempAlt_2 import TFromH
from Mass_extract_2_2 import massfunction
# from Velocity_Check import pixel_det
# from Velocity_Check import pixel_data
import time

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

tlist = [0,61,79,140,1000000]
thrustlist = [AvgThurst('minuteman', 1),AvgThurst('minuteman', 1),AvgThurst('minuteman', 2),AvgThurst('minuteman', 3),0]
thrustfunction = sp.interpolate.interp1d(tlist,thrustlist,kind='next',fill_value='extrapolate',assume_sorted=True)

def mtomach(v,h):
    R = 8.314
    gamma = 1.4
    a = gamma*R*TFromH(h)
    return v/a

#----------------SETTING UP DIFFERENTIAL EQUATIONS----------------------------
#EOMS
#missile origin
x0 = 0
y0 = Re

def TrajectoryData(rot_alt,rot_angle,x0,y0):

    turn = False

    dt = 1 #s
    tmax = 140 #s
    Niter = int(tmax / dt) + 1
    nrot = np.size(rot_angle)

     #initial conditions
    # x and y coordinates are measured from the center of the earth
    v0 = np.ones((1,nrot))*0.001       #km/s # starting with a neglibele initial  velocity
    phi0 = 0
    # x0 = 0
    # y0 = Re   # do we integrate till the y coordinate is Re again? that makes sense
    h0 = np.zeros((1,nrot)) #km

    #Initially there would be no horizontal velocity or accellleration as the missile
    #typically has a very small angle of attack

    t0 = 0.0
    vx0 = v0*np.sin(phi0)
    vy0 = v0*np.cos(phi0)

    dvx0 = ((thrustfunction(0) - 0.5*density_from_height(0.0)*A_m*CDfromM(0)*v0**2)/massfunction(0))\
           *(vx0/v0) - (G*Me*x0)/(x0**2+y0**2)**(3/2)

    dvy0 = ((thrustfunction(0) - 0.5*density_from_height(0.0)*A_m*CDfromM(0)*v0**2)/massfunction(0))\
           *(vy0/v0) - (G*Me*y0)/(x0**2+y0**2)**(3/2)



    #you need to convert the input for the Cd approximate to mach
    # create a temperture altitude tool

    # #the EOMs need to be integrated till z = Re - wtf
    # y   = [y0]       #km
    # x   = [x0]       #km
    # h   = [h0]       #km
    # v   = [v0]       #km/s
    # vx  = [vx0]      #km/s
    # vy  = [vy0]      #km/s
    # dvx = [dvx0]     #km/s^2
    # dvy = [dvy0]     #km/s^2
    # timestamp = [t0] #s

    y = np.empty((Niter,nrot))
    x = np.empty((Niter,nrot))
    h = np.empty((Niter,nrot))
    v = np.empty((Niter,nrot))
    vx = np.empty((Niter,nrot))
    vy = np.empty((Niter,nrot))
    dvx = np.empty((Niter,nrot))
    dvy = np.empty((Niter,nrot))
    timestamp = np.empty((Niter,nrot))

    y[0,:] = y0
    x[0,:] = x0
    h[0,:] = h0
    v[0,:] = v0
    vx[0,:] = vx0
    vy[0,:] = vy0
    dvx[0,:] = dvx0
    dvy[0,:] = dvy0
    timestamp[:,:] = np.linspace(0,tmax,Niter)[:,None]

    i = 0
    for t in timestamp[:-1,0]:
        if h[i,0]<=80000:
            Thrust = thrustfunction(t)
            Drag = 0.5*density_from_height(h[i,:])*A_m*CDfromM(mtomach(v[i,:],h[i,:]))*v[i,:]**2
            mass = massfunction(t)
            gravity = (G*Me)/(x[i,:]**2+y[i,:]**2)**(3/2)
            dvx_new = (Thrust-Drag)/mass * vx[i,:]/v[i,:] - gravity*x[i,:]
            dvy_new = (Thrust-Drag)/mass * vy[i,:]/v[i,:] - gravity*y[i,:]

            # dvx_new =  ((thrustfunction(t) - 0.5*density_from_height(h[i])*A_m*Cd(mtomach(v[i],h[i]))*v[i]**2)/massfunction(t))\
            #    *(vx[i]/v[i]) - (G*Me*x[i])/(x[i]**2+y[i]**2)**(3/2)

            dvx[i+1,:] = dvx_new

            # dvy_new = ((thrustfunction(t) - 0.5 * density_from_height(h[i]) * A_m * Cd(mtomach(v[i], h[i])) * v[
            #     i] ** 2) / massfunction(t)) \
            #           * (vy[i] / v[i]) - (G * Me * y[i]) / (x[i] ** 2 + y[i] ** 2) ** (3 / 2)

            dvy[i+1,:] = dvy_new

        else: #-----------beyond 80km drag becomes neglibible thus we set Cd = 0
            Thrust = thrustfunction(t)
            mass = massfunction(t)
            gravity = (G*Me)/(x[i,:]**2+y[i,:]**2)**(3/2)
            dvx_new = (Thrust)/mass * vx[i,:]/v[i,:] - gravity*x[i,:]
            dvy_new = (Thrust)/mass * vy[i,:]/v[i,:] - gravity*y[i,:]

            # dvx_new = ((thrustfunction(t) - 0.5 * density_from_height(h[i]) * A_m * 0 * v[
            #     i] ** 2) / massfunction(t)) \
            #           * (vx[i] / v[i]) - (G * Me * x[i]) / (x[i] ** 2 + y[i] ** 2) ** (3 / 2)

            dvx[i+1,:] = dvx_new

            # dvy_new = ((thrustfunction(t) - 0.5 * density_from_height(h[i]) * A_m * 0 * v[
            #     i] ** 2) / massfunction(t)) \
            #           * (vy[i] / v[i]) - (G * Me * y[i]) / (x[i] ** 2 + y[i] ** 2) ** (3 / 2)

            dvy[i+1,:] = dvy_new

        vx_new = vx[i,:] + dvx_new*dt
        vy_new = vy[i,:] + dvy_new*dt


        x_new = x[i,:] + vx_new*dt
        y_new = y[i,:] + vy_new*dt

        h_new = np.sqrt(x_new**2 + y_new**2) - Re

        v_new = np.sqrt(vx_new**2 + vy_new**2)


        # # #trying to incorporate a control input for trajectory
        if h[i,0] > rot_alt and turn == False:
            phi_new = rot_angle * np.pi/180
            vx_new = v_new*np.sin(phi_new)
            vy_new = v_new*np.cos(phi_new)
            turn=True


        x[i+1,:] = x_new
        y[i+1,:] = y_new
        h[i+1,:] = h_new
        vx[i+1,:] = vx_new
        vy[i+1,:] = vy_new
        v[i+1,:] = v_new


        i+=1
    return [x,y,h,vx,vy,v,timestamp]





