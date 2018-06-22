#! /usr/bin/env python

import rospy
import rospkg
from iri_wam_reproduce_trajectory.srv import ExecTraj, ExecTrajRequest # Import the service message used by the service
import sys 

rospack = rospkg.RosPack()
# This rospack.get_path() works in the same way as $(find name_of_package) in the launch files.
traj = rospack.get_path('iri_wam_reproduce_trajectory') + "/config/get_food.txt"

rospy.init_node('service_execute_trajectory_client') # Initialise a ROS node with the name service_client
rospy.wait_for_service('/execute_trajectory') # Wait for the service client /gazebo/delete_model to be running
execute_trajectory_service_client = rospy.ServiceProxy('/execute_trajectory', ExecTraj)
traj_req = ExecTrajRequest()
traj_req.file = traj
result = execute_trajectory_service_client(traj_req) # Send through the connection the name of the object to be deleted by the service
print result # Print the result given by the service called