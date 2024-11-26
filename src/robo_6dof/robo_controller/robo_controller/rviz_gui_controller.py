#!/usr/bin/env python
#coding:utf-8

'''
rviz_gui 控制器节点

'''
import rclpy
from rclpy.node import Node
from robo_driver.uservo_ex import uservo_ex
from robo_interfaces.msg import SetAngle
from sensor_msgs.msg import JointState
import time
# import math

RVIZ_GUI_CONTROLLER_NODE = 'rviz_gui_controller_node'+str(uservo_ex.ID)
ROBO_SET_ANGLE_PUBLISHER ='set_angle_topic'+str(uservo_ex.ID)


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
        self.get_logger().info("rviz_gui_controller_node is started")

    def set_servo_angle_callback(self, msg):
        goal_msg = SetAngle()

        for i in range(len(msg.name)):
            if msg.name[i] == uservo_ex.fake_joint_name :
                continue
            goal_msg.servo_id.append(uservo_ex.INDEX_JOINT_[msg.name[i]])
            goal_msg.target_angle.append(uservo_ex.jointstate2servoangle(servo_id = goal_msg.servo_id[i], joint_state = msg.position[i]))
        
        goal_msg.test_time = 0

        delay_time = 50.0
        goal_msg.time = [delay_time for _ in range(6)]
        print(goal_msg)
        self.set_angle_publishers.publish(goal_msg)
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