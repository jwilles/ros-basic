#! /usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyRequest


rospy.init_node('bb8_move_in_square_service_client')
rospy.wait_for_service('/move_bb8_in_square')
move_bb8_in_square_client = rospy.ServiceProxy('/move_bb8_in_square', Empty)
move_bb8_req = EmptyRequest()
result = move_bb8_in_square_client(move_bb8_req)
print result