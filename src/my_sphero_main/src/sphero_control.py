#! /usr/bin/env python

import rospy
import actionlib
from my_sphero_actions.msg import RecordOdomAction, RecordOdomGoal
from std_srvs.srv import Trigger, TriggerRequest
from cmd_vel_publisher import CmdVelPub
from odometry_analysis import check_out_of_maze


class SpheroControl(object):
    
    def __init__(self, goal_distance):
        self.goal_distance = goal_distance
        self.init_direction_service_client()
        self.init_record_odom_action_client()
        self.cmd_vel_pub = CmdVelPub()
        
    def init_direction_service_client(self):
        rospy.loginfo('Initializing Direction Service Client')
        rospy.wait_for_service('/crash_detection')
        self.direction_service_client = rospy.ServiceProxy('/crash_detection', Trigger)
        self.direction_service_request = TriggerRequest()
        
    def init_record_odom_action_client(self):
        self.rec_odom_client = actionlib.SimpleActionClient('/record_odom_as', RecordOdomAction)
        self.rec_odom_goal = RecordOdomGoal()
        
    def init_cmd_vel_publisher(self):
        self.cmd_vel_pub = CmdVelPub()
        
    def send_goal_to_odom_action_server(self):
        self.rec_odom_client.send_goal(self.rec_odom_goal, feedback_cb=self.odom_feedback_callback)
        
    def odom_feedback_callback(self, feedback):
        rospy.loginfo('Odom Feedback: '+str(feedback))
        
    def has_odom_finished(self):
        return (self.rec_odom_client.get_state() >= 2)
        
    def get_rec_odom_result(self):
        return self.rec_odom_client.get_result()
    
    def get_movement_direction(self):
        result = self.direction_service_client(self.direction_service_request)
        return result.message
        
    def move(self, direction):
        self.cmd_vel_pub.move_robot(direction)
        
    
        
        
        
rospy.init_node('sphero_main_node')
sphero = SpheroControl(goal_distance=2.0)
rate = rospy.Rate(10)

sphero.send_goal_to_odom_action_server()

while not sphero.has_odom_finished():
    movement_direction = sphero.get_movement_direction()
    rospy.loginfo(movement_direction)
    sphero.move(movement_direction)
    rate.sleep()
    
odom_result = sphero.get_rec_odom_result()
odom_result_array = odom_result.result_odom_array

if check_out_of_maze(sphero.goal_distance, odom_result_array):
    rospy.loginfo('Out of Maze!')
else:
    rospy.loginfo('Out of Time!')
    
rospy.loginfo('Finished')