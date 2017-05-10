# -*- coding: utf-8 -*-
#!/usr/bin/env python


# Python libs
import sys,time
#Ros libraries
import rospy
#Open CV2
import cv2
#Numpy arrays for python
import numpy as np
#ROS messaging libraries
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

VERBOSE=True

class display_image:

    def __init__(self):
        """initialize ROS subscriber"""
    #topic we subscribe on
        self.subscriber = rospy.Subscriber("/display_image",
            Image, self.callback,  queue_size = 1)
        if VERBOSE:
            print "subscribed to /display_image"


    def callback(self,ros_data):
        #print "im in"
        bridge=CvBridge()
        img = bridge.imgmsg_to_cv2(ros_data,"bgr8")
        cv2.imshow('recieved image',img)
        cv2.waitKey(2)
        #print "entered callback"



def main(args):
    display_image()
    rospy.init_node('display_image',anonymous=False)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS image display module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)