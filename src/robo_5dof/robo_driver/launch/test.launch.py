from launch import LaunchDescription
# from launch_ros.actions import PushRosNamespace, Node
from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import FrontendLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    

    robo_state_publisher_launch = os.path.join(get_package_share_directory('robo_description'),'launch')
    robo_state_publisher_node = IncludeLaunchDescription(PythonLaunchDescriptionSource([robo_state_publisher_launch,'/robo_state_publisher.launch.py']))


    robo_moveit_launch = os.path.join(get_package_share_directory('robo_moveit'),'launch')
    robo_moveit_node = IncludeLaunchDescription(PythonLaunchDescriptionSource([robo_moveit_launch,'/test.launch.py']))


    return LaunchDescription([
        robo_state_publisher_node,
        robo_moveit_node
    ])

