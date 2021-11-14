#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Point, Twist
from math import sqrt

# initialize position and direction (what happens values not overwritten?)
dir = Point()
dir.x = 0
dir.y = 1
norm_dir = 1

# define the position of the goal as a Point (2D with x- and y-coordinate)
goal = Point()
goal.x = 5
goal.y = 5

# define the control-output control_ (velocity)
speed = 0.3  # speed (magnitude of the velocity)
control_ = Twist()


def calc_vel(robot_pos):

    global norm_dir

    dir.x = goal.x - robot_pos.x
    dir.y = goal.y - robot_pos.y
    norm_dir = sqrt(dir.x ** 2 + dir.y ** 2)

    if norm_dir > 0.5:
        control_.linear.x = speed * (dir.x / norm_dir) * 0.05
        control_.linear.y = speed * (dir.y / norm_dir) * 0.05
        rospy.loginfo(robot_pos)
    else:
        control_.linear.x = 0
        control_.linear.y = 0
        print('robot reached the destination')
        print(robot_pos.x, robot_pos.y)


def controller():
    control_pub = rospy.Publisher('/control_cmd', Twist, queue_size=10)
    # Init controller_node
    rospy.init_node('controller_node', anonymous=True)
    # subscribe the position from the robot
    rate = rospy.Rate(10)  # 10hz

    while not rospy.is_shutdown():
        if norm_dir < 0.5:
            break
        rospy.Subscriber("/robot_pos_", Point, calc_vel)
        control_pub.publish(control_)
        rate.sleep()


if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass
