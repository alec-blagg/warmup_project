#!/usr/bin/env python3
""" This script has the robot follow a person"""
import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class PersonFollower(object):
    def __init__(self):
        # Initialize node and set up subscriber and publisher
        rospy.init_node('person_follower')
        rospy.Subscriber("/scan", LaserScan, self.follow)
        self.control = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    def follow(self, data):
        # initialize range to the 0 value
        cur_range = data.ranges[0]
        cur_index = 0

        vel_msg = Twist()

        # iterate over list of range data to find the angle nearest object
        for i in range(len(data.ranges)):
            if data.ranges[i] < cur_range:
                cur_index = i
                cur_range = data.ranges[i]

        # identify what rotation needs to occur
        if (cur_index < 180):
            # rotate and set linear velocity
            vel_msg.angular.z = 0.01 * cur_index
            vel_msg.linear.x = (1/((cur_index + 1)/10)) * (cur_range - 0.5)
        else:
            vel_msg.angular.z = -0.01 * (360 - cur_index)
            vel_msg.linear.x = (1/((360 - cur_index)/10)) * (cur_range - 0.5)

        # if we can't find object stop
        if (cur_range == math.inf):
            vel_msg.angular.z = 0
            vel_msg.linear.x = 0

        self.control.publish(vel_msg)
    
    def run(self):
        rospy.spin()

if __name__ == '__main__':
    node = PersonFollower()
    node.run()