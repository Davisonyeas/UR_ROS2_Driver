import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'action_servers'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.[pxy][yma]*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='davis',
    maintainer_email='davisonyeas1@gmail.com',
    description='ROS2 Driver for Universal Robots (Non official)',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "cart_pose_server = action_servers.cart_pose_server:main",
            "joint_pose_server = action_servers.joint_pose_server:main",
            "cart_pose_client = action_servers.cart_pose_client:main"
        ],
    },
)
