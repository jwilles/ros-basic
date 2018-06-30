#! /usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

class OdomTopicReader(object):
    
    def __init__(self):
        self.sub = rospy.Subscriber('/odom', Odometry, self.callback)
        self.odom_data = Odometry()
        
    def callback(self, msg):
        self.odom_data = msg
        
    def get_odomdata(self):
        return self.odom_data
        
if __name__ == '__main__':
    
    rospy.init_node('odom_topic_subscriber_node')
    odom_reader_obj = OdomTopicReader()
    
    rate = rospy.Rate(0.5)
    
    ctrl_c = False 
    def shutdownhook():
        global ctrl_c
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        data = odom_reader_obj.get_odomdata()
        rospy.loginfo(data)
        rate.sleep()
    
        
        