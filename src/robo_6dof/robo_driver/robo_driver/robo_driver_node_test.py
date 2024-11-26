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




ROBO_DRIVER_NODE = 'robo_driver_node'+str(uservo_ex.ID)
ROBO_CURRENT_ANGLE_PUBLISHER = 'current_angle_topic'+str(uservo_ex.ID)
ROBO_SET_ANGLE_SUBSCRIBER ='set_angle_topic'+str(uservo_ex.ID)


class Arm_contorl(Node):
    target_angle = [0.0,0.0,0.0,0.0,0.0,0.0]

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
        self.Servo.set_angle(msg)

        
    # 定时查询舵机角度
    def query_servo_angle_callback(self):
        # angle_msg = self.Servo.current_angle_msg_generator()
        angle_msg = Float32MultiArray()
        angle_msg.data = [999.0, 999.0, 999.0, 999.0, 999.0, 999.0]
        for i in range(6):
            angle = self.Servo.query_servo_current_angle(i)
            angle_msg.data[i] = angle
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
