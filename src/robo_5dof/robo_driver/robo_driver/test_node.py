#!/usr/bin/env python
#coding:utf-8
'''
打印调试曲线用节点
'''
import rclpy
from rclpy.node import Node
import serial
from .uservo import UartServoManager
import time
from std_msgs.msg import Float32MultiArray
from robo_interfaces.srv import RoboStates

class test_node_(Node):

    def __init__(self):
        super().__init__('robo_leader_node')

        self.cli = self.create_client(RoboStates, 'robo_states')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

        self.req = RoboStates.Request()

        timer_period = 0.10  # seconds
        self.timer = self.create_timer(timer_period, self.test_publish)
        self.i = 0

    def test_publish(self):
        print("test_publish")
        self.req.command = 'angle'
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()




def main(args=None):
        rclpy.init(args=args)

        test_node = test_node_()

        rclpy.spin(test_node)

        test_node.destroy_node()

        rclpy.shutdown()



if __name__ == '__main__':
    # follower_arm_init()
    main()
