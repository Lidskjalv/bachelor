# Program to identify objects in a photo


#####################################
# last entry: 15/2 - 2017 by TGJ
#####################################
# -*- coding: utf-8 -*-
# Building the basics of the program. import a photo
# Looking blue objects on floor.
#
######################################
import cv2
import numpy as np

#print "Dette er en en python start test"
#Reading in the picture
picture1 = cv2.imread('1.jpg')			#Test pictures
#picture2 = cv2.imread('2.jpg')			#Test pictures
#picture3 = cv2.imread('3.jpg')			#Test pictures
#picture4 = cv2.imread('4.jpg')			#Test pictures

#Showing picture
cv2.imshow('Original',picture1)

################ Test zone ####################

print 'The size of the Original picture is ', picture1.shape

# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
crop_img = picture1[190:450,525:890] 			#rough estimates from picture1

cv2.imshow('cropped image',crop_img)			#Output image

cv2.imwrite('cropped image.jpg' , crop_img)		#Saving the cropped image
    
hsv = cv2.cvtColor(picture1, cv2.COLOR_BGR2HSV)		# Convert BGR to HSV
    # define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

lower_red = np.array([160,50,50])
upper_red = np.array([179,255,255])

    # Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)		#Blue mask
    # Bitwise-AND mask and original image
res = cv2.bitwise_and(picture1,picture1, mask= mask)	#Resulting Blue objects

Rmask = cv2.inRange(hsv, lower_red,upper_red)		#Red mask
Rres = cv2.bitwise_and(picture1,picture1, mask = Rmask)	#Resulting Red objects

cv2.imshow('mask',mask)
#cv2.imshow('res',res)
#cv2.imshow('Red objects',Rres)

######## testing with the cropped image ######
hsv2 = cv2.cvtColor(crop_img , cv2.COLOR_BGR2HSV)	#Transform to HSV
# define range of blue color in HSV
lower_blue2 = np.array([110,50,30])
upper_blue2 = np.array([130,255,255])

lower_red2 = np.array([160,50,50])
upper_red2 = np.array([179,255,255])

mask2 = cv2.inRange(hsv2,lower_blue2,upper_blue2)	#Blue mask
res2= cv2.bitwise_and(crop_img,crop_img,mask = mask2)	#Resulting Blue objects

Rmask2 = cv2.inRange(hsv2, lower_red2,upper_red2)	#Red mask
Rres2 = cv2.bitwise_and(crop_img,crop_img, mask = Rmask2)#Resulting Red objects

total_mask = mask2+Rmask2
total_Res=cv2.bitwise_and(crop_img,crop_img, mask = total_mask)

cv2.imshow('Image with object and corners',total_Res)
cv2.imwrite('All objects.jpg',total_Res)

cv2.imshow('cropped res',res2)
cv2.imshow('cropped Red res',Rres2)



###############################################

#Saving the image


# waiting for keystroke, then closes all windows
cv2.waitKey(0)

#cv2.destroyALLWindows()


