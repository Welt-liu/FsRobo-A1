#!/usr/bin/env python
#coding:utf-8
'''
从臂舵机控制节点(Demo)
'''
import rclpy
from rclpy.node import Node
import serial
from .uservo import UartServoManager
import time
from std_msgs.msg import Float32MultiArray

class FollowerArm(Node):

    SERVO_PORT_NAME =  u'/dev/ttyUSB2'      # 舵机串口号 <<< 修改为实际串口号
    SERVO_BAUDRATE = 115200                 # 舵机的波特率

    def __init__(self):
        super().__init__('follower_arm_node')
        # self.publisher_ = self.create_publisher(Float32MultiArray, 'topic', 10)  # CHANGE
        self.subscription = self.create_subscription(
            Float32MultiArray,                                               # CHANGE
            'follower_arm_control_topic',
            self.set_servo_angle_callback,
            10)
        self.publishers = self.create_publisher(Float32MultiArray, 'follower_arm_publisher_topic', 10)
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
        print("舵机串口初始化成功")
        # self.uservo = UartServoManager(self.uart)
        servo_ids = list(self.uservo.servos.keys())
        # print(self.uservo.ping(0))
        self.get_logger().info("有效的舵机ID列表: {}".format(servo_ids))

        # 初始化舵机管理器
    def set_servo_angle_callback(self,msg):
        # for i in range(5):
        #     self.uservo.set_servo_angle(i, msg.data[i], interval=0)
        self.get_logger().info("set servo %d angle %f" % (0, msg.data[1]))
    def close(self):
         self.uart.close()

def main(args=None):
        rclpy.init(args=args)
        followerarm_subscriber = FollowerArm()
        rclpy.spin(followerarm_subscriber)
        followerarm_subscriber.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    # follower_arm_init()
    main()
