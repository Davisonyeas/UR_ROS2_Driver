import os 
from glob import glob
from setuptools import find_packages, setup

package_name = 'msg_publishers'

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
    install_requires=['setuptools', 'urx'],
    zip_safe=True,
    maintainer='davis',         
    maintainer_email='davisonyeas1@gmail.com',
    description='ROS2 Driver for Universal Robots (Non official)',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "current_cart = msg_publishers.current_cart:main",
            "current_joint = msg_publishers.current_joint:main",
            "is_moving = msg_publishers.move_check:main"
        ],
    },
)
