#!/usr/bin/env python
"""OpenCV feature detectors with ros Image Topics in python.

This example subscribes to a ros topic containing sensor_msgs
Image. It converts the Image into a numpy.ndarray,
then detects and marks features in that image. It finally displays
and publishes the new image - again as Image topic.
"""
__author__ =  'Thor Jensen'
__version__=  '0.1'

# Python libs
import sys, time
import math

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

# OpenCV
import cv2
# Ros libraries
import roslib
import rospy

# Ros Messages
import message_filters

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

#app import
from feature_detection.msg import coord
from markerlocator.msg import markerpose

# Globals
VERBOSE=False
timestamp=[]
x=[]            #List of x coord from corners
y=[]            #List of y coord from corners
bridge=CvBridge()
mark4Flag = False
mark5Flag = False
mark6Flag = False
mark8Flag = False
targetFlag = False
frobitFlag = False
fx = 0            #frobits x coord
fy = 0            #frobits y coord
tx = 0            #targets x coord
ty = 0            #targets y coord

color_img= np.ndarray


def markerCrop(xList,yList,image):
    hx = int(max(xList))
    lx = int(min(xList))
    hy = int(max(yList))
    ly = int(min(yList))
    image[ly:hy,lx:hx]
    return cropped


def autoCrop(image):                              #Cut the usable workspace from image
    xlist=[]
    ylist=[]
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_limit=np.array([60,100,140])             #threshold
    upper_limit=np.array([100,255,255])            #threshold
    mask = cv2.inRange(hsv,lower_limit,upper_limit)#masking
    res=cv2.bitwise_and(image,image,mask=mask)     #result after masking
    #cv2.imwrite('maskedCorners.png',res)           #saving the picture
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
    #print "hy = ", hy
    #print "xlist", xlist
    #print "lx %i , hx %i     ly %i , hy %i" %(lx,hx,ly,hy)
    crop_img = image[ly:hy,lx:hx]
    #cv2.imshow('cropped image',crop_img)
    return crop_img



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


def makeMatrix(image):                            #Makes a .txt file acordingly to the threshold values
    tmp = image
    if tmp.any() >60:
        print "im in"
        image[tmp]=255
    elif tmp.any() <=60:
        image[tmp]=0
        #print "im in elif"
    #cv2.imshow('masking',image)
    np.savetxt('matrix.txt',image,fmt='%1d',header='%i\n%i\n%i\n%i' %(row(image),coloum(image),50,50),comments='')##missing robot pos 50 ,50
    #np.savetxt('colorScale.txt',image,fmt='%1d',header='%i\n%i\n%i\n%i' %(row(image),coloum(image),50,50),comments='')


def findRed(image):                               #Finds Red in image
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_limit=np.array([0,100,140])             #threshold
    upper_limit=np.array([20,255,255])            #threshold
    mask = cv2.inRange(hsv,lower_limit,upper_limit)#masking
    #res=cv2.bitwise_and(image,image,mask=mask)     #result after masking
    #outI(res)
    #outI(mask)
    return mask

def colorScale(image):
    image[image == 255] = 7


def save(image):
    cv2.imwrite('featureDetectionV1_2.png',image)


