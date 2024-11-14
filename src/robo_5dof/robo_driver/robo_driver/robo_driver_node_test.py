#!/usr/bin/env python
#coding:utf-8
'''
从臂舵机控制节点(Demo)
'''
import rclpy                            # type: ignore
from rclpy.action import ActionServer   # type: ignore
from rclpy.node import Node              # type: ignore
import numpy as np
import serial                           # type: ignore
from .uservo import UartServoManager
from sensor_msgs.msg import JointState  # type: ignore
import math
import time

from std_msgs.msg import Float32MultiArray
from robo_interfaces.srv import RoboStates
from robo_interfaces.action import MoveArm
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup

# def radians_to_degrees(radians):
#     degrees = radians * (180 / math.pi)
#     return degrees

def degrees_to_radians(degrees):
    radians = degrees * (math.pi / 180)
    return radians

# #将米转为角度
# def meters_to_degrees(meters):
    
#     degrees = (meters/0.027) * 50
#     return degrees


class Arm_contorl(Node):
    DEAD_ZONE = 0.4
    SERVO_PORT_NAME =  u'/dev/ttyUSB0'      # 舵机串口号 <<< 修改为实际串口号
    SERVO_BAUDRATE = 115200                 # 舵机的波特率
    # joint_ = ['robot_joint1','robot_joint2','robot_joint3','robot_joint4','hand_joint','grippers_joint','right_joint']
    # index_joint_ = {value: index for index, value in enumerate(joint_)}

    target_angle = [0.0,0.0,0.0,0.0,0.0,0.0]
    current_angle = [0.0,0.0,0.0,0.0,0.0,0.0]

    def __init__(self):
        super().__init__('robo_driver_node')


        self._action_server = ActionServer(
            self,
            MoveArm,
            'move',
            execute_callback=self.set_servo_angle_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
            )#TODO
        self.timer = self.create_timer(0.005,self.timer_callback)  # 设置定时器，每0.005秒调用一次
        self.timer2 = self.create_timer(0.5,self.timer_callback2)  # 设置定时器，每0.005秒调用一次
        # 创建服务 :反馈舵机状态消息
        self.service = self.srv = self.create_service(RoboStates, 'robo_states', self.query_data_callback)
        # test
        self.angle_publishers = self.create_publisher(
            Float32MultiArray,
            'leader_arm_angle_topic',
            1)

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
        servo_ids = list(self.uservo.servos.keys())
        self.get_logger().info("手臂在线舵机ID: {}".format(servo_ids))
        for i in self.uservo.servos:
            self.target_angle[i] = self.uservo.query_servo_angle(i)
            self.current_angle[i] =  self.target_angle[i]

    #取消
    def cancel_callback(self, goal_handle):
        
        print('enter cancel_callback')
        return CancelResponse.ACCEPT
        

    #将舵机角度转换为关节位置
    def servoangle2jointstate(self,servo_id,servo_angle):
        if servo_id == 0:
            return degrees_to_radians(servo_angle)
        elif servo_id == 1:
            return degrees_to_radians(servo_angle)
        elif servo_id == 2:
            return -degrees_to_radians(servo_angle)
        elif servo_id == 3:
            return degrees_to_radians(servo_angle)
        elif servo_id == 4:
            return degrees_to_radians(servo_angle)
        elif servo_id == 5:
            return -degrees_to_radians(servo_angle)
        
    def set_all_servo_angle(self):
        for i in self.uservo.servos:
            if abs(self.target_angle[i] - self.current_angle[i]) < self.DEAD_ZONE:
                # print(f"舵机{i}角度已到达目标位置,target_angle:{self.target_angle[i]},current_angle:{self.current_angle[i]}")
                continue
            if(self.target_angle[i] > self.current_angle[i]):
                self.current_angle[i] += 0.2
            else:
                self.current_angle[i] -= 0.2
            self.uservo.set_servo_angle4arm(i,self.current_angle[i])

    def servo_move_finished(self):
        for i in self.uservo.servos:
            if abs(self.target_angle[i] - self.current_angle[i]) > self.DEAD_ZONE:
                return False
        return True
    
    def goal_callback(self, goal_request):
        """Accept or reject a client request to begin an action."""
        # This server allows multiple goals in parallel
        # self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT
    
    def cancel_callback(self, goal_handle):
        """Accept or reject a client request to cancel an action."""
        # self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT
    
    # 动作接收处理
    def set_servo_angle_callback(self,goal_handle):
        goal_msg = goal_handle.request

        #DEBUG
        test = Float32MultiArray()
        test.data = [0.0,0.0,0.0,0.0,0.0,0.0]

        for i in range(len(goal_msg.target_angle)):
            if(i >= 6):
                break
            self.target_angle[goal_msg.servo_id[i]] = goal_msg.target_angle[i]

        # while not self.servo_move_finished():
        #     pass

        print("move finished")
        goal_handle.succeed()
        result = MoveArm.Result()
        result.result = True
        return result

    def timer_callback(self):
        if not self.servo_move_finished():
            self.set_all_servo_angle()

    def timer_callback2(self):
        pass
        # print("before query_servo_angle"+str(self.current_angle))
        # for i in self.uservo.servos:
            
        #     self.current_angle[i] =  self.uservo.query_servo_angle(i)
        # print("after query_servo_angle"+str(self.current_angle))

    def query_data_callback(self, request, response):
        command = request.command
        match command:
            case 'angle':
                for i in self.uservo.servos:
                    angle =self.uservo.query_servo_angle(i)
                    response.servo_name.append(self.joint_[i])
                    response.servo_data.append(self.servoangle2jointstate(i,self.uservo.servos[i].angle))
                formatted_string = ", ".join(map(lambda num: f"{num:.2f}", response.servo_data))
                print("read angle: ",formatted_string)
                return response
            case 'disable':
                for i in self.uservo.servos:
                    self.uservo.disable_torque(i)
                    response.servo_name.append(self.joint_[i])
                    response.servo_data.append(i)
                print("disable torque: ")
                return response
    
        
def main(args=None):
    rclpy.init(args=args)
    followerarm_subscriber = Arm_contorl()
    rclpy.spin(followerarm_subscriber)
    followerarm_subscriber.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()