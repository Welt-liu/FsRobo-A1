#   !/bin/sh 
cd /home/ny/FsRobo-A1 
colcon build 
source ./install/setup.sh 
ls /dev/ttyUSB*