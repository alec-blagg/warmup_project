#!/usr/bin/env python3
""" This script has the robot find and then follow a wall """
import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class WallFollower(object):
    def __init__(self):
        rospy.init_node('wall_follower')
        rospy.Subscriber("/scan", LaserScan, self.follow)
        self.control = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    def follow(self, data):
        cur_range = data.ranges[0]
        cur_index = 0

        vel_msg = Twist()

        for i in range(len(data.ranges)):
            if (data.ranges[i] < cur_range):
                cur_index = i
                cur_range = data.ranges[i]

        f = open("output.txt", 'a')
        f.write("\ncur_index: " + str(cur_index) + " cur_range: " + str(cur_range))
        f.close()

        if (cur_range == math.inf):
            vel_msg.angular.z = 0
            vel_msg.linear.x = 0.5

        if (cur_range > 0.6):
            if (cur_index > 355 or cur_index < 5):
                vel_msg.angular.z = -0.05 * math.copysign(1, 180 - cur_index)
                vel_msg.linear.x = cur_range - 0.5
            elif (cur_index >= 0 and cur_index <= 180):
                vel_msg.angular.z = 0.01 * cur_index
                vel_msg.linear.x = 0
            else:
                vel_msg.angular.z = -0.01 * (360 - cur_index)
                vel_msg.linear.x = 0
        elif(cur_range < 0.4):
            if (cur_index > 175 and cur_index < 185):
                vel_msg.angular.z = -0.05 * math.copysign(1, 180 - cur_index)
                vel_msg.linear.x = 0.5 - cur_range
            elif (cur_index > 0 and cur_index <= 180):
                vel_msg.angular.z = 0.01 * cur_index
                vel_msg.linear.x = 0
            else:
                vel_msg.angular.z = -0.01 * (360 - cur_index)
                vel_msg.linear.x = 0
        else:
            if (cur_index > 85 and cur_index < 95):
                vel_msg.angular.z = 0
                vel_msg.linear.x = (1 - (0.1 * abs(90 - cur_index)))
            else:
                if (cur_index >= 270):
                    vel_msg.angular.z = -0.1
                    vel_msg.linear.x = 0
                elif (cur_index <= 90):
                    vel_msg.angular.z = 0.1
                    vel_msg.linear.x = 0
                elif (cur_index >= 90):
                    vel_msg.angular.z = 0.1
                    vel_msg.linear.x = 0

        self.control.publish(vel_msg)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    node = WallFollower()
    node.run()