#!/usr/bin/env python
#coding:utf-8
'''
从臂舵机控制节点(Demo)
'''
import rclpy
import numpy as np
from rclpy.node import Node
import serial # type: ignore
from .uservo import UartServoManager
from sensor_msgs.msg import JointState
# from std_msgs.msg import Header
import math
import time
from robo_interfaces.srv import RoboStates

def radians_to_degrees(radians):
    degrees = radians * (180 / math.pi)
    return degrees

def degrees_to_radians(degrees):
    radians = degrees * (math.pi / 180)
    return radians

class Arm_contorl(Node):

    SERVO_PORT_NAME =  u'/dev/ttyUSB1'      # 舵机串口号 <<< 修改为实际串口号
    SERVO_BAUDRATE = 115200                 # 舵机的波特率
    joint_ = ['robot_joint1','robot_joint2','robot_joint3','robot_joint4','hand_joint','left_joint','right_joint']
    index_joint_ = {value: index for index, value in enumerate(joint_)}

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

    #将关节位置转换为舵机角度
    def jointstate2servoangle(self,joint_name,joint_postion):
        if joint_name == self.joint_[0]:
            self.uservo.set_servo_angle(0,-radians_to_degrees(joint_postion),interval=1000)
        elif joint_name == self.joint_[1]:
            self.uservo.set_servo_angle(1,radians_to_degrees(joint_postion),interval=1000)
        elif joint_name == self.joint_[2]:
            self.uservo.set_servo_angle(2,-radians_to_degrees(joint_postion),interval=1000)
        elif joint_name == self.joint_[3]:
            self.uservo.set_servo_angle(3,radians_to_degrees(joint_postion),interval=1000)
        elif joint_name == self.joint_[4]:
            self.uservo.set_servo_angle(4,-90+radians_to_degrees(joint_postion),interval=1000)
        elif joint_name == self.joint_[5]:
            self.uservo.set_servo_angle(5,-radians_to_degrees(joint_postion),interval=1000)

    #将舵机角度转换为关节位置
    def servoangle2jointstate(self,servo_id,servo_angle):
        if servo_id == 0:
            return -degrees_to_radians(servo_angle)
        elif servo_id == 1:
            return degrees_to_radians(servo_angle)
        elif servo_id == 2:
            return -degrees_to_radians(servo_angle)
        elif servo_id == 3:
            return degrees_to_radians(servo_angle)
        elif servo_id == 4:
            return degrees_to_radians(servo_angle+90)
        elif servo_id == 5:
            return -degrees_to_radians(servo_angle)
        
    # 话题接收消息处理
    def set_servo_angle_callback(self,msg):
        print("joint_states: ",msg.position)
        for i in range(len(msg.name)):  
            if self.index_joint_[msg.name[i]] not in self.uservo.servos:
                continue
            self.jointstate2servoangle(joint_postion = msg.position[i],joint_name = msg.name[i])
        self.uservo.wait( timeout=1.01)

    # 反馈舵机状态消息处理
    def query_data_callback(self, request, response):
        command = request.command
        match command:
            case 'angle':
                self.uservo.query_all_srv_angle()
                for i in self.uservo.servos:
                    response.servo_name.append(self.joint_[i])
                    # response.servo_data.append(self.uservo.servos[i].angle)
                    response.servo_data.append(self.servoangle2jointstate(i,self.uservo.servos[i].angle))
                print("joint_states: ",response.servo_data)
                return response

        
def main(args=None):
        rclpy.init(args=args)
        followerarm_subscriber = Arm_contorl()
        rclpy.spin(followerarm_subscriber)
        followerarm_subscriber.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()
