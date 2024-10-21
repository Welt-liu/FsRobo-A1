#!/usr/bin/env python
#coding:utf-8
'''
从臂舵机控制节点(Demo)
'''
import rclpy
from rclpy.node import Node
import serial # type: ignore
from .uservo import UartServoManager
# import time
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math
import time
def radians_to_degrees(radians):
    degrees = radians * (180 / math.pi)
    return degrees


class FollowerArm(Node):

    SERVO_PORT_NAME =  u'/dev/ttyUSB0'      # 舵机串口号 <<< 修改为实际串口号
    SERVO_BAUDRATE = 115200                 # 舵机的波特率

    def __init__(self):
        super().__init__('fsrobo_a1_driver_node')
        self.subscription = self.create_subscription(
            JointState,                                               
            'joint_states',
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
            self.uservo = UartServoManager(self.uart)
        except Exception as e:
            print(f"UartServoManager初始化失败: {e}")
        print("舵机串口初始化成功")
        servo_ids = list(self.uservo.servos.keys())
        self.get_logger().info("手臂在线舵机ID: {}".format(servo_ids))

        # 初始化舵机管理器
    def set_servo_angle_callback(self,msg):
        # time.sleep(0.1)
        self.uservo.set_servo_angle(0,radians_to_degrees(msg.position[0]),interval=100,t_acc=50,t_dec=50)
        self.uservo.set_servo_angle(1,radians_to_degrees(msg.position[1]),interval=100,t_acc=50,t_dec=50)
        self.uservo.set_servo_angle(2,-45-radians_to_degrees(msg.position[2]),interval=100,t_acc=50,t_dec=50)
        self.uservo.set_servo_angle(3,-radians_to_degrees(msg.position[3]),interval=100,t_acc=50,t_dec=50)
        self.uservo.set_servo_angle(4,radians_to_degrees(msg.position[4]),interval=100,t_acc=50,t_dec=50)
        time.sleep(0.1)
        print("主臂舵机角度: {}".format(msg.position[4]))
        # self.get_logger().info("主臂舵机角度: {}".format(msg.data))



def main(args=None):
        rclpy.init(args=args)

        followerarm_subscriber = FollowerArm()
        
        rclpy.spin(followerarm_subscriber)

        followerarm_subscriber.destroy_node()

        rclpy.shutdown()



if __name__ == '__main__':
    main()
