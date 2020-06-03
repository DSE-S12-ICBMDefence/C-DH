import math
import numpy as np

def TransformationNadirEarth(lat,lon): #Angles in radians
    ##First transformation from Earth fixed cord system to Orbital cord system

    #Tranformation in z axis
    Trans_in_z = np.array([[np.cos(lon),np.sin(lon),0],
                           [-np.sin(lon),np.cos(lon),0],
                           [0,0,1]])

    #Transformation in y axis
    Trans_in_y = np.array([[-np.sin(lat),0,np.cos(lat)],
                           [0,1,0],
                           [-np.cos(lat),0,-np.sin(lat)]])

    #Rotation sequence: first y, second z
    TransformationEarthNadir = Trans_in_y*Trans_in_z
    ##Inverse due to opposite transformation procedure
    Final_result = np.linalg.inv(TransformationEarthNadir)
    return Final_result

def TransformationOrbitalEarth(yaw,pitch,roll):
    #Transformation in x axis (roll)
    Trans_in_x=np.array([[1,0,0],
                         [0,np.cos(roll),np.sin(roll)],
                         [0,-np.sin(roll),np.cos(roll)]])
    # Transformation in y axis (pitch)
    Trans_in_y=np.array([[np.cos(pitch),0,-np.sin(pitch)],
                         [0,1,0],
                         [np.sin(pitch),0,np.cos(pitch)]])

    # Transformation in z axis (yaw)
    Trans_in_z = np.array([[np.cos(yaw),np.sin(yaw),0],
                           [-np.sin(yaw),np.cos(yaw),0],
                           [0,0,1]])

    Final_result = Trans_in_x*Trans_in_y*Trans_in_z
    return Final_result

def Transformation(lon,lat,yaw,pitch,roll):
    return TransformationNadirEarth(lon,lat)*TransformationOrbitalEarth(yaw,pitch,roll)