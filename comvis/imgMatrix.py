# -*- coding: utf-8 -*-

import numpy as np
import cv2
"""-------- Loading area ------------"""

img = cv2.imread('cropped.jpg',0)            #opening a greyscale picture
cv2.imwrite('cropped.png',img)                #saving it as an .png file

newImg = cv2.imread('cropped.png',0)            #reading the .png file

img = cv2.imread('GreenMiddle.png')             #importing image
#cv2.imshow('newImg',newImg)                    #showing image

pix = cv2.imread('10pix.png')


cv2.imshow('my working image',img)
"""            Helping functions            """
def properties(image):
    print "Shape is ",image.shape
    print "max pixel value is  %i."  %(image.max() )
    print "min pixel value is %i."   %(image.min() )
def printE(image):
    countCol = 0
    countRow = 0
    for col in image:
        countCol +=1
        print col
        for row in col:
            #print row
            countRow +=1
    print "coloums: %i. rows %i " %(countCol,countRow/countCol)
def row(image):
    rows=0
    for col in image:
        for row in col:
            rows +=1
    return rows/coloum(image)
def coloum(image):
    colum = 0
    for col in image:
        colum+=1
    return colum
def corners(image):
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_limit=np.array([60,100,140])
    upper_limit=np.array([100,255,255])
    #threshold
    mask = cv2.inRange(hsv,lower_limit,upper_limit)
    res=cv2.bitwise_and(image,image,mask=mask)
    cv2.imshow('Colours matching corners',res)
    #print "hsv values UpperLeft", hsv[126][400]
    #print "hsv values UpperRight", hsv[100][880]
    #print "hsv values LowerLeft", hsv[393][393]
    #print "hsv values LowerRight", hsv[412][904]
    if cv2.__version__[0]=='3': #For opencv 3.0
       _, contours, hierarchy = cv2.findContours(res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else: #For opencv <3.0
        contours, hierarchy = cv2.findContours(res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



corners(img)





#manuel H159 S 100 V67.5
"""            Workspace                """

#print "HSV COLOR"
#print "RGB color", img[126][400]

#hsvPix = cv2.cvtColor(pix, cv2.COLOR_BGR2HSV)
#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    # Convert BGR to HSV
    # define range of blue color in HSV
#lower_blue = np.array([110,50,50])
#upper_blue = np.array([130,255,255])
    # Threshold the HSV image to get only blue colors
#mask = cv2.inRange(hsv, lower_blue, upper_blue)        #Blue mask
    # Bitwise-AND mask and original image

#cv2.imshow('blue masked',mask)

#res = cv2.bitwise_and(img,img, mask= mask)    #Resulting Blue objects
#cv2.imshow('resulting blue',res)
#img2 = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)





print "coloumns ",coloum(newImg)
print "rows ",row(newImg)
#printE(newImg)
#properties(newImg)



"""####### my mask function #####
cropped = newImg
cv2.imshow('cropped and greyscale',cropped)
print cropped[135][74]            # white
print cropped[236][334]            #black
mask = cropped >30
cropped[mask]= 255
cv2.imshow('re made',cropped)
#printE(cropped)
##############################
"""







cv2.waitKey(0)


