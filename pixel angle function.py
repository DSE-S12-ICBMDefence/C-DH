import math as m
import numpy as np

#I made this but I really think it's wrong and that it makes no sense now

def pic_angles(w_bright,h_bright,n_pix_w,n_pix_h,FOV_w,FOV_h):

    FOV_w = FOV_w*m.pi/180
    FOV_h = FOV_h*m.pi/180

    center_width = -(n_pix_w/2-0.5)+(w_bright-1)
    center_height = -(n_pix_h/2-0.5)+(h_bright-1)

    print(center_width)

    ratio_width = center_width/(n_pix_w/2)
    ratio_height = center_height/(n_pix_h/2)
    
    center_beta = m.atan(ratio_width*m.tan(FOV_w/2))*180/m.pi
    center_alpha = m.atan(ratio_height*m.tan(FOV_h/2))*180/m.pi
    center_angles = np.array([center_beta,center_alpha])

    #CREATING THE PIXEL AS A VOLUME IN SPACE
    a_beta = m.atan((-n_pix_w/2+w_bright-1)*m.tan(FOV_w/2))*180/m.pi
    a_alpha = m.atan((-n_pix_w/2+w_bright-1)*m.tan(FOV_h/2))*180/m.pi
    a_angles = np.array([a_beta,a_alpha])
    
    b_beta = m.atan((-n_pix_w/2+w_bright)*m.tan(FOV_w/2))*180/m.pi
    b_alpha = m.atan((-n_pix_w/2+w_bright-1)*m.tan(FOV_h/2))*180/m.pi
    b_angles = np.array([b_beta,b_alpha])
    
    c_beta = m.atan((-n_pix_w/2+w_bright)*m.tan(FOV_w/2))*180/m.pi
    c_alpha = m.atan((-n_pix_w/2+w_bright)*m.tan(FOV_h/2))*180/m.pi
    c_angles = np.array([c_beta,c_alpha])
    
    d_beta = m.atan((-n_pix_w/2+w_bright-1)*m.tan(FOV_w/2))*180/m.pi
    d_alpha = m.atan((-n_pix_w/2+w_bright)*m.tan(FOV_h/2))*180/m.pi
    d_angles = np.array([d_beta,d_alpha])

    return center_angles, a_angles, b_angles, c_angles, d_angles

print(pic_angles(5,5,5,5,90,90))

# for w_bright in range(1,6):
#     if w_bright != 0:
#         print(pic_angles(w_bright,3,5,5,90,90))
