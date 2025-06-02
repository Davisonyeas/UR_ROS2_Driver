#!usr/bin/env python3
import os
import sys
import time
import rclpy
from rclpy.node import Node

venv_site_packages = "/home/davis/Documents/PhD_CS_Davis_UI/Optimize/ROS2/ur_ros2_driver_d/venv/lib/python3.10/site-packages"
sys.path.insert(0, venv_site_packages)

import urx
from urx import Robot
import rcl_interfaces

from rcl_interfaces.msg import ParameterDescriptor
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ur_interfaces'))
import ur_interfaces
from ur_interfaces.msg import IsMoving

class check_movement(Node):
    def __init__(self):
        super().__init__("check_movement")
        param_descriptor = ParameterDescriptor(description="Returns the current cartesian position of the Robot")

        self.declare_parameters(namespace="",
                                parameters=[("robot_ip", "129.101.98.211", param_descriptor),
                                            ("robot_name", "name_of_robot", param_descriptor)])
        
        self.bot = urx.Robot(self.get_parameter("robot_ip").value)

        self.publisher_ = self.create_publisher(IsMoving,  f"{self.get_parameter('robot_name').value}/is_moving", 10)

        timer_period = 0.5

        self.timer = self.create_timer(timer_period, self.timer_callback_check_move)

        self.get_logger().info("Robot State is ready to start.")
        
        
    def timer_callback_check_move(self):
        msg = IsMoving()
        msg.moving = self.bot.is_running()
        msg.debug_message = "Robot state Received"
        self.publisher_.publish(msg)
        self.get_logger().info(f"Robot State: {str(msg.moving)}")


def main(args=None):
    rclpy.init(args=args)

    node = check_movement()

    rclpy.spin(node)

    # check_movement.destroy_node()

    rclpy.shutdown(node)

if __name__ == "__main__":
    main()
