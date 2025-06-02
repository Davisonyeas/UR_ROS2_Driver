import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    package_name = "msg_publishers"

    robot_name_launch_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='name_of_robot',
        description='The name of the Robot'
    )

    robot_ip_launch_arg = DeclareLaunchArgument(
        'robot_ip',
        default_value='129.101.98.211',
        description='The IP of the Robot'
    )

    robot_name = LaunchConfiguration("robot_name")
    robot_ip = LaunchConfiguration("robot_ip")

    cart_node = Node(
        package=package_name,
        executable="current_cart",
        parameters= [{
            "robot_ip": robot_ip,
            "robot_name": robot_name
        }],
        respawn= True,
        respawn_delay=4,
    )


    joint_node = Node(
        package=package_name,
        executable="current_joint",
        parameters= [{
            "robot_ip": robot_ip,
            "robot_name": robot_name
        }],
        respawn= True,
        respawn_delay=4,
    )

    move_node = Node(
        package=package_name,
        executable="is_moving",
        parameters= [{
            "robot_ip": robot_ip,
            "robot_name": robot_name
        }],
        respawn= True,
        respawn_delay=4,
    )


    return LaunchDescription([
        robot_name_launch_arg,
        robot_ip_launch_arg,

        cart_node,
        joint_node,
        move_node,

        # LogInfo(msg=LaunchConfiguration("robot_ip")),
        # LogInfo(msg=LaunchConfiguration("robot_name")),

    ])