#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


def callback(msg):
    print msg.ranges[360]
    
    if (msg.ranges[360] > 1):
        print 'Moving Forward'
        move.linear.x = 0.1
        move.angular.z = 0.0
        
    if(msg.ranges[360] < 1):
        print 'Wall Detected, turning'
        move.linear.x = 0.0
        move.angular.z = 0.2
        
    if (msg.ranges[719] < 0.3):
        move.linear.x = 0.0
        move.angular.z = -0.2
        
    if (msg.ranges[0] < 0.3):
        move.linear.x = 0.0
        move.angular.z = 0.2
      
    pub.publish(move)
   
rospy.init_node('mini_project_node')     
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, callback)
move = Twist()

rospy.spin()


    
