#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Imu

class ImuTopicReader(object):
    
    def __init__(self):
        self.imu_data = Imu()
        self.sub = rospy.Subscriber('/sphero/imu/data3', Imu, self.callback)
        
    def callback(self, msg):
        self.imu_data = msg
        
    def get_imu_data(self):
        return self.imu_data
        
if __name__ == '__main__':
    
    rospy.init_node('imu_topic_subscriber_node')
    imu_topic_obj = ImuTopicReader()
    
    rate = rospy.Rate(0.5)
    
    ctrl_c = False
    def shutdownhook():
        global ctrl_c
        ctrl_c = True
        
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        data = imu_topic_obj.get_imu_data()
        rospy.loginfo(data)
        rate.sleep()
    