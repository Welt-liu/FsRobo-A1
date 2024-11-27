#!/usr/bin/env python
#coding:utf-8
'''
从臂舵机控制节点(Demo)
'''
import rclpy                           
# from rclpy.action import ActionServer   
from rclpy.node import Node              
# import numpy as np
                       
# from robo_driver.uservo import UartServoManager
from robo_driver.uservo_ex import uservo_ex

# from sensor_msgs.msg import JointState 
# import math
# import time

from std_msgs.msg import Float32MultiArray
from robo_interfaces.srv import RoboStates
# from robo_interfaces.action import MoveArm
# from rclpy.action import ActionServer, CancelResponse, GoalResponse
# from rclpy.callback_groups import ReentrantCallbackGroup
from robo_interfaces.msg import SetAngle
import struct




ROBO_DRIVER_NODE = 'robo_driver_node'+str(uservo_ex.ID)
ROBO_CURRENT_ANGLE_PUBLISHER = 'current_angle_topic'+str(uservo_ex.ID)
ROBO_SET_ANGLE_SUBSCRIBER ='set_angle_topic'+str(uservo_ex.ID)


class Arm_contorl(Node):
    current_angle = [0.0,0.0,0.0,0.0,0.0,0.0]

    def __init__(self):
        super().__init__(ROBO_DRIVER_NODE)
        self.Servo = uservo_ex()
        # 初始化串口
        self.get_logger().info("手臂在线舵机ID: {}".format(self.Servo.servo_ids))

        #回馈实时角度，设置定时器，每0.1秒调用一次  
        self.angle_publishers = self.create_publisher(Float32MultiArray,ROBO_CURRENT_ANGLE_PUBLISHER,1)
        self.timer2 = self.create_timer(0.05,self.query_servo_angle_callback) 
     
        #处理设置角度   
        self.angle_subscribers =  self.create_subscription( SetAngle,ROBO_SET_ANGLE_SUBSCRIBER,self.set_angle_callback,1)
        # 创建服务 :反馈舵机状态消息
        self.service = self.srv = self.create_service(RoboStates, 'robo_states', self.query_data_callback)
        #初始化步骤 归零
        self.Servo.move_to_zero()
    
    #设置舵机角度
    def set_angle_callback(self,msg):
        for i in range(6):
            if abs(msg.target_angle[i] - self.current_angle[i]>20.0):
                self.get_logger().info("舵机角度设置失败，舵机{}目标角度与当前角度差距过大".format(i))
                return

        command_data_list = [struct.pack('<BhHH', msg.servo_id[i], int(msg.target_angle[i]*10), int(msg.time[i]), 0)for i in range(len(msg.target_angle))]
        self.Servo.set_angle(len(msg.target_angle),command_data_list)

        
    # 定时查询舵机角度
    def query_servo_angle_callback(self):
        angle_msg = Float32MultiArray()
        angle_msg.data = [999.0, 999.0, 999.0, 999.0, 999.0, 999.0]
        for i in range(6):
            self.current_angle[i] = self.Servo.query_servo_current_angle(i)
            angle_msg.data[i] = self.current_angle[i]
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
            case 'zero':
                    self.Servo.move_to_zero()
                    for i in self.Servo.uservo.servos:
                        response.servo_id.append(i)
                        response.servo_data.append(0)
                    print("move to zero")
            case 'error':#TODO test
                    for i in self.Servo.uservo.servos:
                        response.servo_id.append(i)
                        if self.Servo.query_status(i) > 1:
                            response.servo_data.append(255)
                        else:
                            response.servo_data.append(0)
            case 'temperature':
                    for i in self.Servo.uservo.servos:
                        response.servo_id.append(i)
                        response.servo_data.append(self.Servo.query_temperature(i))
            case _:
                    print("invalid command")
        return response

    
        
def main(args=None):
    rclpy.init(args=args)
    followerarm_subscriber = Arm_contorl()
    rclpy.spin(followerarm_subscriber)
    followerarm_subscriber.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
