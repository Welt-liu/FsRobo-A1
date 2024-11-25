#!/usr/bin/env python
#coding:utf-8

'''
示教模式节点

'''
import rclpy
from rclpy.node import Node
# from std_msgs.msg import String
import threading
import time
from std_msgs.msg import Float32MultiArray
from robo_driver.uservo import robo_Arm_Info
from robo_interfaces.msg import SetAngle
import numpy as np
from robo_interfaces.srv import RoboStates

ROBO_SET_ANGLE_PUBLISHER ='set_angle_topic'+str(robo_Arm_Info.ID)
ROBO_CURRENT_ANGLE_SUBSCRIPTION = 'current_angle_topic'+str(robo_Arm_Info.ID)

# class servo_servicer_(Node):

#     def __init__(self):
#         super().__init__('servo_servicer_node')






class MyNode(Node):
    running = True  # 输入线程运行标志
    GET_ANGLE = False
    current_angle = [0.0, 0.0, 0.0, 0.0, 0.0,0.0]  # 当前关节角度
    #记录角度
    angle_record = []
    tech_enable = False  # 示教模式使能标志
    replay_enable = False  # 示教模式回放标志
    pubulish_delay_ms = 200.0 #ms

    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('初始化中..')


        self.servo_servicer = self.create_client(RoboStates, 'robo_states')
        while not self.servo_servicer.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')


        # 订阅新发布的角度
        self.subscriber = self.create_subscription(
            Float32MultiArray,
            ROBO_CURRENT_ANGLE_SUBSCRIPTION,
            self.current_angle_callback,
            10
        )

        #发布角度控制话题
        self.set_angle_publishers = self.create_publisher(
            SetAngle,ROBO_SET_ANGLE_PUBLISHER,
            1)

         # 启动线程来读取终端输入
        self.input_thread = threading.Thread(target=self.read_input)
        self.input_thread.start()
        self.tech_thread = threading.Thread(target=self.tech_mode_controller)
        self.tech_thread.start()

    def send_servo_request(self, command):
        req = RoboStates.Request()
        req.command = command
        self.get_logger().info('等待..')
        future = self.servo_servicer.call_async(req)
        
        # rclpy.spin_until_future_complete(self, future)
        # return future.result()

    # def send_servo_request(self, command):
    #     self.req.command = command
    #     self.future = self.cli.call_async(self.req)
    #     rclpy.spin_until_future_complete(self, self.future)
    #     return self.future.result()


    def read_input(self):
        while self.running:
            self.get_logger().info('S:开始示教/停止，T：执行示教动作，D：失能手臂，C:清除示教记录,Ctrl+C：退出示教模式')
            input_str = input()
            if input_str == 'S' or input_str == 's':
                if self.tech_enable == False:
                    self.tech_enable = True
                    self.get_logger().info('示教模式开启')
                else:
                    self.tech_enable = False
                    self.get_logger().info('示教模式关闭')
                pass
            elif input_str == 'C' or input_str == 'c':
                self.angle_record = []
                self.get_logger().info('示教记录清除')
            elif input_str == 'T' or input_str == 't':
                if not self.tech_enable:
                    if self.replay_enable == False:
                        self.replay_enable = True
                        self.get_logger().info('示教模式回放开启')

            elif input_str == 'D' or input_str == 'd':
                # threading.Thread(target=self.send_servo_request, args=('disable',)).start()
                self.send_servo_request('disable')
                self.get_logger().info('失能手臂OK')


    def tech_mode_controller(self):
        while not self.GET_ANGLE:
            pass
        delay_time = 6000.0

        while self.running:
            if(self.tech_enable):
                data = tuple(self.current_angle)
                self.angle_record.append(data)
                time.sleep(self.pubulish_delay_ms*0.001)
            if self.replay_enable:
                for i in range(len(self.angle_record)):
                    goal_msg = SetAngle()
                    goal_msg.servo_id = [0,1,2,3,4,5]
                    goal_msg.target_angle = self.angle_record[i]
                    if i == 0:
                        delay_time = 2000.0
                    else:
                        delay_time = self.pubulish_delay_ms
                    goal_msg.time = [delay_time for _ in range(6)]

                    self.set_angle_publishers.publish(goal_msg)
                    time.sleep(delay_time*0.001)

                self.replay_enable = False
                self.get_logger().info('示教模式回放关闭')
                self.replay_enable = False



    def destroy_node(self):
        self.running = False  # 停止输入线程
        self.input_thread.join()  # 等待线程完成
        super().destroy_node()

    # 处理当前角度话题回调
    def current_angle_callback(self, msg):
        self.GET_ANGLE = True
        _data = msg.data
        for i in range(len(_data)):
            self.current_angle[i] = _data[i]






def main(args=None):
    rclpy.init(args=args)
    node = MyNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
