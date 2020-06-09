import math as m
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sp

# inputs
#### NOTE!!!! The satellite that is "moving" is sat 2. Sat 1 is the one that is "looking down"

h = 1000    # Altitude in km
long1 = 65.2	# Longitude of satellite #1 in degrees
long2 = 90	# Longitude of satellite #2 in degrees
Psize = 10	# Pixel size in arcseconds
x_pixel = 6378*m.cos(88*m.pi/180) # X-coordinate of the bright pixel
y_pixel = 6378*m.sin(88*m.pi/180) # Y-coordinate of the bright pixel

# Constants
Re = 6378	# Radius of Earth in km

# Calculate coordinates

R = Re + h 						# Orbitl radius
long1 = long1*m.pi/180			# Change from degrees to rad
long2 = long2*m.pi/180			# Change from degrees to rad
x1 = R*m.cos(long1) 	        # X-coordinate of the satellite #1
y1 = R*m.sin(long1)				# Y-coordinate of the satellite #1
x2 = R*m.cos(long2)				# X-coordinate of the satellite #2
y2 = R*m.sin(long2)				# Y-coordinate of the satellite #2


def CalcLines(a1u,a1l,a2u,a2l,Psize,x1u,y1u,x1l,y1l,x2u,y2u,x2l,y2l):
	
	
	# Calculate intersection of lines
	
	# Upper line from sat 1
	m1u = m.tan(a1u)
	c1u = y1u - m1u*x1u
	
	# Lower line from sat 1
	m1l = m.tan(a1l)
	c1l = y1l - m1l*x1l
	
	
	# Upper line from sat 2
	m2u = m.tan(a2u)
	c2u = y2u - m2u*x2u
	
	# Lower line from sat 2
	m2l = m.tan(a2l)
	c2l = y2l - m2l*x2l
	
	
	# Initial point for defraction
	
	# Calculating intersections
	
	Auu = np.array([[-m1u,1],[-m2u,1]])
	Cuu = np.array([[c1u],[c2u]])
	x_uu,y_uu = np.linalg.solve(Auu,Cuu)
	
	Aul = np.array([[-m1u,1],[-m2l,1]])
	Cul = np.array([[c1u],[c2l]])
	x_ul,y_ul = np.linalg.solve(Aul,Cul)
	
	Alu = np.array([[-m1l,1],[-m2u,1]])
	Clu = np.array([[c1l],[c2u]])
	x_lu,y_lu = np.linalg.solve(Alu,Clu)
	
	All = np.array([[-m1l,1],[-m2l,1]])
	Cll = np.array([[c1l],[c2u]])
	x_ll,y_ll = np.linalg.solve(All,Cll)
	
	# Maximum distances between points	 
	dx = max(abs(x_uu - x_ul),abs(x_uu - x_lu),abs(x_uu - x_ll),abs(x_ll - x_ul),abs(x_ll - x_lu),abs(x_lu - x_ul))
			
	dy = max(abs(y_uu - y_ul),abs(y_uu - y_lu),abs(y_uu - y_ll),abs(y_ll - y_ul),abs(y_ll - y_lu),abs(y_lu - y_ul))
	
	
	# "Mid" point of intersections
	
	x_mis,y_mis = np.array([x_ll + dx/2,y_lu - dy/2])
	

	return dx,dy,x_mis,y_mis

		
		


def PixelInter(Type,x1,y1,x2,y2,x_pixel,y_pixel,Psize,alpha1_e,x1_e,y1_e,alpha2_e,x2_e,y2_e,n): 
	# Constants
	Re = 6378
	
	# Position of Pixel
	
	R_pixel = m.sqrt(x_pixel**2 + y_pixel**2)		# Position of pixel on orbit
	long_pixel = m.atan(y_pixel/x_pixel)			# Long position of pixel
	
	x1 = x1 + x1_e 						# New coordinate
	y1 = y1 + y1_e 						# New coordinate
	x2 = x2 + x2_e 						# New coordinate
	y2 = y2 + y2_e 						# New coordinate
	
	gamma1 = long_pixel - long1 			#	Earth angle for sat 1
	gamma2 = long2 - long_pixel 			# 	Earth angle for sat 2
	l1 = m.sqrt(R**2 + R_pixel**2 - 2*Re*R*m.cos(gamma1))	# Length to the bright pixel from sat 1
	l2 = m.sqrt(R**2 + R_pixel**2 - 2*Re*R*m.cos(gamma2))	#Length to the bright pixel from sat 1
	alpha1 = m.asin((R_pixel/l1)*m.sin(gamma1)) + alpha1_e*m.pi/180			# Angle at which satellite #2 is looking
	alpha2 = m.asin((R_pixel/l2)*m.sin(gamma2)) + alpha2_e*m.pi/180			# Angle at which satellite #2 is looking
	
	a1u = 3/2*m.pi - (alpha1 - 0.5*Psize/3600*m.pi/180)				# Upper angle of the line from sat 1 to pixel
	a1l = 3/2*m.pi - (alpha1 + 0.5*Psize/3600*m.pi/180)				# Lowe angle of the line froom sat 1 to pixel
	
	a2u = 3/2*m.pi + alpha2 + 0.5*Psize/3600*m.pi/180		# Upper angle of the line from sat 2 to pixel
	a2l = 3/2*m.pi + alpha2 - 0.5*Psize/3600*m.pi/180		# Lower angle of the line from sat 2 to pixel

	if Type == 1:
		pos_original = CalcLines(a1u,a1l,a2u,a2l,Psize,x1,y1,x1,y1,x2,y2,x2,y2)
		return pos_original
	
	
	# Refraction shit
	
	if Type == 2:
		h_refract = Re + 50
