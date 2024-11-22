#!/usr/bin/env python
#coding:utf-8
'''
从臂舵机控制节点(Demo)
'''
import rclpy
from rclpy.node import Node
import serial
from .uservo import UartServoManager,robo_Arm_Info
import time
from std_msgs.msg import Float32MultiArray


ROBO_ACTION_NODE = 'robo_action_client_node'+str(robo_Arm_Info.ID)
FOLLOWER_ARM_ANGLE_TOPIC = 'leader_arm_angle_topic' + str(robo_Arm_Info.ID)

class FollowerArm(Node):

    SERVO_PORT_NAME =  u'/dev/ttyUSB0'      # 舵机串口号 <<< 修改为实际串口号
    SERVO_BAUDRATE = 115200                 # 舵机的波特率

    def __init__(self):
        super().__init__('robo_follower_node')
        self.subscription = self.create_subscription(
            Float32MultiArray,
            FOLLOWER_ARM_ANGLE_TOPIC,
            self.set_servo_angle_callback,
            1)
        self.subscription

        # 初始化串口
        try:
            self.uart = serial.Serial(port=self.SERVO_PORT_NAME, baudrate=self.SERVO_BAUDRATE,\
                                parity=serial.PARITY_NONE, stopbits=1,\
                                bytesize=8,timeout=0)
        except serial.SerialException as e:
            print(f"串口初始化失败: {e}")
        try:
            self.uservo = UartServoManager(self.uart,srv_num=6)
        except Exception as e:
            print(f"UartServoManager初始化失败: {e}")
        print("舵机串口初始化成功")
        servo_ids = list(self.uservo.servos.keys())
        self.get_logger().info("手臂在线舵机ID: {}".format(servo_ids))

        # 初始化舵机管理器
    def set_servo_angle_callback(self,msg):
        for i in range(6):
            self.uservo.set_servo_angle(i,msg.data[i],velocity = 60)
        # time.sleep(0.05)

def main(args=None):
        rclpy.init(args=args)

        followerarm_subscriber = FollowerArm()
        
        rclpy.spin(followerarm_subscriber)

        followerarm_subscriber.destroy_node()

        rclpy.shutdown()



if __name__ == '__main__':
    main()
