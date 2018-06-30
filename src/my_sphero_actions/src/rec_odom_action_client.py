#! /usr/bin/env python

import rospy
import actionlib
from my_sphero_actions.msg import RecordOdomAction, RecordOdomGoal, RecordOdomResult
from nav_msgs.msg import Odometry

def feedback_callback(feedback):
    print feedback
    
rospy.init_node('rec_odom_action_client')
client = actionlib.SimpleActionClient('/record_odom_as', RecordOdomAction)
client.wait_for_server()

goal = RecordOdomGoal()

client.send_goal(goal, feedback_cb=feedback_callback)

rate = rospy.Rate(1)

state = client.get_state()

while state < 2:
    rospy.loginfo('Waiting')
    rate.sleep()
    state = client.get_state()
    rospy.loginfo("state_result: "+str(state))
    
state = client.get_state()
rospy.loginfo('Final State: '+str(state))
rospy.loginfo('Final Result: '+str(client.get_result()))