class image_feature:

    def __init__(self):

        '''Initialize ros publisher, ros subscriber'''
        # topic where we publish
        self.image_pub = rospy.Publisher("/output/image_treated",
            Image,queue_size = 1)

        self.image_pub_display = rospy.Publisher("/display_image",Image,queue_size =1)

        self.coord_pub = rospy.Publisher("/output/target_frobit",coord,queue_size = 1)

        # subscribed Topic
        self.raw_sub = rospy.Subscriber("/markercapture/raw",Image, self.callbackMaster,queue_size = 1)

        self.subMark4 = rospy.Subscriber("/markerlocator/markerpose_4",
            markerpose, self.callback4,  queue_size = 1) # UpperLeft Corner
        self.subMark5 = rospy.Subscriber("/markerlocator/markerpose_5",
            markerpose, self.callback5,  queue_size = 1) # LowerRight Corner

        self.subMark6 = rospy.Subscriber("/markerlocator/markerpose_6",
            markerpose, self.callback6,  queue_size = 1) # UpperRight Corner

        self.subMark7 = rospy.Subscriber("/markerlocator/markerpose_7",
            markerpose, self.frobit,  queue_size = 1) # The Frobit

        self.subMark8 = rospy.Subscriber("/markerlocator/markerpose_8",
            markerpose, self.callback8,  queue_size = 1) # LowerLeft Corner

        self.subMark9 = rospy.Subscriber("/markerlocator/markerpose_9",
            markerpose, self.target,  queue_size = 1) # Target

        self.subscriber = rospy.Subscriber("/image_cropped",
            Image, self.callback,  queue_size = 1)
        if VERBOSE :
            print "subscribed to /camera/image/compressed"

    def callback4(self,ros_data):
        global mark4Flag
        mark4Flag = True
        x.append(ros_data.x)
        y.append(ros_data.y)

    def callback5(self,ros_data):
        global mark5Flag
        mark5Flag = True
        x.append(ros_data.x)
        y.append(ros_data.y)


    def callback6(self,ros_data):
        global mark6Flag
        mark6Flag = True
        x.append(ros_data.x)
        y.append(ros_data.y)


    def callback8(self,ros_data):
        global mark8Flag
        mark8Flag = True
        #print mark8Flag
        x.append(ros_data.x)
        y.append(ros_data.y)

    def target(self,ros_data):
        global targetFlag
        targetFlag = True
        global tx
        tx = int(ros_data.x)
        global ty
        ty = int(ros_data.y)

    def frobit(self,ros_data):
        global frobitFlag
        frobitFlag = True
        global fx
        fx= int(ros_data.x)
        global fy
        fy= int(ros_data.y)

    def callbackMaster(self,ros_data):
        img=bridge.imgmsg_to_cv2(ros_data,"bgr8")
        print "entered master"
        #print mark4Flag, mark8Flag
        if mark4Flag and mark5Flag and mark6Flag and mark8Flag:
            #print "if state"
            hx = int(max(x))
            lx = int(min(x))
            hy = int(max(y))
            ly = int(min(y))
            new_img = img[ly:hy, lx:hx]
            cv2.imshow("cropped",img) # change to new_img for crop
            cv2.waitKey(3)
            obj = findRed(img)
            colorScale(obj)
            if VERBOSE:
                cv2.imshow('the raw image',img)
                cv2.imshow('consist only of 0 and 7',obj)
                cv2.waitKey(2)
            msg=bridge.cv2_to_imgmsg(obj, encoding="8UC1")
            self.image_pub.publish(msg)
            cmsg = coord()
            cmsg.fx = fx
            cmsg.fy = fy
            cmsg.tx = tx
            cmsg.ty = ty
            self.coord_pub.publish(cmsg)
            global mark4Flag
            mark4Flag = False
            global mark8Flag
            mark8Flag = False





    def callback3(self,ros_data):
        img=bridge.imgmsg_to_cv2(ros_data,"bgr8")
        #color_img = img
        print "started callback 3"
       #print type(img)
        #hx = int(max(x))
        #lx = int(min(x))
        #hy = int(max(y))
        #ly = int(min(y))
        #new_img = img[ly:hy, lx:hx]
        #checker = False
        #print mark_data
        #cv2.imshow("recieved raw image",img)
        #cv2.waitKey(5)



    def callback2(self,ros_data):
        timestamp.append(ros_data.timestamp) #putting the timestamps into list
        tmp1=int(round(ros_data.x))
        tmp2=int(round(ros_data.y))
        x.append(tmp1) # appending x coord in list
        y.append(tmp2) # appendign y coord in list
        if len(timestamp) == 2:
            #print len(timestamp)
            if timestamp[0] == timestamp[1]: # check for sync
                #checker = True
                #print timestamp , x , y
                del timestamp[:] , x[:],y[:]
            else:
                print "msg not in sync"

#      if ros_data.quality > 0.7:
   #         print ros_data.timestamp
    #    else:
     #       print ros_data
            #print "Thor is shinning golden GOD amongst sheeps"

    def callback(self,ros_data):
        img = bridge.imgmsg_to_cv2(ros_data,"bgr8")
        obj=findRed(img)
        colorScale(obj)
        #makeMatrix(obj)
        #save(obj)
        if VERBOSE:
            cv2.imshow('the raw image',img)
            cv2.imshow('consist only of 0 and 7',obj)
            cv2.waitKey(2)
        msg=bridge.cv2_to_imgmsg(obj, encoding="8UC1")
        msg2=bridge.cv2_to_imgmsg(img,encoding="bgr8")

        self.image_pub.publish(msg)
        self.image_pub_display.publish(msg2)
        #self.subscriber.unregister()



def main(args):
    '''Initializes and cleanup ros node'''
    image_feature()
    rospy.init_node('feature_detect', anonymous=False)
    try:
        #raw_sub = message_filters.Subscriber('/markercapture/raw',Image)
        #test = message_filters.Subscriber('/markerlocater/markerpose_7',markerpose)
        #tss = message_filters.TimeSynchronizer([raw_sub,test],0)
        #tss.registerCallback(image_feature.gotimage)
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

