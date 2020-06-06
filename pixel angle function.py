import math as m

def pic_angles(w_bright,h_bright,n_pix_w,n_pix_h,FOV_w,FOV_h):

    FOV_w = FOV_w*m.pi/180
    FOV_h = FOV_h*m.pi/180

    center_width = -(n_pix_w/2-0.5)+(w_bright-1)
    center_height = -(n_pix_h/2-0.5)+(h_bright-1)

    print(center_width)

    ratio_width = center_width/(n_pix_w/2)
    ratio_height = center_height/(n_pix_h/2)
    
    angle_width = m.atan(ratio_width*m.tan(FOV_w/2))*180/m.pi
    angle_height = m.atan(ratio_height*m.tan(FOV_h/2))*180/m.pi    

    return angle_width, angle_height



for w_bright in range(1,5):
    if w_bright != 0:
        print(pic_angles(w_bright,1,4,4,90,90))
