#!usr/bin/env python3
import os
import sys
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, ActionClient, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.action.client import ClientGoalHandle

venv_site_packages = "/venv/lib/python3.10/site-packages"
sys.path.insert(0, venv_site_packages)

import urx
from urx import Robot
import rcl_interfaces
from rcl_interfaces.msg import ParameterDescriptor
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ur_interfaces'))
import ur_interfaces
from ur_interfaces.msg import IsMoving
from ur_interfaces.action import CartPose


class cart_pose_client(Node):
    def __init__(self):
        super().__init__(self, "cart_pose_client")

        self.cart_client_ = ActionClient(self, CartPose, f"/{self.get_parameter('robot_name').value}/cartesian_pose")


    def send_goal(self, x, y, z, w, p, r):
        self.cart_client_.wait_for_server()

        goal = CartPose.Goal()
        goal.x = x
        goal.y = y
        goal.z = z
        goal.w = w
        goal.p = p
        goal.r = r

        self.get_logger().info("Sending Goal...")

        self.cart_client_. \
            send_goal_async(goal). \
                add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        self.goal_handle_: ClientGoalHandle = future.result()

        if self.goal_handle_.accepted:
            self.get_logger().info("Goal Accepted")
            self.goal_handle_.get_result_async().add_done_callback(self.goal_result_callback)

        else:
            self.get_logger().info("SERVER REJECT the Goal")


    def goal_result_callback(self, future):
        result = future.result().result

        self.get_logger().info("Distance Left: " + str(result.distance_left))


def main(args=None):
    rclpy.init(args=args)

    cart_client = cart_pose_client()

    cart_client.send_goal(0.0, 0.4, 0.9, 0.3, 0.8, 1.2)

    rclpy.spin(cart_client)

    rclpy.shutdown()


if __name__ == "__main__":
    main()