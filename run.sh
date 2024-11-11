#   !/bin/sh 
cd /root/robo/FsRobo-A1
colcon build 
source ./install/setup.sh 
ls /dev/ttyUSB*
#ros2 launch are1018_urdf arm1018urdftest