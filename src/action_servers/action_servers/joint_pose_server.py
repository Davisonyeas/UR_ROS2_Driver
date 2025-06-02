#!usr/bin/env python3
import os
import sys
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle

venv_site_packages = "/venv/lib/python3.10/site-packages"
sys.path.insert(0, venv_site_packages)

import urx
from urx import Robot
import rcl_interfaces
from rcl_interfaces.msg import ParameterDescriptor
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ur_interfaces'))
import ur_interfaces
from ur_interfaces.msg import IsMoving
from ur_interfaces.action import JointPose

class joint_pose_server(Node):
    def __init__(self):
        super().__init__("joint_pose_server")
        param_descriptor = ParameterDescriptor(description="Receives joint coordinates from Client")

        self.declare_parameters(namespace="",
                                parameters=[("robot_ip", "129.101.98.211", param_descriptor),
                                            ("robot_name", "name_of_robot", param_descriptor)])
        
        self.goal = JointPose.Goal()

        self.bot = urx.Robot(self.get_parameter("robot_ip").value)

        self.joint_action_server_ = ActionServer(self, JointPose, f"/{self.get_parameter('robot_name').value}/joint_pose", 
                                           execute_callback=self.execute_callback, 
                                           goal_callback=self.goal_callback,
                                           cancel_callback=self.cancel_callback)

        self.get_logger().info("Action Server for Joint has started...")

    
    def goal_callback(self, goal_request):
        """ Either Accept or Reject the client request to begin Action """

        self.goal = goal_request

        # Check if goal is valid
        if self.goal.joint1 > 6.28 or self.goal.joint1 < -6.28:
            self.get_logger().error("Invalid Request... Joint out of range")
            return GoalResponse.REJECT
        
        elif self.goal.joint2 > 6.28 or self.goal.joint2 < -6.28:
            self.get_logger().error("Invalid Request... Joint out of range")
            return GoalResponse.REJECT
        
        elif self.goal.joint3 > 6.28 or self.goal.joint3 < -6.28:
            self.get_logger().error("Invalid Request... Joint out of range")
            return GoalResponse.REJECT
        
        elif self.goal.joint4 > 6.28 or self.goal.joint4 < -6.28:
            self.get_logger().error("Invalid Request... Joint out of range")
            return GoalResponse.REJECT
        
        elif self.goal.joint5 > 6.28 or self.goal.joint5 < -6.28:
            self.get_logger().error("Invalid Request... Joint out of range")
            return GoalResponse.REJECT
        
        elif self.goal.joint6 > 6.28 or self.goal.joint6 < -6.28:
            self.get_logger().error("Invalid Request... Joint out of range")
            return GoalResponse.REJECT
        
        else:
            self.get_logger().info("Joint Goal Received: " + str(self.goal))
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
            feedback_msg = JointPose.Feedback()
            feedback_msg.distance_left = self.bot.getj()

            self.get_logger().info(f"""Current Joint 1 - Joint 6  = 
                                   {feedback_msg.distance_left[0], 
                                    feedback_msg.distance_left[1], 
                                    feedback_msg.distance_left[2],
                                    feedback_msg.distance_left[3],
                                    feedback_msg.distance_left[4],
                                    feedback_msg.distance_left[5]}""")
            
            # Moving robot to new position
            self.bot.movel([self.goal.joint1,
                            self.goal.joint2,
                            self.goal.joint3,
                            self.goal.joint4,
                            self.goal.joint5,
                            self.goal.joint6])
            
            while self.bot.is_running():
                # Calculate the distance left
                feedback_msg.distance_left[0] -= self.goal.joint1
                feedback_msg.distance_left[1] -= self.goal.joint2
                feedback_msg.distance_left[2] -= self.goal.joint3
                feedback_msg.distance_left[3] -= self.goal.joint4
                feedback_msg.distance_left[4] -= self.goal.joint5
                feedback_msg.distance_left[5] -= self.goal.joint6

                # send value
                goal_handle.publish_feedback(feedback_msg)

                # Update current Joint position
                feedback_msg.distance_left = self.bot.getj()
        
        except:
            goal_handle.canceled()
            result = JointPose.Result()
            result.success = False
        # Reset
        self.goal = JointPose.Goal()
        return result


def main(args=None):
    print("here.....................................")
    rclpy.init(args=args)

    joint_action_server = joint_pose_server()

    rclpy.spin(joint_action_server)

    joint_action_server.destroy_node()

    rclpy.shutdown()

if __name__ == "__main__":
    main()
