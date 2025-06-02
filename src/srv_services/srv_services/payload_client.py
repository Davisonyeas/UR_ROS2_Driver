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


class payload_client_async(Node):
    def __init__(self):
        super().__init__("payload_client_async")

        self.declare_parameters(namespace="",
                                parameters=[("robot_ip", "129.101.98.211", ParameterDescriptor(description="IP of the Robot")),
                                            ("robot_name", "name_of_robot", ParameterDescriptor(description="Name of the Robot"))])


        self.bot = urx.Robot(self.get_parameter("robot_ip").value)

        self.client = self.create_client(SetPayload, f"{self.get_parameter('robot_ip').value}/set_payload")

        # Active service 
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available, waiting again...")
  
    def send_request(self):
        request = SetPayload.Request()
        request.payload = float(sys.argv[1])
        self.future = self.client.call_async(request)

def main(args=None):
    rclpy.init(args=args)

    payload_client = payload_client_async()

    payload_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(payload_client)
        if payload_client.future.done():
            try:
                response = payload_client.future.result()
                print(f"Payload set to: {response.success}")
            except Exception as e:
                payload_client.get_logger().error(f"Service call failed: {e}")

            else:
                f"Payload is {response.success}"

            break

    payload_client.destroy_node()

    rclpy.shutdown()

if __name__ == "__main__":
    main()