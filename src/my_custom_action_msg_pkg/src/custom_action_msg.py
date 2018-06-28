#! /usr/bin/env python

import rospy
import actionlib
from std_msgs.msg import String
from std_msgs.msg import Empty
from my_custom_action_msg_pkg.msg import CustomActionMsgAction, CustomActionMsgFeedback, CustomActionMsgResult

class MoveVerticalClass(object):
    _feedback = CustomActionMsgFeedback()
    _result = CustomActionMsgResult()
    take_off_cmd = Empty()
    land_cmd = Empty()
    
    def __init__(self):
        self._as = actionlib.SimpleActionServer('move_vertical_as', CustomActionMsgAction, self.goal_callback, False)
        self._as.start()
        self.take_off_pub = rospy.Publisher('/drone/takeoff', Empty)
        self.land_pub = rospy.Publisher('/drone/land', Empty)
    
    def goal_callback(self, goal):
        
        direction = goal.goal
        rate = rospy.Rate(1)
        success = True
        
        for i in range(4):
            
            rospy.loginfo("Moving")
            
            if self._as.is_preempt_requested():
                self._as.set_preempted()
                success = False
                break
            
            if direction == 'UP':
                self.take_off_pub.publish(self.take_off_cmd)
            
            if direction == 'DOWN':
                self.land_pub.publish(self.land_cmd)
            
            rate.sleep()
        
        if success:
            self._as.set_succeeded(self._result)

if __name__ == "__main__":
    rospy.init_node('custom_action_msg')
    MoveVerticalClass()
    rospy.spin()
    