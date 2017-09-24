# -*- coding: utf-8 -*-
#!/usr/bin/env python


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
VERBOSE = False
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

class path_planner:

    def __init__(self):
        "Initialize ROS publisher /subscriber"
        #PUBLISHER
        self.path_subscriber = rospy.Subscriber("/output/image_treated",Image,self.callback,queue_size =1)
        if VERBOSE:
            print "subscribed to /output/image_treated"


    def callback(self,ros_data):
        bridge=CvBridge()
        img = bridge.imgmsg_to_cv2(ros_data,"8UC1")
        if VERBOSE:
            cv2.imshow("picture",img)
            cv2.waitKey(2)
        printE(img)

def main(args):
    '''Initializes and cleanup ros node'''
    path_planner()
    rospy.init_node('path_planner',anonymous=False)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)