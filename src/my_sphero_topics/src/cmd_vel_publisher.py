#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

class CmdVelPub(object):
    
    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist)
        self.cmd_msg = Twist()
        
        
    def move_robot(self, direction):
        if direction == 'forwards':
            self.cmd_msg.linear.x = 0.02
            self.cmd_msg.angular.z = 0.0
        elif direction == 'backwards':
            self.cmd_msg.linear.x = -0.2
            self.cmd_msg.angular.z = 0.0
        elif direction  == 'right':
            self.cmd_msg.linear.x = 0.0
            self.cmd_msg.angular.z = 0.2
        elif direction == 'left':
            self.cmd_msg.linear.x = 0.0
            self.cmd_msg.angular.z = -0.2
        elif direction == 'stop':
            self.cmd_msg.linear.x = 0.0
            self.cmd_msg.angular.z = -0.2
            
        self.pub.publish(self.cmd_msg)
            
if __name__ == '__main__':
    
    rospy.init_node('cmd_vel_publisher_node')
    cmd_vel_pub_object = CmdVelPub()
    
    rate = rospy.Rate(1)
    ctrl_c = False
    
    def shutdownhook():
        
        global ctrl_c
        global cmd_msg
        global pub
        
        ctrl_c = True
        cmd_vel_pub_object.move_robot('stop')
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        cmd_vel_pub_object.move_robot('forwards')
        rate.sleep()
            
    