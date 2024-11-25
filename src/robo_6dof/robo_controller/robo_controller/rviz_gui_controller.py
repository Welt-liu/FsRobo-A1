#!/usr/bin/env python
#coding:utf-8

'''
rviz_gui 控制器节点

'''
import rclpy
from rclpy.node import Node
from robo_driver.uservo import robo_Arm_Info
from robo_interfaces.msg import SetAngle
from sensor_msgs.msg import JointState
import time
import math

RVIZ_GUI_CONTROLLER_NODE = 'rviz_gui_controller_node'+str(robo_Arm_Info.ID)
ROBO_SET_ANGLE_PUBLISHER ='set_angle_topic'+str(robo_Arm_Info.ID)
JOITN_ = ['robot_joint1','robot_joint2','robot_joint3','robot_joint4','hand_joint','grippers_joint','right_joint']
INDEX_JOINT_ = {value: index for index, value in enumerate(JOITN_)}

#将弧度转为角度
def radians_to_degrees(radians):
    degrees = radians * (180 / math.pi)
    return degrees
#将米转为角度
def meters_to_degrees(meters):
    degrees = (meters/0.027) * 50
    return degrees

def jointstate2servoangle(servo_id,joint_state):
    if servo_id == 0:
        return radians_to_degrees(joint_state)
    elif servo_id == 1:
        return radians_to_degrees(joint_state)
    elif servo_id == 2:
        return radians_to_degrees(-joint_state)
    elif servo_id == 3:
        return radians_to_degrees(-joint_state)
    elif servo_id == 4:
        return radians_to_degrees(-joint_state)
    elif servo_id == 5:
        return meters_to_degrees(joint_state)
    else:
        return 0


class Rviz_Gui_Controller_Node(Node):
    def __init__(self):
        super().__init__(RVIZ_GUI_CONTROLLER_NODE)
         # 创建话题 :接收joint_states消息
        self.subscription = self.create_subscription(
            JointState,                        
            'joint_states',
            self.set_servo_angle_callback,1)
        #发布角度控制话题
        self.set_angle_publishers = self.create_publisher(
            SetAngle,ROBO_SET_ANGLE_PUBLISHER,
            1)

    def set_servo_angle_callback(self, msg):
        goal_msg = SetAngle()

        for i in range(len(msg.name)):
            if self.index_joint_[msg.name[i]] not in self.uservo.servos:
                continue
            goal_msg.servo_id.append(self.index_joint_[msg.name[i]])
            goal_msg.target_angle.append(jointstate2servoangle(servo_id = goal_msg.servo_id[i], joint_state = msg.position[i]))
            goal_msg.test_time.append(0.0)
            

        delay_time = 2000.0
        goal_msg.time = [delay_time for _ in range(6)]
        print(goal_msg)
        # self.set_angle_publishers.publish(goal_msg)
        time.sleep(delay_time*0.001)


def main(args=None):
    rclpy.init(args=args)
    node = Rviz_Gui_Controller_Node()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()