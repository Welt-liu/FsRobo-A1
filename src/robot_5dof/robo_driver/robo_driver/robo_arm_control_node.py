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
# from std_msgs.msg import Float32MultiArray

from robo_interfaces.srv import RoboStates
def radians_to_degrees(radians):
    degrees = radians * (180 / math.pi)
    return degrees
def get_keys_by_value(d, target_value):
    return [key for key, value in d.items() if value == target_value]

class Arm_contorl(Node):

    SERVO_PORT_NAME =  u'/dev/ttyUSB4'      # 舵机串口号 <<< 修改为实际串口号
    SERVO_BAUDRATE = 115200                 # 舵机的波特率
    joint_ = {'robot_joint1':0,'robot_joint2':1,'robot_joint3':2,'robot_joint4':3,'hand_joint':4,'left_joint':5,'right_joint':99}
    last_angle = {0,0,0,0,0,0}
    def __init__(self):
        super().__init__('robo_arm_control_node')

        # 创建话题 :接收joint_states消息
        self.subscription = self.create_subscription(
            JointState,                                               
            'joint_states',
            self.set_servo_angle_callback,1)
        # 创建服务 :反馈舵机状态消息
        self.service = self.srv = self.create_service(RoboStates, 'robo_states', self.query_data_callback)


        # 初始化串口
        try:
            self.uart = serial.Serial(port=self.SERVO_PORT_NAME, baudrate=self.SERVO_BAUDRATE,\
                                parity=serial.PARITY_NONE, stopbits=1,\
                                bytesize=8,timeout=0)
        except serial.SerialException as e:
            print(f"串口初始化失败: {e}")
        try:
            self.uservo = UartServoManager(self.uart)
        except Exception as e:
            print(f"UartServoManager初始化失败: {e}")
        servo_ids = list(self.uservo.servos.keys())
        self.get_logger().info("手臂在线舵机ID: {}".format(servo_ids))

    # 判断关节名称和位置，转换为舵机角度
    def convert_to_servo_angle(self,joint_name,joint_postion):
        if self.joint_[joint_name] == 0:
            self.uservo.set_servo_angle(0,-radians_to_degrees(joint_postion),interval=1000)
        elif self.joint_[joint_name] == 1:
            self.uservo.set_servo_angle(1,radians_to_degrees(joint_postion),interval=1000)
        elif self.joint_[joint_name] == 2:
            self.uservo.set_servo_angle(2,-radians_to_degrees(joint_postion),interval=1000)
        elif self.joint_[joint_name] == 3:
            self.uservo.set_servo_angle(3,radians_to_degrees(joint_postion),interval=1000)
        elif self.joint_[joint_name] == 4:
            self.uservo.set_servo_angle(4,-90+radians_to_degrees(joint_postion),interval=1000)
        elif self.joint_[joint_name] == 5:
            self.uservo.set_servo_angle(5,-radians_to_degrees(joint_postion),interval=1000)

    # 话题接收消息处理
    def set_servo_angle_callback(self,msg):
        for i in range(len(msg.name)):  
            self.convert_to_servo_angle(joint_postion = msg.position[i],joint_name = msg.name[i])
        self.uservo.wait( timeout=1.01)
    
    def query_data_callback(self, request, response):
        request_type = request.query_type
        match request_type:
            case 'angle':
                self.uservo.query_all_srv_angle()
                for i in self.uservo.servos:
                    response.servo_names.append( get_keys_by_value(self.joint_,i))
                    response.servo_states.append(self.uservo.servos[i].angle)
                return response

        
        




def main(args=None):
        rclpy.init(args=args)
        followerarm_subscriber = Arm_contorl()
        rclpy.spin(followerarm_subscriber)
        followerarm_subscriber.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()
