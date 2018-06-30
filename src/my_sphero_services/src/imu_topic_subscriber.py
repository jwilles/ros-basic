#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Imu

class ImuTopicReader(object):
    
    def __init__(self):
        self.imu_data = Imu()
        self.threshold = 7.00
        self.sub = rospy.Subscriber('/sphero/imu/data3', Imu, self.callback)
        
    def callback(self, msg):
        self.imu_data = msg
        
    def get_imu_data(self):
        return self.imu_data
        
    def four_sector_detection(self):
    
        x_accel = self.imu_data.linear_acceleration.x
        y_accel = self.imu_data.linear_acceleration.y
        z_accel = self.imu_data.linear_acceleration.z
        
        axes_list = [x_accel, y_accel, z_accel]
        
        max_axis_index = axes_list.index(max(axes_list))
        positive = axes_list[max_axis_index] >= 0
        
        significant_value = axes_list[max_axis_index] >= self.threshold
        
        if significant_value:
            
            if max_axis_index == 0:
                if postive:
                    message = 'right'
                else:
                    message = 'left'
            elif max_axis_index == 1:
                if positive:
                    message = 'front'
                else:
                    message = 'back'
            elif max_axis_index == 2:
                if positive:
                    message = 'up'
                else:
                    message = 'down'
        else:
            message = 'none'
                
        return self.convert_to_dict(message)
        
    def convert_to_dict(self, message):
        
        detection_dict = {}
        
        detection_dict = {
            'front': (message=='front' or message=='up' or message == 'down'),
            'left': message=='left',
            'right': message=='right',
            'back': message=='back'
        }
        
        return detection_dict
        
        
        
if __name__ == '__main__':
    
    rospy.init_node('imu_topic_subscriber_node')
    imu_topic_obj = ImuTopicReader()
    
    rate = rospy.Rate(0.5)
    
    ctrl_c = False
    def shutdownhook():
        global ctrl_c
        ctrl_c = True
        
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        data = imu_topic_obj.get_imu_data()
        rospy.loginfo(data)
        rate.sleep()
    