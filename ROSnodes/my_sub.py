# -*- coding: utf-8 -*-
#!/usr/bin/env python

import rospy
import subprocess
from std_msgs.msg import String


def callback(data):
    rospy.loginfo(rospy.get_caller_id()  + ' I recieved %s' , data.data)
    fh=open("r.txt","w")
    fh.write(data.data)
    fh.close
    program ='./demo.exe'
    arg = 'r.txt'
    subprocess.call([program, arg])

def listener():
    rospy.init_node('listener',anonymous=False)
    rospy.Subscriber('chatter', String, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
