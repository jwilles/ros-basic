#! /usr/bin/env python

import rospy                                          
from exercise22.msg import Age 

rospy.init_node('age_publisher')                   # Initiate a Node called 'topic_subscriber'

pub = rospy.Publisher('/age_info', Age, queue_size=1)
rate= rospy.Rate(2)
age = Age()
age.years = 1
age.months = 2
age.days = 3

while not rospy.is_shutdown():
    pub.publish(age)
    rate.sleep()