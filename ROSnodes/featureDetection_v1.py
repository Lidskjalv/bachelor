#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import numpy as np
from array import array
import cv2

"""-------- Loading area ------------"""
#newImg = cv2.imread('cropped.png',0)            #reading the .png file

img = cv2.imread('GreenMiddle.png')             #importing image

"""            Helping functions            """
def properties(image):                            #Prints shape and pixel values
    print "Shape is ",image.shape
    print "max pixel value is  %i."  %(image.max() )
    print "min pixel value is %i."   %(image.min() )
def printE(image):                                #Prints the elements in the picture
    countCol = 0
    countRow = 0
    for col in image:
        countCol +=1
        print col
        for row in col:
            #print row
            countRow +=1
    print "coloums: %i. rows %i " %(countCol,countRow/countCol)
def row(image):                                   #Prints the # of rows
    rows=0
    for col in image:
        for row in col:
            rows +=1
    return rows/coloum(image)
def coloum(image):                                #Prints the # of coloums
    colum = 0
    for col in image:
        colum+=1
    return colum
def autoCrop(image):                              #Cut the usable workspace from image
    xlist=[]
    ylist=[]
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_limit=np.array([60,100,140])             #threshold
    upper_limit=np.array([100,255,255])            #threshold
    mask = cv2.inRange(hsv,lower_limit,upper_limit)#masking
    res=cv2.bitwise_and(image,image,mask=mask)     #result after masking
    cv2.imwrite('maskedCorners.png',res)           #saving the picture
    #print "hsv values UpperLeft", hsv[126][400]
    #print "hsv values UpperRight", hsv[100][880]
    #print "hsv values LowerLeft", hsv[393][393]
    #print "hsv values LowerRight", hsv[412][904]
    tmp = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)      #coverting resulting into color-scale
    bwimg = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)   #converting colorpic into GREY-scale
    #cv2.imwrite('greyCorn.png',bwimg)              #output greyscale of matching color found
#Finding coherent elements
    if cv2.__version__[0]=='3': #For opencv 3.0
       _, contours, hierarchy = cv2.findContours(bwimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else: #For opencv <3.0
        contours, hierarchy = cv2.findContours(bwimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        areal = cv2.contourArea(cnt)
        print "areal ", areal
        if(areal)>1:
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])                ## ???
            cy = int(M['m01']/M['m00'])                ## ???

        if(areal) >12:
            #print "im in"
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])                ## ???
            cy = int(M['m01']/M['m00'])                ## ???

            xlist.append(cx)                    #list containing center x coord
            ylist.append(cy)                    #list containing center y coord
            #print "length", len(xlist)
            ly = min(ylist)
            hy =max(ylist)
            lx=min(xlist)
            hx=max(xlist)
    print "hy = ", hy
    print "xlist", xlist
    print "lx %i , hx %i     ly %i , hy %i" %(lx,hx,ly,hy)
    crop_img = image[ly:hy,lx:hx]
    cv2.imshow('cropped image',crop_img)
    return crop_img

def markCorners(image):                           #Marks WS corners in image
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_limit=np.array([60,100,140])             #threshold
    upper_limit=np.array([100,255,255])            #threshold
    mask = cv2.inRange(hsv,lower_limit,upper_limit)#masking
    res=cv2.bitwise_and(image,image,mask=mask)     #result after masking
    cv2.imshow('Colours matching corners',res)     #showing matching colors
    cv2.imwrite('maskedCorners.png',res)           #saving the picture
    tmp = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)      #coverting resulting into color-scale
    bwimg = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)   #converting colorpic into GREY-scale
    #cv2.imshow('grey corners',bwimg)
    cv2.imwrite('greyCorn.png',bwimg)              #output greyscale of matching color found
#Finding coherent elements
    if cv2.__version__[0]=='3': #For opencv 3.0
       _, contours, hierarchy = cv2.findContours(bwimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else: #For opencv <3.0
        contours, hierarchy = cv2.findContours(bwimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        areal = cv2.contourArea(cnt)
        print "areal ", areal
        if(areal)>1:
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])                ## ???
            cy = int(M['m01']/M['m00'])                ## ???

            # Print et sigtekorn der markerer elementet. (se handout)
            # <ret disse linjer>
            cv2.circle(image, (cx, cy), 8, (255, 0, 255), -1)
            cv2.circle(image, (cx, cy), 20, (255, 0, 255), 4)
            cv2.line(image, (0, cy), (1000, cy), (255, 0, 255), 4)
            cv2.line(image, (cx, 0), (cx, 1000), (255, 0, 255), 4)
            # </ret disse linjer>
            cv2.imshow('Cross airs2',image)

def outI(image):                                  #Prints image
    cv2.imshow('print funk',image)

def makeMatrix(image):                            #Makes a .txt file acordingly to the threshold values
    tmp = image
    if tmp.any() >60:
        print "im in"
        image[tmp]=255
    elif tmp.any() <=60:
        image[tmp]=0
        print "im in elif"
    #cv2.imshow('masking',image)
    np.savetxt('matrix.txt',image,fmt='%1d',header='%i\n%i\n%i\n%i' %(row(image),coloum(image),50,50),comments='')##missing robot pos 50 ,50
    #np.savetxt('colorScale.txt',image,fmt='%1d',header='%i\n%i\n%i\n%i' %(row(image),coloum(image),50,50),comments='')


def findRed(image):                               #Finds Red in image
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_limit=np.array([0,100,140])             #threshold
    upper_limit=np.array([20,255,255])            #threshold
    mask = cv2.inRange(hsv,lower_limit,upper_limit)#masking
    res=cv2.bitwise_and(image,image,mask=mask)     #result after masking
    #outI(res)
    outI(mask)
    return mask

def save(image):
    cv2.imwrite('saved.png',image)

def greyScale(image):
    tmp = cv2.cvtColor(image,cv2.COLOR_HSV2BGR)      #coverting resulting into color-scale
    grey = cv2.cvtColor(tmp,cv2.COLOR_BGR2GRAY)
    return grey

def colorScale(image):
    image[image == 255] = 7

"""-------- ROS controls -----------"""
def talker():
    pub = rospy.Publisher('map',String, queue_size = 10) #topic=chatter
    rospy.init_node('featureDetection',anonymous=False)                #NOT a unique name
    rate = rospy.Rate(1) # 1 hz                              #rate of publishing
    """            Workspace                """
    cropped=autoCrop(img)                            # Returns a picture which is cropped to fit
    obj=findRed(cropped)
    #properties(obj)
    #colorScale(obj)
    #save(obj)
    colorScale(obj)
    makeMatrix(obj)
    if not rospy.is_shutdown():
        file_obj= open("matrix.txt","r")                #Read-only matrix.txt
        r = file_obj.read()                                 #reads the whole txt 1 line a time
        #rospy.loginfo(r)                                    #logs info in terminal
        pub.publish(r)                                      #publishes msg
        rate.sleep()                                        #sleeps to adjust rate()

if __name__ == '__main__':
    try:

        talker()
    except rospy.ROSInterruptException:
        pass




cv2.waitKey(0)
