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

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

# OpenCV
import cv2
# Ros libraries
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

VERBOSE=True
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

class image_feature:

    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        # topic where we publish
        self.image_pub = rospy.Publisher("/output/image_treated",
            Image,queue_size = 1)
        # self.bridge = CvBridge()

        # subscribed Topic
        self.subscriber = rospy.Subscriber("/image_cropped",
            Image, self.callback,  queue_size = 1)
        if VERBOSE :
            print "subscribed to /camera/image/compressed"






    def callback(self, ros_data):
        bridge=CvBridge()
        img = bridge.imgmsg_to_cv2(ros_data,"bgr8")

        obj=findRed(img)
        colorScale(obj)
        makeMatrix(obj)

        msg=bridge.cv2_to_imgmsg(img, encoding="bgr8")


        self.image_pub.publish(msg)

        #self.subscriber.unregister()

def main(args):
    '''Initializes and cleanup ros node'''
    ic = image_feature()
    rospy.init_node('feature_detect', anonymous=False)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)