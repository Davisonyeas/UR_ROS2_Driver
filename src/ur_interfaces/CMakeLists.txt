cmake_minimum_required(VERSION 3.8)
project(ur_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# if(BUILD_TESTING)
#   find_package(ament_lint_auto REQUIRED)
#   # the following line skips the linter which checks for copyrights
#   # comment the line when a copyright and license is added to all source files
#   set(ament_cmake_copyright_FOUND TRUE)
#   # the following line skips cpplint (only works in a git repo)
#   # comment the line when this package is in a git repo and when
#   # a copyright and license is added to all source files
#   set(ament_cmake_cpplint_FOUND TRUE)
#   ament_lint_auto_find_test_dependencies()
# endif()

find_package(rosidl_default_generators REQUIRED)

#add
find_package(action_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)

set(action_files
    "action/CartPose.action"  
    "action/JointPose.action"
)


set(msg_files
   "msg/CurCartesian.msg"
   "msg/CurJoints.msg"
   "msg/IsMoving.msg"
  #  "msg/CurGripper.msg"
  #  "msg/IsMoving.msg"
  #  "msg/CurSpeed.msg"
  #  "msg/ProxReadings.msg"
)

set(srv_files
  "srv/SetPayload.srv"

)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${action_files}
  ${msg_files}
  ${srv_files}


)

# ament_export_dependencies(rosidl_default_runtime)
# ament_python_install_package(urx)


ament_package()
