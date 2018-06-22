#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist 
import time

class MoveBB8:
    def __init__(self):
        self.bb8_vel_publisher = rospy.Publisher('/cmd_vel', Twist)
        self.rate = rospy.Rate(10)
        rospy.on_shutdown(self.shutdown)
        self.ctrl_c = False
        
    def publish_cmd_once(self, cmd):
        while not self.ctrl_c:
            num_connections = self.bb8_vel_publisher.get_num_connections()
            if (num_connections > 0):
                self.bb8_vel_publisher.publish(cmd)
                break
            else:
                self.rate.sleep()
                
    def stop(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.publish_cmd_once(cmd)
        
        
    def shutdown(self):
        self.stop()
        self.ctrl_c = True
        
    def move(self, move_time, linear_speed, angular_speed):
        cmd = Twist()
        cmd.linear.x = linear_speed
        cmd.angular.z = angular_speed
        self.publish_cmd_once(cmd)
        time.sleep(move_time)
        self.stop()
    
    def move_square(self):
        for i in range(4):
            self.move(4.0, 2.0, 0.0)
            self.move(2.0, 0.0, 0.0)
            self.move(2.0, 0.0, 1.0)
        
        
if __name__ == '__main__':
    rospy.init_node('move_bb8_square')
    move_bb8_object = MoveBB8()
    try:
        move_bb8_object.move_square()
    except rospy.ROSInterruptException:
        pass
        
    