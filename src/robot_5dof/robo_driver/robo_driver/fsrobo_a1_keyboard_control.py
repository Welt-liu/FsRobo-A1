#!/usr/bin/env python
#coding:utf-8

'''
键盘控制机械臂节点
通过发送JointState话题消息来控制机械臂的关节角度
'''

import rclpy
from rclpy.node import Node

import curses
# from rclpy.node import Node
from sensor_msgs.msg import JointState

class angle_publisher_(Node):
    
    # keyboard = keyboard_control()
    def __init__(self):
        super().__init__('keyboard_control_node')
        self.angle_publishers = self.create_publisher(
            JointState,                                               
            'joint_states',
            10)
    
    def publish_angle(self,position):
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = ['robot_joint1', 'robot_joint2', 'robot_joint3', 'robot_joint4', 'hand_joint', 'left_joint']
        joint_state.position = position
        self.angle_publishers.publish(joint_state)


class keyboard_control_:
    

    MIN_ANGLES = [-2.0, -0.9, -2.1, -2, -0.5, -1.1]  # 示例最小值
    MAX_ANGLES = [2.0, 1.5, 2.1, 1.5, 3.1, 0.0]         # 示例最大值    
    INCREMENT_VALUE = 0.087 # 按下一次按键时，增加的角度

    angles = [0.0,0.0,0.0,0.0,0.0,0.0] 
    cur_control_joint = 1  # 当前控制的关节编号

    def __init__(self):
        self.angle_publisher = angle_publisher_()
        curses.wrapper(self.loop_) #启动wrapper，传入loop_函数

    def refresh_(self,stdscr):
        
        stdscr.clear()
        stdscr.addstr(0,0,'请确认终端显示行/列数是否足够\n')
        stdscr.addstr(1,0,'键盘1~6切换控制关节(包括末端夹爪),键盘上下键增减关节角度,S键发送命令,按下q退出\n')
        angles_str = ', '.join(f'关节{i}: {self.angles[i-1]:.2f}' for i in range(1, 7))  # 格式化角度
        stdscr.addstr(3,0,f'正在修改关节{self.cur_control_joint}') 
        stdscr.addstr(4,0,f'当前角度: {angles_str}') 
        stdscr.refresh()
        
    def loop_(self,stdscr):

        self.refresh_(stdscr)

        while True:
            key = stdscr.getch()  # 等待键盘输入

            if key == ord('q'):  # 按下 'q' 键退出
                break

            elif key == ord('1'):
                self.cur_control_joint = 1
                self.angle_publisher.publish_angle(self.angles)
            elif key == ord('2'):
                self.cur_control_joint = 2
            elif key == ord('3'):
                self.cur_control_joint = 3
            elif key == ord('4'):
                self.cur_control_joint = 4
            elif key == ord('5'):
                self.cur_control_joint = 5
            elif key == ord('6'):
                self.cur_control_joint = 6
            
            elif key == curses.KEY_UP:
                self.angles[self.cur_control_joint-1] += self.INCREMENT_VALUE
            elif key == curses.KEY_DOWN:
                self.angles[self.cur_control_joint-1] -= self.INCREMENT_VALUE
            elif key == curses.KEY_LEFT:
                if  self.cur_control_joint  > 1:
                    self.cur_control_joint -=1
            elif key == curses.KEY_RIGHT:
                if  self.cur_control_joint  < 6:
                    self.cur_control_joint +=1
            elif key == ord('s'):  # 按下S键发送命令
                self.angle_publisher.publish_angle(self.angles)
                
            for i in range(len(self.angles)):
                if self.angles[i] < self.MIN_ANGLES[i]:
                    self.angles[i] = self.MIN_ANGLES[i]
                elif self.angles[i] > self.MAX_ANGLES[i]:
                    self.angles[i] = self.MAX_ANGLES[i]
            
            self.refresh_(stdscr)



        

def main(args=None):
    
    rclpy.init(args=args)
    
    keyboard_contro = keyboard_control_()
    
    rclpy.spin(keyboard_contro.angle_publisher)

    keyboard_contro.angle_publisher.destroy_node()

    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
