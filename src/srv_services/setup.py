import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'srv_services'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.[pxy][yma]*')),
        # (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
        # (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
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
            "set_payload = srv_services.set_payload:main",
            "payload_client = srv_services.payload_client:main"
        ],
    },
)
