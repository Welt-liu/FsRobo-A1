echo 1234 | sudo -S chmod 777 /dev/ttyUSB0
while true;do ros2 run robo_driver driver;done;