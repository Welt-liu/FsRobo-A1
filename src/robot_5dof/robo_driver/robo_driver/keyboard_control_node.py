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

JOINT_NAME = ['robot_joint1', 'robot_joint2', 'robot_joint3', 'robot_joint4', 'hand_joint', 'left_joint','right_joint']


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
    servo_num = 0                                    # 关节数量
    MIN_ANGLES = [-2.0, -0.9, -2.1, -2, -0.5, -1.1]  # 角度最小值
    MAX_ANGLES = [2.0, 1.5, 2.1, 1.5, 3.1, 0.0]      # 角度最大值    
    INCREMENT_VALUE = 0.087                          # # 按下一次按键时，增加的角度

    set_angle = [0.0,0.0,0.0,0.0,0.0,0.0]            # 普通控制模式
    cur_control_joint = 1                            # 当前调节的关节编号
    cur_angle =[0.0,0.0,0.0,0.0,0.0,0.0]
    saved_angle = []

    def __init__(self):
        self.angle_publisher = angle_publisher_() #角度发布节点
        self.servo_servicer = servo_servicer_() #接收舵机服务节点

        #curser图形界面初始化
        curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.wrapper(self.loop_)                  #启动wrapper，传入loop_函数

    def start_(self,stdscr):
        #初始化界面，显示欢迎信息
        self.height, self.width = stdscr.getmaxyx()
        stdscr.clear()
        message= '欢迎使用键盘控制机械臂节点'
        x = (self.width // 2) - (len(message))//2
        stdscr.addstr(0,x,message,curses.color_pair(1))

        message= '输入1开始普通控制模式,输入2开始示教模式'
        y = (self.height // 2)
        x = (self.width // 2) - (len(message))//2
        stdscr.addstr(y,x,message,curses.color_pair(1))
        stdscr.refresh()

    def normal_control_refresh(self,stdscr):
        # 刷新普通控制模式界面
        stdscr.clear()
        stdscr.addstr(1,0,'上下键：增减关节角度  || 左右键：切换修改的关节 ',curses.color_pair(1))
        stdscr.addstr(2,0,'S键：控制全部关节角度 || R键：读取全部关节角度',curses.color_pair(1))
        stdscr.addstr(5,0,f'正在修改{self.cur_control_joint}关节角度',curses.color_pair(1))

        angles_str = ', '.join(f'关节{i}: {self.set_angle[i-1]:.2f}' for i in range(1, self.servo_num+1))  # 格式化角度
        stdscr.addstr(6,0,f'当前设置角度: {angles_str}',curses.color_pair(1))

        cur_angle_str = ', '.join(f'关节{i}: {self.cur_angle[i-1]:.2f}' for i in range(1, self.servo_num+1))  # 格式化角度
        stdscr.addstr(8,0,f'回读角度: {cur_angle_str}',curses.color_pair(1))
        stdscr.addstr(10,0,f'ctrl+c键：退出',curses.color_pair(1))
        stdscr.refresh()

    def normal_control(self,stdscr):
        # 普通控制模式的主循环
        self.servo_num = 6
        while True:
            #刷新界面
            self.normal_control_refresh(stdscr)
            # 等待键盘输入
            key = stdscr.getch()  

            # 按键处理
            if key == ord('r')or key == ord('R'):
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

            if key == ord('s')or key == ord('S'):  # 按下t键发送命令
                self.angle_publisher.publish_angle(self.set_angle)
                

    
    def show_mode_refresh(self,stdscr,msg_str='',current_step=0):
        # 刷新示教模式界面
        stdscr.clear()
        stdscr.addstr(1,0,'S键：保存当前角度    / T键：按顺序执行命令，间隔1s')
        stdscr.addstr(2,0,'C键：清除保存的角度  / D键：失能所有关节')
        stdscr.addstr(4,0,msg_str,curses.color_pair(3))

        stdscr.move(6,0)
        for i in range(len(self.saved_angle)):
            if i == current_step:
                color = 2
            else:
                color = 1
            stdscr.addstr(f'第{i+1}组角度:',curses.color_pair(color))
            for j in range(len(self.saved_angle[i])):
                stdscr.addstr(f'{self.saved_angle[i][j]:.2f} ',curses.color_pair(color))
            stdscr.addstr('\n',curses.color_pair(color))
        stdscr.addstr('\n')
        stdscr.addstr(f'ctrl+c键：退出')

        stdscr.refresh()
           
    def show_mode(self,stdscr):
        #示教模式的主循环
        self.show_mode_msg_str = ''
        while True:
            self.show_mode_refresh(stdscr,self.show_mode_msg_str)
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
            elif key == ord('d') or key == ord('D'):  # 按下d,失能所有关节
                response  = self.servo_servicer.send_servo_request('disable')
                self.show_mode_msg_str ='已失能所有关节'
                self.show_mode_refresh(stdscr,self.show_mode_msg_str)
            elif key == ord('s') or key == ord('S'):  # 按下s,保存当前角度

                if len(self.saved_angle) >= self.height-10:
                    self.show_mode_msg_str = '保存角度已满，请先清除保存的角度或扩展终端行数'
                    self.show_mode_refresh(stdscr,self.show_mode_msg_str)
                    continue
                self.show_mode_msg_str = 'reading angle,please wait...'
                self.show_mode_refresh(stdscr,self.show_mode_msg_str)

                response  = self.servo_servicer.send_servo_request('angle')
                self.show_mode_msg_str ='cur angle: '
                self.servo_num = len(response.servo_name)
                for i in range(len(response.servo_name)):
                    index = JOINT_NAME.index(response.servo_name[i])
                    self.cur_angle[index] = response.servo_data[i]
                    self.show_mode_msg_str += f'{response.servo_name[i]}: {self.cur_angle[index]:.2f} '

                self.show_mode_refresh(stdscr,self.show_mode_msg_str)

                self.saved_angle.append(self.cur_angle.copy())
            elif key == ord('t') or key == ord('T'):
                for i in range(len(self.saved_angle)):
                    #格式化字符串，输出当前目标角度
                    self.show_mode_refresh(stdscr,msg_str= 'running step ',current_step=i)
                    self.angle_publisher.publish_angle(self.saved_angle[i])

                    time.sleep(1)
                self.show_mode_msg_str = 'running finished'
                self.show_mode_refresh(stdscr,msg_str= self.show_mode_msg_str,current_step=i)
            elif key == ord('c') or key == ord('C'):
                self.saved_angle.clear()
                self.show_mode_msg_str = 'saved angle cleared'
                self.show_mode_refresh(stdscr,self.show_mode_msg_str)
            


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
