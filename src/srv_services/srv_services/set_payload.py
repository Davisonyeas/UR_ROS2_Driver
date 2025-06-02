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
from ur_interfaces.srv import SetPayload


class set_payload(Node):
    def __init__(self):
        super().__init__("payload_srv")

        self.declare_parameters(namespace="",
                                parameters=[("robot_ip", "129.101.98.211", ParameterDescriptor(description="IP of the Robot")),
                                            ("robot_name", "name_of_robot", ParameterDescriptor(description="Name of the Robot"))])


        self.bot = urx.Robot(self.get_parameter("robot_ip").value)

        self.srv = self.create_service(SetPayload, f"{self.get_parameter('robot_name').value}/set_payload", self.service_callback)

        self.get_logger().info("Payload Service has started...")

    def service_callback(self, request, response):
        self.get_logger().info("Incoming Payload Request...")
        if request.payload >= 0 and request.payload <= 5:
            self.bot.set_payload(request.payload)
            self.get_logger().info("Changing payload to : " + str(request.payload) + "kg")
            response.success = True
        
        else:
            self.get_logger().warn("Invalid payload. Payload should be in the range of 0 to 5kg")
            response.success = False

        return response


def main(args=None):
    rclpy.init(args=args)

    payload_service = set_payload()

    rclpy.spin(payload_service)

    payload_service.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()