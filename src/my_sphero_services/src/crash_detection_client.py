#! /usr/bin/env python

import rospy
from std_srvs.srv import Trigger, TriggerRequest

rospy.init_node('crash_detection_client')
rospy.wait_for_service('/crash_detection')
crash_detection_client = rospy.ServiceProxy('/crash_detection', Trigger)
crash_detection_request = TriggerRequest()

rate = rospy.Rate(5)
ctrl_c = False

def shutdownhook():
    global ctrl_c
    ctrl_c = False
    
rospy.on_shutdown(shutdownhook)

while not ctrl_c:
    result = crash_detection_client(crash_detection_request)
    print result
    rate.sleep()

