#!/usr/bin/env python3
import os
import sys
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle

venv_site_packages = "/home/davis/Documents/PhD_CS_Davis_UI/Optimize/ROS2/ur_ros2_driver_d/venv/lib/python3.10/site-packages"
sys.path.insert(0, venv_site_packages)

import urx
from urx import Robot
import rcl_interfaces
from rcl_interfaces.msg import ParameterDescriptor
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ur_interfaces'))
import ur_interfaces
from ur_interfaces.msg import IsMoving
from ur_interfaces.action import CartPose

class cart_pose_server(Node):
    def __init__(self):
        super().__init__("cart_pose_server")
        param_descriptor = ParameterDescriptor(description="Receives cartesian coordinates from Client")

        self.declare_parameters(namespace="",
                                parameters=[("robot_ip", "129.101.98.211", param_descriptor),
                                            ("robot_name", "name_of_robot", param_descriptor)])
        
        self.goal = CartPose.Goal()
        
        self.bot = urx.Robot(self.get_parameter("robot_ip").value)

        self.cart_action_server_ = ActionServer(self, CartPose, f"/{self.get_parameter('robot_name').value}/cartesian_pose", 
                                           execute_callback=self.execute_callback, 
                                           goal_callback=self.goal_callback,
                                           cancel_callback=self.cancel_callback)
        
        self.get_logger().info("Action Server for Cart has started...")
    
    def goal_callback(self, goal_request):
        """ Either Accept or Reject the client request to begin Action """

        self.goal = goal_request

        # Check if goal was received
        if self.goal.w > 0 or self.goal.w < 6.0:
            self.goal.w = self.bot.getl()[3]

        else:
            self.get_logger().warn("Invalid Request. W needs to be in the range of 6.0 and -6.0")
            return GoalResponse.REJECT

        if self.goal.p < 6.0 or self.goal.p > -6.0:
            self.goal.p = self.bot.getl()[4]
            
        else:
            self.get_logger().warn("Invalid Request. P needs to be in the range of 6.0 and -6.0")
            return GoalResponse.REJECT
        
        if self.goal.r < 6.0 or self.goal.r > -6.0:
            self.goal.r = self.bot.getl()[5]
            
        else:
            self.get_logger().warn("Invalid Request. R needs to be in the range of 6.0 and -6.0")
            return GoalResponse.REJECT
        
        # Accepted
        self.get_logger().info("Cart Goal Received: " + str(self.goal))
        return GoalResponse.ACCEPT
    

    def cancel_callback(self, goal_handle):
        """ Either Accept ot REject a client request to cancel an action """

        if self.goal == None:
            self.get_logger().info("No Goal to Cancel")
            return CancelResponse.REJECT
        
        else:
            self.get_logger().info("Received Cancel request")
            goal_handle.canceled()
            return CancelResponse.ACCEPT    

    def execute_callback(self, goal_handle):
        try:
            feedback_msg = CartPose.Feedback()
            feedback_msg.distance_left = self.bot.getl()

            self.get_logger().info(f"""Current X, Y, Z coordinates = 
                                   {feedback_msg.distance_left[0], 
                                    feedback_msg.distance_left[1], 
                                    feedback_msg.distance_left[2]}""")
            
            # Moving robot to new position
            self.bot.movel([self.goal.x,
                            self.goal.y,
                            self.goal.z,
                            self.goal.w,
                            self.goal.p,
                            self.goal.r])
            
            while self.bot.is_running():
                # Calculate the distance left
                feedback_msg.distance_left[0] -= self.goal.x
                feedback_msg.distance_left[1] -= self.goal.y
                feedback_msg.distance_left[2] -= self.goal.z
                feedback_msg.distance_left[3] -= self.goal.w
                feedback_msg.distance_left[4] -= self.goal.p
                feedback_msg.distance_left[5] -= self.goal.r

                # send value
                goal_handle.publish_feedback(feedback_msg)

                # Update current cartesan position
                feedback_msg.distance_left = self.bot.getl()
        
        except:
            goal_handle.canceled()
            result = CartPose.Result()
            result.success = False
        # Reset
        self.goal = CartPose.Goal()
        return result


def main(args=None):
    rclpy.init(args=args)

    cart_pose_action_server = cart_pose_server()

    rclpy.spin(cart_pose_action_server)

    cart_pose_action_server.destroy_node()

    rclpy.shutdown()

if __name__ == "__main__":
    main()
