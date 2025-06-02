#!usr/bin/env python3
#~/Documents/PhD_CS_Davis_UI/Optimize/ROS2/ur_ros2_driver_d/venv python3

import sys
import os
import rclpy
from rclpy.node import Node
import rcl_interfaces
from rcl_interfaces.msg import ParameterDescriptor
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'urx'))
# import urx_d
# from urx_d import Robot
# from urx_d import R

# sys.path.insert(1, "ur_ros2_driver_d/urx_d")
# # import urx_d
# from urx_d import Robot

# from os.path import dirname, join, abspath
# sys.path.insert(0, abspath(join(dirname(__file__), '..')))
# import urx_d
# from urx_d import Robot

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ur_ros2_driver_d')))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../urx')))

venv_site_packages = "/home/davis/Documents/PhD_CS_Davis_UI/Optimize/ROS2/ur_ros2_driver_d/venv/lib/python3.10/site-packages"
sys.path.insert(0, venv_site_packages)
import urx
from urx import Robot


import time

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ur_interfaces'))
import ur_interfaces
from ur_interfaces.msg import CurJoints


class current_cartesian(Node):
    def __init__(self):
        super().__init__("current_joint")
        param_descriptor = ParameterDescriptor(description="Returns the current joint position of the Robot")

        self.declare_parameters(namespace="",
                                parameters=[("robot_ip", "129.101.98.211", param_descriptor),
                                            ("robot_name", "name_of_robot", param_descriptor)])
        
        self.bot = urx.Robot(self.get_parameter("robot_ip").value)

        self.publisher_ = self.create_publisher(CurJoints,  f"{self.get_parameter('robot_name').value}/cur_joint", 10)

        timer_period = 0.5

        self.timer = self.create_timer(timer_period, self.timer_callback_cart)

        self.get_logger().info("Current Cartesian Position Node is ready to start.")
        
    
    def timer_callback_cart(self):
        msg = CurJoints()
        msg.joints = self.bot.getj()
        msg.debug_message = "Joints successfully published"
        self.publisher_.publish(msg)
        # Convert the pose array to a string before logging
        self.get_logger().info(f"Joints: {str(msg.joints)}")

    ## def timer_callback_cart(self):
    #     msg = CurCartesian()
    #     msg.pose = self.bot.getl()
    #     msg.debug_message = "Pose successfully updated"
    #     self.publisher_.publish(msg)
    #     self.get_logger().info(msg.pose)
        # self.get_logger().info("Publishing ", msg.pose)
        # self.get_logger().info("Done successfully updating ", msg.debug_message)


def main(args=None):
    rclpy.init(args=args)

    node = current_cartesian()

    rclpy.spin(node)

    rclpy.shutdown(node)


if __name__ == "__main__":
    main()
