#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Point, Twist

robot_pos = Point()
robot_vel = Twist()
robot_pos.x = 1
robot_pos.y = 1


def callback(control_):

    robot_pos.x += control_.linear.x
    robot_pos.y += control_.linear.y

    robot_vel.linear.x = control_.linear.x
    robot_vel.linear.y = control_.linear.y


def robot():
    pos_pub = rospy.Publisher('/robot_pos_', Point, queue_size=10)
    vel_pub = rospy.Publisher('/robot_vel', Twist, queue_size=10)
    # Init robot_node
    rospy.init_node('robot_node', anonymous=True)
    # Subscribe to the Controller --> get the desired velocity (Twist)
    rate = rospy.Rate(10)  # 10hz

    while not rospy.is_shutdown():
        rospy.Subscriber("/control_cmd", Twist, callback)
        print(robot_pos.x, robot_pos.y)
        pos_pub.publish(robot_pos)
        vel_pub.publish(robot_vel)
        rate.sleep()


if __name__ == '__main__':
    try:
        robot()
    except rospy.ROSInterruptException:
        pass
