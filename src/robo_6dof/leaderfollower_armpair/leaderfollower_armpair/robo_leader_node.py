#!/usr/bin/env python
#coding:utf-8
'''
从臂舵机控制节点(Demo)
'''
import rclpy
# import sys
# import os
# current_file_path = os.path.abspath(__file__)
# parent_dir = os.path.dirname(os.path.dirname(current_file_path))
# sys.path.append(parent_dir)

from rclpy.node import Node
import serial
from robo_driver.uservo import UartServoManager
from robo_driver.uservo_ex import uservo_ex

# import time
from std_msgs.msg import Float32MultiArray

LEADER_ARM_ANGLE_TOPIC = 'leader_arm_angle_topic' + str(uservo_ex.ID)
SERVO_PORT_NAME =  u'/dev/ttyUSB0'      # 舵机串口号 <<< 修改为实际串口号
SERVO_BAUDRATE = 115200                 # 舵机的波特率

class LeaderArm(Node):



    def __init__(self):
        super().__init__('robo_leader_node')
        # 创建主臂角度发布者
        self.angle_publishers = self.create_publisher(
            Float32MultiArray,                                               
            LEADER_ARM_ANGLE_TOPIC,
            1)
        # 初始化串口
        try:
            self.uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
                                parity=serial.PARITY_NONE, stopbits=1,\
                                bytesize=8,timeout=0)
        except serial.SerialException as e:
            print(f"串口初始化失败: {e}")
        try:
            self.uservo = UartServoManager(self.uart,srv_num=6)
        except Exception as e:
            print(f"UartServoManager初始化失败: {e}")
        #打印初始化信息
        print("舵机串口初始化成功")
        servo_ids = list(self.uservo.servos.keys())
        self.get_logger().info("主臂在线舵机ID: {}".format(servo_ids))

        for i in range(6):
            self.uservo.set_damping(i,power=400)
        
        # 创建定时器
        timer_period = 0.050  # seconds
        self.timer = self.create_timer(timer_period, self.fsrobo_a1_leader_angle_publish)
        # self.i = 0


        # 初始化舵机管理器
    def fsrobo_a1_leader_angle_publish(self):
        msg = Float32MultiArray()
        msg.data = [999.0, 999.0, 999.0, 999.0, 999.0, 999.0]
        for i in range(6):
            msg.data[i] = self.uservo.query_servo_angle(i)
        self.angle_publishers.publish(msg)


def main(args=None):
        rclpy.init(args=args)

        followerarm_leader = LeaderArm()

        rclpy.spin(followerarm_leader)

        followerarm_leader.destroy_node()

        rclpy.shutdown()



if __name__ == '__main__':
    # follower_arm_init()
    main()
