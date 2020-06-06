from math import *
import numpy as np
import matplotlib.pyplot as plt

FOV   = 20*pi/180 #rad
Re   = 6371 #km
n_pix = 3
h = 1000 #km
grav_c = 398600 #km^3 s^-2

spot = np.array([0,Re])
theta_0 = 0*pi/180 + pi/2 #rad
t_0 = 0
dt = 1 #s
# theta_end = -10*pi/180 + pi/2 #rad

# print(thetas*180/pi)



def pixel_det(theta, spot, FOV, h,n_pix):

    p = np.array([(Re+h)*cos(theta), (Re+h)*sin(theta)])
    # print(p)
    d_x = - p[0] + spot[0]    #y distance between bright and to s/c
    d_y = - p[1] + spot[1]    #x distance between bright and s/c
    # print(d_x,d_y)
    d = sqrt((d_x)**2 + (d_y)**2) #distance between bright and to s/c
    # print(d)
    angle_pix = np.linspace(-FOV / 2, FOV / 2, n_pix+1)
    # print(len(angle_pix))

    if d_x > 0:
        mu = acos((d**2 + (Re+h)**2 - Re**2)/(2*d*(Re+h)))
    elif d_x <= 0:
        mu = -acos((d ** 2 + (Re + h) ** 2 - Re ** 2) / (2 * d * (Re + h)))
    print(mu)
    if mu < FOV/2 and mu > -FOV/2:
        i = 0
        pix = i
        while mu > angle_pix[i]:
            pix = pix+1
            i = i + 1

        # equation of the lines going from s/c to pixel of interest

        eta1 = angle_pix[pix - 1]
        m1 = -tan(pi-theta + abs(eta1))
        b1 = p[1] - m1 * p[0]

        eta2 = angle_pix[pix]
        m2 = tan(theta - abs(eta2))
        b2 = p[1] - m2 * p[0]

    else:
        pix = 500000
        m1 = 500000
        b1 = 500000
        m2 = 500000
        b2 = 500000


    return pix, m1, b1, m2, b2, mu


    # y1 = tan(eta1)*x1 + b
    # y2 = tan(eta2)*x2 + b




running = True
t = t_0
omega_sat = 1 / sqrt((Re + h) ** 3 / grav_c)  # rad/s

# pixel_data = np.array(["Time",  "Gradient L1", "Intercept L1", "Gradient L2", "Intercept L2"])
pixel_data = np.array([0, 0, 0, 0,0])

theta = theta_0

while running:

    pix, grad1, int1, grad2, int2, mu = pixel_det(theta, spot, FOV, h, n_pix)

    new_data = np.array([t, grad1, int1, grad2, int2])

    update = np.vstack((pixel_data, new_data))

    pixel_data = update



    dtheta = omega_sat*dt
    theta = theta - dtheta
    t = t_0 + dt

    if grad1 > 100000:
        running = False
        pixel_data = pixel_data[:-1, :]

x = np.linspace(0,300,10)

m1 = pixel_data[1:,1]
b1 = pixel_data[1:,2]
m2 = pixel_data[1:,3]
b2 = pixel_data[1:,4]

funys = []
for i in range(len(m1)):

    y2 = m2[i]*x + b2[i]
    funys.append(y2)

for plot in funys:
    plt.plot(x,plot)
plt.show()

# for i in range(len(m2)):
#
#     y2 = m2[i]*x + b2[i]
#
#     plt.plot(x,y2)
#     plt.show()
#
#
# ytes = []
# for i in range(len(x)):
#     y = m1[i]*x[i] + b1[i]
#     ytes.append(y)
#
# plt.plot(x,ytes)
# plt.show()
#
# for i in range(len(m1)):
#     y1 = []
#     y1 = m1[i] * x + b1[i]



# def check_trajectory ():
