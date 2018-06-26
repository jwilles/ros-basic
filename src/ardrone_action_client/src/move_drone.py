#! /usr/bin/env python

import rospy
import actionlib
import time
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback
from geometry_msgs.msg import Twist 
from std_msgs.msg import Empty

PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

nImage = 1

def feedback_callback(feedback):
    global nImage
    print ('Feedback: image n.%d received' %nImage)
    nImage += 1
    
rospy.init_node('move_drone')

action_server_name = '/ardrone_action_server'
client = actionlib.SimpleActionClient(action_server_name, ArdroneAction)
client.wait_for_server()

move = rospy.Publisher('/cmd_vel', Twist)
take_off = rospy.Publisher('/drone/takeoff', Empty)
land = rospy.Publisher('/drone/land', Empty)


move_cmd = Twist()
take_off_cmd = Empty()
land_cmd = Empty()


goal = ArdroneGoal()
goal.nseconds = 10
client.send_goal(goal, feedback_cb=feedback_callback)

state = client.get_state()

rate = rospy.Rate(1)

i = 0
while not i == 3:
    take_off.publish(take_off_cmd)
    time.sleep(1)
    i += 1

while state < DONE:
    move_cmd.linear.x = 1.0
    move_cmd.angular.z = 1.0
    move.publish(move_cmd)
    rate.sleep()
    state = client.get_state()
    
i = 0
while not i == 3:
    move_cmd.linear.x = 0.0
    move_cmd.angular.z = 0.0
    move.publish(move_cmd)
    land.publish(land_cmd)
    time.sleep(1)
    i += 1
    
    
    