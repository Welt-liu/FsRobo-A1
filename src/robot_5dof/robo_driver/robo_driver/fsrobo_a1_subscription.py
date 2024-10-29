#!/usr/bin/env python
#coding:utf-8
'''
从臂舵机控制节点(Demo)
'''
import rclpy
import numpy as np
# from scipy.interpolate import CubicSpline
from rclpy.node import Node
import serial # type: ignore
from .uservo import UartServoManager
# import time
# from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import JointState
# from std_msgs.msg import Header
import math
import time

def radians_to_degrees(radians):
    degrees = radians * (180 / math.pi)
    return degrees


class Arm_contorl(Node):

    SERVO_PORT_NAME =  u'/dev/ttyUSB0'      # 舵机串口号 <<< 修改为实际串口号
    SERVO_BAUDRATE = 115200                 # 舵机的波特率
    joint_ = {'robot_joint1':0,'robot_joint2':1,'robot_joint3':2,'robot_joint4':3,'hand_joint':4,'left_joint':5,'right_joint':99}

    def __init__(self):
        super().__init__('fsrobo_a1_driver_node')
        self.subscription = self.create_subscription(
            JointState,                                               
            'joint_states',
            self.set_servo_angle_callback,1)
        self.subscription

        # 初始化串口
        try:
            self.uart = serial.Serial(port=self.SERVO_PORT_NAME, baudrate=self.SERVO_BAUDRATE,\
                                parity=serial.PARITY_NONE, stopbits=1,\
                                bytesize=8,timeout=1)
        except serial.SerialException as e:
            print(f"串口初始化失败: {e}")
        try:
            self.uservo = UartServoManager(self.uart)
        except Exception as e:
            print(f"UartServoManager初始化失败: {e}")
        servo_ids = list(self.uservo.servos.keys())
        self.get_logger().info("手臂在线舵机ID: {}".format(servo_ids))

    def convert_to_servo_angle(self,joint_name,joint_postion):
        if self.joint_[joint_name] == 0:
            self.uservo.set_servo_angle(0,-radians_to_degrees(joint_postion),velocity = 50)
        elif self.joint_[joint_name] == 1:
            self.uservo.set_servo_angle(1,radians_to_degrees(joint_postion),velocity = 50)
        elif self.joint_[joint_name] == 2:
            self.uservo.set_servo_angle(2,-radians_to_degrees(joint_postion),velocity=50)
        elif self.joint_[joint_name] == 3:
            self.uservo.set_servo_angle(3,radians_to_degrees(joint_postion),velocity=50)
        elif self.joint_[joint_name] == 4:
            self.uservo.set_servo_angle(4,-90+radians_to_degrees(joint_postion),velocity=50)
        elif self.joint_[joint_name] == 5:
            self.uservo.set_servo_angle(5,-radians_to_degrees(joint_postion),velocity=50)

    # 话题接收消息处理
    def set_servo_angle_callback(self,msg):
        for i in range(len(msg.name)):
            self.convert_to_servo_angle(joint_postion = msg.position[i],joint_name = msg.name[i])        
        time.sleep(0.05)



def main(args=None):
        rclpy.init(args=args)

        followerarm_subscriber = Arm_contorl()
        
        rclpy.spin(followerarm_subscriber)

        followerarm_subscriber.destroy_node()

        rclpy.shutdown()



if __name__ == '__main__':
    main()
