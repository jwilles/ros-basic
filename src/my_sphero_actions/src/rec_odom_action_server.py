#! /usr/bin/env python

import rospy
import actionlib
from odom_topic_subscriber import OdomTopicReader
from odometry_analysis import check_out_of_maze
from my_sphero_actions.msg import RecordOdomAction, RecordOdomResult, RecordOdomFeedback
from nav_msgs.msg import Odometry


class RecordOdom(object):
    
    def __init__(self, goal_distance):
        self.result = RecordOdomResult()
        self.odom_reader = OdomTopicReader()
        self.seconds_recording = 120
        self.goal_distance = goal_distance
        
        self._as = actionlib.SimpleActionServer('/record_odom_as', RecordOdomAction, self.goal_callback)
        self._as.start()
        
    def goal_callback(self, goal):
        success = True
        
        rate = rospy.Rate(1)
        
        for i in range(self.seconds_recording):
            rospy.loginfo("Recording Odom index="+str(i))
            
            if self._as.is_preempt_requested():
                rospy.logdebug('The goal has been cancelled/preempted')
                self._as.set_preempted()
                success = False
                break
            
            if self.reached_goal_distance():
                rospy.logwarn('Reached distance Goal')
                break;
            else:
                rospy.logdebug('Reading Odometry...')
                current_odom = self.odom_reader.get_odomdata()
                self.result.result_odom_array.append(current_odom)
            
            rate.sleep()
            
        if success:
            self._as.set_succeeded(self.result)
            
        self.clean_variables()
            
    def reached_goal_distance(self):
        return check_out_of_maze(self.goal_distance, self.result.result_odom_array)
        
    def clean_variables(self):
        self.result = RecordOdomResult()
        
if __name__ == '__main__':
    rospy.init_node('record_odom_action_server')
    RecordOdom(goal_distance=2.0)
    rospy.spin()