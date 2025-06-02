# Universal Robot ROS 2 Driver

A ROS Driver for Universal Robots (not the official driver) for seamless integration and control of the UR robotic arms within ROS 2 applications.

### Features

* Real-time control of the UR robots via ROS2 (joint trajectories, I/O control).
* Support for all UR models (UR3, UR5, UR5e, UR10, UR16).
* Simulation-ready (Gazebo & Ignition) - In Progress (ETA: Q4 2025)
* URCap integration for deployment on robot controllers.

### Installation

#### Prerequisites

* ROS 2 (Humble, Foxy, Galactic)
* Universal Robot (e-series or CB3, with Polyscope >= 5.0)
* Colcon build system

#### Build 

```
mkdir -p ~/ur_ros2_ws/src
cd ~/ur_ros2_ws/src
git clone https://github.com/Davisonyeas/UR_ROS2_Driver.git
cd ..
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```

### Configure the Robot

* Enable external control on the UR teach pendant
* Set the robot's IP
* NOTE: Robot should be on External Control mode to use this ROS2 Driver.

### Usage

#### Launching the Driver

To launch the driver with a specific UR robot model:

```
source ~/ur_ros2_ws/install/setup.bash
ros2 launch ur_ros2_driver ur_driver.launch.py robot_ip:=<robot-ip> robot_model:=<robot_model>
```

#### Controlling the Robot

Send trajectory commands using ROS 2 action interfaces. You can also integrate with MoveIt 2 for motion planning.
