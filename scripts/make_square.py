#!/usr/bin/env python3
"""This scripts gets the robot to make a square"""
import rospy
import math
from geometry_msgs.msg import Twist

class SquareRobot(object):
    def __init__(self):
        rospy.init_node('square_robot')
        self.publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    ## function to do the turn action
    def turn(self, vel_msg):
        ## give angular speed, publish, and let go
        ## speed a bit higher than mathematically calculated value
        ## this is to handle noise
        vel_msg.angular.z = 0.56
        self.publisher.publish(vel_msg)
        rospy.sleep(math.pi)

        ## set angular speed to 0 and publish, give time to stop
        vel_msg.angular.z = 0
        self.publisher.publish(vel_msg)
        rospy.sleep(0.1)

    ## function to travel in a straight line
    def straight_line(self, vel_msg):
        ## give linear speed, publish, and let go for 5 seconds
        vel_msg.linear.x = 0.25
        self.publisher.publish(vel_msg)
        rospy.sleep(5)

        ## set linear speed to 0 and publish, give time to stop
        vel_msg.linear.x = 0
        self.publisher.publish(vel_msg)
        rospy.sleep(0.1)

    ## function to make the square
    def makeSquare(self):
        vel_msg = Twist()

        ## line needed to allow connection
        rospy.sleep(1)

        ## make each of the four sides
        for x in range(4):
            self.straight_line(vel_msg)
            self.turn(vel_msg)

if __name__ == '__main__':
    node = SquareRobot()
    node.makeSquare()