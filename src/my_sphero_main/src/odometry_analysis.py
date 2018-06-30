#! /usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Vector3
from nav_msgs.msg import Odometry

class OdometryAnalysis(object):
    
    def __init__(self):
        pass
        
    def get_distance_moved(self, odom_result_array):
        
        distance = None
        
        if len(odom_result_array) >= 2:
            start_odom = odom_result_array[0]
            end_odom = odom_result_array[-1]
            
            start_position = start_odom.pose.pose.position
            end_position = end_odom.pose.pose.position
            
            distance_vector = self.get_distance_vector(start_position, end_position)
            distance = self.calc_vect_length(distance_vector)
            
        return distance
        
    def get_distance_vector(self, start_position, end_position):
        distance_vector = Vector3()
        distance_vector.x = end_position.x - start_position.x
        distance_vector.y = end_position.y - start_position.y
        distance_vector.z = end_position.z - start_position.z
        return distance_vector
        
    def calc_vect_length(self, distance_vector):
        return math.sqrt((distance_vector.x)**2 + (distance_vector.y)**2 + (distance_vector.z)**2)

def check_out_of_maze(goal_distance, odom_result_array):
    odom_analysis = OdometryAnalysis()
    distance = odom_analysis.get_distance_moved(odom_result_array)
    rospy.loginfo("Distance Moved="+str(distance))
    if distance > goal_distance:
        return True
        
    return False