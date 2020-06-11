from math import *
import numpy as np
import matplotlib.pyplot as plt

FOV_l   = -20*pi/180 #rad
FOV_r   = +20*pi/180 #rad
Re   = 6371 #km
n_pix = 1001
h = 1000 #km
grav_c = 398600 #km^3 s^-2

spot = np.array([0,Re])
t_0 = 0
dt = 1 #s
theta_0 = 1*pi/180 + pi/2 #rad

# theta_end = -10*pi/180 + pi/2 #rad

# print(thetas*180/pi)



def pixel_det(theta, spot, FOV_l, FOV_r, h,n_pix):

    p = np.array([(Re+h)*cos(theta), (Re+h)*sin(theta)])
    # print(p)
    d_x = - p[0] + spot[0]    #y distance between bright and to s/c
    d_y = - p[1] + spot[1]    #x distance between bright and s/c
    # print(d_x,d_y)
    d = sqrt((d_x)**2 + (d_y)**2) #distance between bright and to s/c
    # print(d)
    angle_pix = np.linspace(FOV_l, FOV_r, n_pix+1)
    # print(len(angle_pix))

    if d_x > 0:
        mu = acos((d**2 + (Re+h)**2 - Re**2)/(2*d*(Re+h)))
    elif d_x <= 0:
        mu = -acos((d ** 2 + (Re + h) ** 2 - Re ** 2) / (2 * d * (Re + h)))
        
    if mu < FOV_r and mu > FOV_l:
        i = 0
        pix = i
        while mu > angle_pix[i]:
            pix = pix+1
            i = i + 1

        # equation of the lines going from s/c to pixel of interest

        eta1 = angle_pix[pix - 1]
        if eta1 > 0:
            m1 = tan(-pi+theta+eta1)
        elif eta1 < 0:
            m1 = tan(theta+eta1)
        else:
            m1 = 9999
        b1 = p[1] - m1 * p[0]

        eta2 = angle_pix[pix]
        if eta2 > 0:
            m2 = tan(-pi+theta+eta2)
        elif eta2 < 0:
            m2 = tan(theta+eta2)
        else:
            m2 = 9999
        b2 = p[1] - m2 * p[0]
        
        # print(eta1*180/pi,eta2*180/pi)

    else:
        pix = 500000
        m1 = 500000
        b1 = 500000
        m2 = 500000
        b2 = 500000


    return pix, m1, b1, m2, b2, mu, p


    # y1 = tan(eta1)*x1 + b
    # y2 = tan(eta2)*x2 + b

# print(pixel_det(theta_0, spot, FOV, h, n_pix))
running = True
t_0 = 0
def get_pixel_data(t_0, running=True):

    t = t_0
    dt = 1 #s
    omega_sat = 1 / sqrt((Re + h) ** 3 / grav_c)  # rad/s

    # pixel_data = np.array(["Time",  "Gradient L1", "Intercept L1", "Gradient L2", "Intercept L2"])
    pixel_data = np.array([0, 0, 0, 0,0,0])

    theta = theta_0

    while running:

        pix, grad1, int1, grad2, int2, mu, p = pixel_det(theta, spot, FOV_l, FOV_r, h, n_pix)

        new_data = np.array([t, grad1, int1, grad2, int2, theta])
        #print(new_data)
        update = np.vstack((pixel_data, new_data))
       # print(update)
        pixel_data = update
        #print(pixel_data)


        dtheta = omega_sat*dt
        theta = theta - dtheta
        t = t + dt


        if grad1 > 100000:
            running = False
            pixel_data = pixel_data[:-1, :]

        #things to make a plot
        if running:
            if grad1*grad2<0:
                x = np.linspace(-1,1,2)
            else:
                x = np.linspace(p[0],0,2)
            y1 = grad1*x+int1
            y2 = grad2*x+int2
            plt.plot(x,y1)
            plt.plot(x,y2)

    # plt.scatter(spot[0],spot[1])
    # plt.title('')
    # plt.show()

    return(pixel_data)




