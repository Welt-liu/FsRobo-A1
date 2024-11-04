#!/usr/bin/env python
#coding:utf-8

'''
键盘控制机械臂节点
通过发送JointState话题消息来控制机械臂的关节角度
'''

import rclpy
from rclpy.node import Node
import curses
from sensor_msgs.msg import JointState
from robo_interfaces.srv import RoboStates
import time

JOINT_NAME = ['robot_joint1', 'robot_joint2', 'robot_joint3', 'robot_joint4', 'hand_joint', 'left_joint']


class angle_publisher_(Node):
    #初始化节点
    def __init__(self):
        super().__init__('keyboard_control_node')
        self.angle_publishers = self.create_publisher(
            JointState,                                               
            'joint_states',
            1)
    
    def publish_angle(self,_position):
        joint_state = JointState()
        # joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = JOINT_NAME
        
        position = list(map(float, _position))  # 转换为浮点数数组
        joint_state.position = position
        self.angle_publishers.publish(joint_state)

class servo_servicer_(Node):

    def __init__(self):
        super().__init__('servo_servicer_node')
        self.cli = self.create_client(RoboStates, 'robo_states')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = RoboStates.Request()

    def send_servo_request(self, command):
        self.req.command = command
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()





class keyboard_control_:
    
    MIN_ANGLES = [-2.0, -0.9, -2.1, -2, -0.5, -1.1]  # 角度最小值
    MAX_ANGLES = [2.0, 1.5, 2.1, 1.5, 3.1, 0.0]         # 角度最大值    
    INCREMENT_VALUE = 0.087 # 按下一次按键时，增加的角度

    set_angle = [0.0,0.0,0.0,0.0,0.0,0.0] 
    cur_control_joint = 1  # 当前控制的关节编号
    cur_angle =[0.0,0.0,0.0,0.0,0.0,0.0]
    saved_angle = []

    def __init__(self):
        self.angle_publisher = angle_publisher_()
        self.servo_servicer = servo_servicer_()
        curses.wrapper(self.loop_) #启动wrapper，传入loop_函数

    def start_(self,stdscr):
        self.height, self.width = stdscr.getmaxyx()
        stdscr.clear()
        message= '欢迎使用键盘控制机械臂节点'
        x = (self.width // 2) - (len(message))//2
        stdscr.addstr(0,x,message)

        message= '输入1开始常规控制,输入2开始示教模式'
        y = (self.height // 2)
        x = (self.width // 2) - (len(message))//2
        stdscr.addstr(y,x,message)
        stdscr.refresh()

    def normal_control_refresh(self,stdscr):
        stdscr.clear()
        stdscr.addstr(1,0,'上下键：增减关节角度  || 左右键：切换修改的关节 ')
        stdscr.addstr(2,0,'T键：控制全部关节角度 || R键：读取全部关节角度')
        stdscr.addstr(5,0,f'正在修改{self.cur_control_joint}关节角度')

        angles_str = ', '.join(f'关节{i}: {self.set_angle[i-1]:.2f}' for i in range(1, 7))  # 格式化角度
        stdscr.addstr(6,0,f'当前设置角度: {angles_str}')

        cur_angle_str = ', '.join(f'关节{i}: {self.cur_angle[i-1]:.2f}' for i in range(1, 7))  # 格式化角度
        stdscr.addstr(8,0,f'回读角度: {cur_angle_str}')
        stdscr.addstr(10,0,f'ctrl+c键：退出')
        stdscr.refresh()

    def normal_control(self,stdscr):
        while True:
            self.normal_control_refresh(stdscr)
            key = stdscr.getch()  # 等待键盘输入

            if key == ord('r'):
                response  = self.servo_servicer.send_servo_request('angle')
                for i in range(len(response.servo_name)):
                    index = JOINT_NAME.index(response.servo_name[i])
                    self.cur_angle[index] = response.servo_data[i]
            
            elif key == curses.KEY_UP:
                self.set_angle[self.cur_control_joint-1] += self.INCREMENT_VALUE
            elif key == curses.KEY_DOWN:
                self.set_angle[self.cur_control_joint-1] -= self.INCREMENT_VALUE
            elif key == curses.KEY_LEFT:
                if  self.cur_control_joint  > 1:
                    self.cur_control_joint -=1
            elif key == curses.KEY_RIGHT:
                if  self.cur_control_joint  < 6:
                    self.cur_control_joint +=1

            for i in range(len(self.set_angle)):
                if self.set_angle[i] < self.MIN_ANGLES[i]:
                    self.set_angle[i] = self.MIN_ANGLES[i]
                elif self.set_angle[i] > self.MAX_ANGLES[i]:
                    self.set_angle[i] = self.MAX_ANGLES[i]

            if key == ord('t'):  # 按下t键发送命令
                self.angle_publisher.publish_angle(self.set_angle)
                
    debug_data = 0

    # 示教模式
    def show_mode_refresh(self,stdscr):
        stdscr.clear()
        stdscr.addstr(1,0,'上下键：增减关节角度  || 左右键：切换修改的关节 ')
        stdscr.addstr(2,0,'T键：按顺序执行命令，间隔1s || S键：保存当前角度，最多保存10组')
        stdscr.addstr(3,0,'C键：清除保存的角度')
        stdscr.addstr(5,0,f'ctrl+c键：退出')
        stdscr.addstr(6,0,f'debug_data: {self.debug_data}')
        stdscr.refresh()
           
    def show_mode(self,stdscr):
        while True:
            self.show_mode_refresh(stdscr)
            key = stdscr.getch()  # 等待键盘输入

            if key == curses.KEY_UP:
                self.set_angle[self.cur_control_joint-1] += self.INCREMENT_VALUE
            elif key == curses.KEY_DOWN:
                self.set_angle[self.cur_control_joint-1] -= self.INCREMENT_VALUE
            elif key == curses.KEY_LEFT:
                if  self.cur_control_joint  > 1:
                    self.cur_control_joint -=1
            elif key == curses.KEY_RIGHT:
                if  self.cur_control_joint  < 6:
                    self.cur_control_joint +=1         

            elif key == ord('s'):  # 按下s键发送命令
                response  = self.servo_servicer.send_servo_request('angle')
                if len(self.saved_angle) >= 10:
                    continue
                for i in range(len(response.servo_name)):
                    index = JOINT_NAME.index(response.servo_name[i])
                    self.cur_angle[index] = response.servo_data[i]
                self.saved_angle.append(self.cur_angle.copy())
            elif key == ord('t'):
                for i in range(len(self.saved_angle)):

                    self.angle_publisher.publish_angle(self.saved_angle[i])
                    
                    time.sleep(1)
        

    def loop_(self,stdscr):
        
        self.start_(stdscr)

        mode = stdscr.getch()  # 等待键盘输入
        if mode == ord('1'):
            self.normal_control(stdscr)
        elif mode == ord('2'):
            self.show_mode(stdscr)


def main(args=None):

    rclpy.init(args=args)
    keyboard_contro = keyboard_control_()
    rclpy.spin(keyboard_contro.angle_publisher)
    keyboard_contro.angle_publisher.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
