#!/usr/bin/env python
#coding:utf-8
'''
从臂舵机控制节点(Demo)
'''
import rclpy                           
from rclpy.action import ActionServer   
from rclpy.node import Node              
import numpy as np
import serial                          
from .uservo import UartServoManager
from .uservo import robo_Arm_Info
from sensor_msgs.msg import JointState 
import math
import time
import struct
from std_msgs.msg import Float32MultiArray
from robo_interfaces.srv import RoboStates
from robo_interfaces.action import MoveArm
# from rclpy.action import ActionServer, CancelResponse, GoalResponse
# from rclpy.callback_groups import ReentrantCallbackGroup
from robo_interfaces.msg import SetAngle


START_ANGLE = [0.0,0.0,90.0,0.0,0.0,0.0]

ROBO_DRIVER_NODE = 'robo_driver_node'+str(robo_Arm_Info.ID)
ROBO_CURRENT_ANGLE_PUBLISHER = 'current_angle_topic'+str(robo_Arm_Info.ID)
ROBO_SET_ANGLE_SUBSCRIBER ='set_angle_topic'+str(robo_Arm_Info.ID)
SERVO_PORT_NAME =  u'/dev/ttyUSB0'      # 舵机串口号 <<< 修改为实际串口号
SERVO_BAUDRATE = 115200                 # 舵机的波特率

class UartServo:
    servo_ids = list()
    def __init__(self):
        print("UartServo init")
         # 初始化串口
        success = False
        while not success:
            try:
                self.uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,
                                            parity=serial.PARITY_NONE, stopbits=1,
                                            bytesize=8, timeout=0)
                success = True  # 如果成功初始化，则设置成功标志
            except serial.SerialException as e:
                print(f"串口初始化失败: {e}")
                time.sleep(0.1)  # 暂停 1 秒后重试
        try:
            self.uservo = UartServoManager(self.uart,srv_num=6)
        except Exception as e:
            print(f"UartServoManager初始化失败: {e}")
        self.servo_ids = list(self.uservo.servos.keys())
        # self.get_logger().info("手臂在线舵机ID: {}".format(servo_ids))
    #归零 
    def  move_to_zero(self):
        #归零
        command_data_list = [
            struct.pack('<BhHH',i,int(START_ANGLE[i]*10), 6000, 0)for i in range(6)
        ]
        command_data_list += [struct.pack('<BhHH', 9, 0, 6000, 0)]
        self.uservo.send_sync_angle(8, 7, command_data_list)

    def set_angle(self,msg):
        command_data_list = [struct.pack('<BhHH', msg.servo_id[i], int(msg.target_angle[i]*10), int(msg.time[i]), 0)for i in range(len(msg.target_angle))]
        self.uservo.send_sync_angle(8, len(msg.target_angle), command_data_list)

    def current_angle_msg_generator(self):
        angle_msg = Float32MultiArray()
        angle_msg.data = [999.0, 999.0, 999.0, 999.0, 999.0, 999.0]
        for i in range(6):
            angle = self.uservo.query_servo_angle(i)
            angle_msg.data[i] = angle
        return angle_msg
    
    def disable_all_torque(self):
        for i in self.uservo.servos:
            self.disable_torque(i)

    
    def disable_torque(self,servo_id):
        self.uservo.disable_torque(servo_id)


class Arm_contorl(Node):
    target_angle = [0.0,0.0,0.0,0.0,0.0,0.0]

    def __init__(self):
        super().__init__(ROBO_DRIVER_NODE)
        self.Servo = UartServo()
        # 初始化串口
        self.get_logger().info("手臂在线舵机ID: {}".format(self.Servo.servo_ids))

        #回馈实时角度，设置定时器，每0.1秒调用一次  
        self.angle_publishers = self.create_publisher(Float32MultiArray,ROBO_CURRENT_ANGLE_PUBLISHER,1)
        self.timer2 = self.create_timer(0.1,self.query_servo_angle_callback) 
     
        #处理设置角度   
        self.angle_subscribers =  self.create_subscription( SetAngle,ROBO_SET_ANGLE_SUBSCRIBER,self.set_angle_callback,1)
        # 创建服务 :反馈舵机状态消息
        self.service = self.srv = self.create_service(RoboStates, 'robo_states', self.query_data_callback)
        #初始化步骤 归零
        self.Servo.move_to_zero()
    
    #设置舵机角度
    def set_angle_callback(self,msg):
        self.Servo.set_angle(msg)

        
    # 定时查询舵机角度
    def query_servo_angle_callback(self):
        angle_msg = self.Servo.current_angle_msg_generator()
        self.angle_publishers.publish(angle_msg)

    #舵机状态反馈服务
    def query_data_callback(self, request, response):
        command = request.command
        match command:
            case 'disable':
                    self.Servo.disable_all_torque()
                    for i in self.Servo.uservo.servos:
                        response.servo_id.append(i)
                        response.servo_data.append(0)
                    print("disable all torque")
                    return response
            case 'zero':
                    self.Servo.move_to_zero()
                    for i in self.Servo.uservo.servos:
                        response.servo_id.append(i)
                        response.servo_data.append(0)
                    print("move to zero")
                    return response
    
        
def main(args=None):
    rclpy.init(args=args)
    followerarm_subscriber = Arm_contorl()
    rclpy.spin(followerarm_subscriber)
    followerarm_subscriber.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
