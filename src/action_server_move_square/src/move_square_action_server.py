#! /usr/bin/env python

import rospy
import actionlib
import time
from actionlib.msg import TestAction, TestResult, TestFeedback
from geometry_msgs.msg import Twist 
from std_msgs.msg import Empty

class MoveSquareClass(object):
    
    _feedback = TestFeedback()
    _result = TestResult()
    take_off_cmd = Empty()
    land_cmd = Empty()
    
    def __init__(self):
        self._as = actionlib.SimpleActionServer("move_sqare_as", TestAction, self.goal_callback, False)
        self._as.start()
        self.ctrl_c = False
        self.rate = rospy.Rate(10)
        self.take_off_pub = rospy.Publisher('/drone/takeoff', Empty)
        self.land_pub = rospy.Publisher('/drone/land', Empty)
        self.move_pub = rospy.Publisher('/cmd_vel', Twist)
    
    def publish_cmd_once(self, cmd):
        while not self.ctrl_c:
            num_connections = self.move_pub.get_num_connections()
            if (num_connections > 0):
                self.move_pub.publish(cmd)
                break
            else:
                self.rate.sleep()
        
    def takeoff(self):
        i = 0
        while not i == 3:
            self.take_off_pub.publish(self.take_off_cmd)
            time.sleep(1)
            i += 1
            
    def land(self):
        i = 0
        while not i == 3:
            self.land_pub.publish(self.land_cmd)
            time.sleep(1)
            i += 1
    
    def stop(self):
        stop_cmd = Twist()
        stop_cmd.linear.x = 0.0
        stop_cmd.angular.z = 0.0
        self.publish_cmd_once(stop_cmd)
        
    def move(self, move_time, linear_vel, angular_vel):
        move_cmd = Twist()
        move_cmd.linear.x = linear_vel
        move_cmd.angular.z = angular_vel
        self.publish_cmd_once(move_cmd)
        time.sleep(move_time)
        self.stop()
        
        
    def goal_callback(self, goal):
        
        success = True
        side_length = goal.goal
        t = time.time()
        
        self.takeoff()
        for i in range(4):
            
            rospy.loginfo("Moving")
            if self._as.is_preempt_requested():
                self._as.set_preempted()
                success = False
                break
            
            self.move(side_length, 0.2, 0.0)
            self.move(1, 0.0, 1)
            
            self._feedback.feedback = i
            self._as.publish_feedback(self._feedback)
            
            self.rate.sleep()
        
        self.land()
            
        if success:
            self._result.result = time.time() - t
            self._as.set_succeeded(self._result)


if __name__ == "__main__":
    rospy.init_node('move_square_action_server')
    MoveSquareClass()
    rospy.spin()