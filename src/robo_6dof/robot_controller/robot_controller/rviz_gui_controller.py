#!/usr/bin/env python
#coding:utf-8

'''
rviz_gui 控制器节点

'''
import rclpy
from rclpy.node import Node


class Rviz_Gui_Controller_Node(Node):
    isakaka = 1


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