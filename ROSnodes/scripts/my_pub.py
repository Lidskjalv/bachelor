#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter',String, queue_size = 10) #topic=chatter
    rospy.init_node('talker',anonymous=False)
    rate = rospy.Rate(1) # 1 hz
    while not rospy.is_shutdown():
        msg_string = "This a test string sendt at = %s" %(rospy.get_time())
        file_obj= open("colorScale.txt","r")
        r = file_obj.read()
        rospy.loginfo(msg_string)
        rospy.loginfo(r)
        pub.publish(msg_string)
        pub.publish(r)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

