#! /usr/bin/env python

import rospy
from imu_topic_subscriber import ImuTopicReader
from std_srvs.srv import Trigger, TriggerResponse


class CrashDetectionService(object):
    
    def __init__(self):
        self.service = rospy.Service('/crash_detection', Trigger, self.callback)
        self.imu_reader = ImuTopicReader()
        self.response = TriggerResponse()
        
    def callback(self, request):
        direction_dict = self.imu_reader.four_sector_detection()
        self.response.success = self.has_crashed(direction_dict)
        self.response.message = self.direction_to_move(direction_dict)
        return self.response
        
    def has_crashed(self, direction_dict):
        for key in direction_dict:
            if direction_dict[key] == True:
                return True
        return False 
        
    def direction_to_move(self, direction_dict):
        if not direction_dict['front']:
            return 'forwards'
        else:
            if not direction_dict['left']:
                return 'left'
            else:
                if not direction_dict['right']:
                    return 'right'
                else:
                    if not direction_dict['back']:
                        return 'backwards'
                    else:
                        return 'un_stuck'
                    

        
if __name__ == '__main__':
    rospy.init_node('crash_detection_service')
    CrashDetector = CrashDetectionService()
    rospy.spin()
    
        
        