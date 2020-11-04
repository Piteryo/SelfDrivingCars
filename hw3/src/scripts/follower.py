#! /usr/bin/python

import rospy
from geometry_msgs.msg import Twist
from rospy import Publisher, Subscriber
from turtlesim.msg import Pose
import math
import numpy as np


class Follower:
    def __init__(self):
        self.sub_1 = Subscriber('/turtle1/pose', Pose, self.follow)
        self.sub_2 = Subscriber('/leo/pose', Pose, self.update)
        self.pub_2 = Publisher('/leo/cmd_vel', Twist, queue_size=10)
        self.pose = Pose()
        self.eps = 1e-2

    def update(self, cur_pose):
        self.pose = cur_pose

    def follow(self, pose):
        msg = Twist()
        distance = np.sqrt((pose.x - self.pose.x)**2 + (pose.y - self.pose.y)**2)
        if distance <= self.eps:
            return
        angle = math.atan2(pose.y - self.pose.y, pose.x - self.pose.x) - self.pose.theta

        if angle > math.pi:
            angle -= 2 * math.pi
        elif angle < -math.pi:
            angle += 2 * math.pi

        msg.linear.x = min(distance, 2.0)
        msg.angular.z = angle
        self.pub_2.publish(msg)


rospy.init_node('main')
Follower()
rospy.spin()
