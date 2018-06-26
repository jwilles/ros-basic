#! /usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse
from move_bb8 import MoveBB8

def callback(request):
    BB8 = MoveBB8()
    BB8.move_square()
    return EmptyResponse()
    
rospy.init_node('bb8_move_service_server')
bb8_move_service = rospy.Service('/move_bb8_in_square', Empty, callback)
rospy.spin()