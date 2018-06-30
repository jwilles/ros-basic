#! /usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Vector3
from nav_msgs.msg import Odometry

class OdometryAnalysis(object):
    
    def __init__(self):
        pass
        
    def get_distance_moved(self, odom_result_array):
        print 'hello'
    


def check_out_of_maze(goal_distance, odom_result_array):
    odom_analysis = OdometryAnalysis()
    distance = odom_analysis.get_distance_moved(odom_result_array)
    
    if distance > goal_distance:
        return True
        
    return False