#		alpha11 = m.asin(m.sin(alpha1)/n)											# Angle with refraction for sat 1
#		alpha21 = m.asin(m.sin(alpha2)/n)											# Angle with refraction for sat 2
		
		
		a1u1 = m.asin(m.sin((alpha1 - 0.5*Psize/3600*m.pi/180)/n))				# Lowe angle of the line froom sat 1 to pixel
		a1l1 = m.asin(m.sin((alpha1 + 0.5*Psize/3600*m.pi/180)/n))				# Upper angle of the line from sat 1 to pixel
		
	
		a2u1 = m.asin(m.sin((alpha2 + 0.5*Psize/3600*m.pi/180)/n))		# Upper angle of the line from sat 2 to pixel
		a2l1 = m.asin(m.sin((alpha2 - 0.5*Psize/3600*m.pi/180)/n))		# Lower angle of the line from sat 2 to pixel
	

		x_subs1u = (y1-(h_refract))*m.tan(a1u1)
		x_refract1u = x1-x_subs1u
		x_subs1l = (y1-(h_refract))*m.tan(a1l1)
		x_refract1l = x1-x_subs1l
		x_subs2u = (y2-(h_refract))*m.tan(a2u1)
		x_refract2u = x2+x_subs2u
		x_subs2l = (y2-(h_refract))*m.tan(a2l1)
		x_refract2l = x2+x_subs2l
		
		a1u2 = 3/2*m.pi - a1u1				# Upper angle of the line from sat 1 to pixel
		a1l2 = 3/2*m.pi - a1l1				# Lowe angle of the line froom sat 1 to pixel
	
		a2u2 = 3/2*m.pi + a2u1		# Upper angle of the line from sat 2 to pixel
		a2l2 = 3/2*m.pi + a2l1		# Lower angle of the line from sat 2 to pixel

		
		pos_refraction = CalcLines(a1u2,a1l2,a2u2,a2l2,Psize,x_refract1u,h_refract,x_refract1l,h_refract,x_refract2u,h_refract,x_refract2l,h_refract)
		
		return pos_refraction
	
	
	
#	plt.plot(x_lu,y_lu,'ko')
#	plt.plot(x_ll,y_ll,'bo')
#	plt.plot(x_uu,y_uu,'ro')
#	plt.plot(x_ul,y_ul,'mo')
#	plt.plot(x_mis,y_mis,'co')
#	plt.show()
	






# Error calculations
pos_original = PixelInter(2,x1,y1,x2,y2,x_pixel,y_pixel,Psize,0,0,0,0,0,0,1) 		# Original coordinates
x_errors = np.array([])
y_errors = np.array([])
x_coord = np.array([])
y_coord = np.array([])
#delta_alpha1 = np.array([])
#delta_alpha2 = np.array([])
n = 1.00079										# Refractive index
for i in range(100):
	alpha1_e = np.random.normal(0,0.005)
	alpha2_e = np.random.normal(0,0.005)
	print(i)
	for j in range(10):
		x1_error = np.random.normal(0,0.005)
		x2_error = np.random.normal(0,0.005)
		for k in range(10):
			y1_error = np.random.normal(0,0.005)
			y2_error = np.random.normal(0,0.005)
			pos_new = PixelInter(1,x1,y1,x2,y2,x_pixel,y_pixel,Psize,alpha1_e,x1_error,y1_error,alpha2_e,x2_error,y2_error,n)
						
			# Calculate differences
			x_diff = max(abs((pos_original[2] + pos_original[0])-pos_new[2]),abs((pos_original[2] - pos_original[0])-pos_new[2]))
			y_diff = max(abs((pos_original[3] + pos_original[1])-pos_new[3]),abs((pos_original[3] - pos_original[1])-pos_new[3]))
			x_coord = np.append(x_coord,pos_new[2])
			y_coord = np.append(y_coord,pos_new[3])
#			delta_alpha1 = np.append(delta_alpha1,(pos_new[4]-pos_new[5]))
#			delta_alpha2 = np.append(delta_alpha2,(pos_new[6]-pos_new[7]))
			x_errors = np.append(x_errors,x_diff)
			y_errors = np.append(y_errors,y_diff)
			
print(max(x_errors))
print(max(y_errors))

#plt.hist(y_errors,1000)
#plt.show()


	

