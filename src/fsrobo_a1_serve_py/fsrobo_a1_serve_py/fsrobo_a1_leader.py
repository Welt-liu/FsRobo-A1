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

class LeaderArm(Node):

    SERVO_PORT_NAME =  u'/dev/ttyUSB2'      # 舵机串口号 <<< 修改为实际串口号
    SERVO_BAUDRATE = 115200                 # 舵机的波特率

    def __init__(self):
        super().__init__('leader_arm_node')
        # 创建主臂角度发布者
        self.angle_publishers = self.create_publisher(
            Float32MultiArray,                                               
            'leader_arm_angle_topic',
            10)
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
        #打印初始化信息
        print("舵机串口初始化成功")
        servo_ids = list(self.uservo.servos.keys())
        self.get_logger().info("主臂在线舵机ID: {}".format(servo_ids))

        # 初始化舵机管理器
    def fsrobo_a1_leader_read_angle(self,msg):
        for i in range(5):
            angle = Float32MultiArray
            self.uservo.query_servo_angle(i,angle[i].data)
        self.angle_publishers.publish(angle)
        # self.get_logger().info("set servo %d angle %f" % (0, msg.data[1]))



def main(args=None):
        rclpy.init(args=args)

        followerarm_leader = LeaderArm()


        # rclpy.spin(followerarm_leader)

        followerarm_leader.destroy_node()

        rclpy.shutdown()



if __name__ == '__main__':
    # follower_arm_init()
    main()
