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

### Usage

#### Launching the Driver

To launch the driver
