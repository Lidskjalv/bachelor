# -*- coding: utf-8 -*-
#!/usr/bin/env python

import rospy
import subprocess
from std_msgs.msg import String


def callback(data):
    rospy.loginfo(rospy.get_caller_id()  + ' I recieved %s' , data.data)
    fh=open("r_v1.txt","w")
    fh.write(data.data)
    fh.close
    program ='./demo.exe'
    arg = 'r_v1.txt'
    subprocess.call([program, arg])
    #wait(10)


def listener():
    rospy.init_node('pathPlanner',anonymous=False)
    rospy.Subscriber('map', String, callback)
    rospy.spin()


def talker():
    pub = rospy.Publisher('path',String, queue_size = 10) #topic=path
    #rate = rospy.Rate(1) # 1 hz       #rate of publishing
    #if not rospy.is_shutdown():
    file_obj= open("testoutput1.txt","r")                #Read-only matrix.txt
    r = file_obj.read()                                 #reads the whole txt 1 line a time
    #rospy.loginfo(r)                                    #logs info in terminal
    pub.publish(r)                                      #publishes msg
    #rate.sleep()                                        #sleeps to adjust rate()


if __name__ == '__main__':
    listener()
    #talker()
