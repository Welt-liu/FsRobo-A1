# robo和其他模块的通信中转节点
import rclpy                            # type: ignore
from sensor_msgs.msg import JointState  # type: ignore
from rclpy.action import ActionClient   # type: ignore
from rclpy.node import Node             # type: ignore
import time
from robo_interfaces.action import MoveArm
import math

#将米转为角度
def meters_to_degrees(meters):
    degrees = (meters/0.027) * 50
    return degrees
#将弧度转为角度
def radians_to_degrees(radians):
    degrees = radians * (180 / math.pi)
    return degrees

class RoboActionClient(Node):
    JOITN_ = ['robot_joint1','robot_joint2','robot_joint3','robot_joint4','hand_joint','grippers_joint','right_joint']
    INDEX_JOINT_ = {value: index for index, value in enumerate(JOITN_)}

    goal_msg = None

    def __init__(self):
        super().__init__('robo_action_client_node')

        self.timer = self.create_timer(0.002,self.timer_callback)  # 设置定时器，每0.2秒调用一次
        # 创建话题 :接收joint_states消息
        self.subscription = self.create_subscription(
            JointState,                                               
            'joint_states',
            self.joint_states_callback,10)
        
        self._action_client = ActionClient(self, MoveArm, 'move')
        self._goal_handle = None  # 存储当前目标句柄
        print("action client init")

    def send_command_with_cancel(self):
        # # 如果有当前正在执行的目标，先取消它
        # if self._goal_handle:
        #     print("Canceling previous goal")
        #     future = self._goal_handle.cancel_goal_async()
        #     future.add_done_callback(self.cancel_done)
        # 发送新的命令
        self._send_goal_future = self._action_client.send_goal_async(self.goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        # self._current_goal_handle = self.send_future.result() 

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :('+str(goal_handle.goal_id))
            return

        self._goal_handle = goal_handle
        self.get_logger().info('Goal accepted :)')

        # future = self._goal_handle.cancel_goal_async()
        # future.add_done_callback(self.cancel_done)

    
    def cancel_done(self, future):
        cancel_response = future.result()
        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info('Goal successfully canceled')
        else:
            self.get_logger().info('Goal failed to cancel')


    def joint_states_callback(self, msg):
        self.goal_msg = MoveArm.Goal()
        for i in range(len(msg.name)):
            id = self.INDEX_JOINT_[msg.name[i]]
            angle = radians_to_degrees(msg.position[i])
            self.goal_msg.servo_id.append(id)

            if id == 2 or id == 5:
                self.goal_msg.target_angle.append(-angle)
            else:
                self.goal_msg.target_angle.append(angle)

    def timer_callback(self):
        # #取消上一个命令
        if self.goal_msg:

            self.send_command_with_cancel()



def main(args=None):
    rclpy.init(args=args)
    action_client = RoboActionClient()
    rclpy.spin(action_client)
    # future = action_client.send_goal(10)
    # rclpy.spin_until_future_complete(action_client, future)
    action_client.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
