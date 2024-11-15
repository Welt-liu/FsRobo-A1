# robo和其他模块的通信中转节点
import rclpy                            # type: ignore
from sensor_msgs.msg import JointState  # type: ignore
from rclpy.action import ActionClient   # type: ignore
from rclpy.node import Node             # type: ignore
import time
from robo_interfaces.action import MoveArm
import math
from std_msgs.msg import Float32MultiArray
from .uservo import robo_Arm_Info

ROBO_ACTION_NODE = 'robo_action_client_node'+str(robo_Arm_Info.ID)
ROBO_CURRENT_ANGLE_SUBSCRIPTION = 'current_angle_topic'+str(robo_Arm_Info.ID)
ROBO_ACTION_CLIENT = 'move'+str(robo_Arm_Info.ID)


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
    test_time = 0
    goal_msg = None
    current_angle = [0.0,0.0,0.0,0.0,0.0,0.0]
    current_joint_state = [0.0,0.0,0.0,0.0,0.0,0.0]
    time_delay = 0
    def __init__(self):
        super().__init__(ROBO_ACTION_NODE)

        self.timer = self.create_timer(0.01,self.timer_callback)  # 设置定时器，每0.01秒调用一次
        # 创建话题 :接收joint_states消息
        self.subscription = self.create_subscription(
            JointState,                                               
            'joint_states',
            self.joint_states_callback,1)
        # 创建话题 :接收current_angle_topic消息
        self.subscription = self.create_subscription(
            Float32MultiArray,                                               
            ROBO_CURRENT_ANGLE_SUBSCRIPTION,
            self.current_angle_callback,1)


        self._action_client = ActionClient(self, MoveArm, ROBO_ACTION_CLIENT)
        self._goal_handle = None  # 存储当前目标句柄
        print("action client init")

    def send_command_with_cancel(self,msg):
        # # 如果有当前正在执行的目标，先取消它
        # if self._goal_handle:
        #     print("Canceling previous goal")
        #     future = self._goal_handle.cancel_goal_async()
        #     future.add_done_callback(self.cancel_done)
        # 发送新的命令
        self._send_goal_future = self._action_client.send_goal_async(msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        # self._current_goal_handle = self.send_future.result() 

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :('+str(goal_handle.goal_id))
            return

        self._goal_handle = goal_handle
        # self.get_logger().info('Goal accepted :)')

        # future = self._goal_handle.cancel_goal_async()
        # future.add_done_callback(self.cancel_done)

    
    def cancel_done(self, future):
        cancel_response = future.result()
        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info('Goal successfully canceled')
        else:
            self.get_logger().info('Goal failed to cancel')


    def joint_states_callback(self, msg):
        for i in range(len(msg.name)):
            if msg.name[i] != 'right_joint':
                id = self.INDEX_JOINT_[msg.name[i]]

                self.current_joint_state[id] = msg.position[i]
               

    def current_angle_callback(self, msg):
        _data = msg.data
        for i in range(len(_data)):
            self.current_angle[i] = _data[i]

    def timer_callback(self):
        if 1 == 0:
            goal_msg = MoveArm.Goal()
            for i in range(len(self.joint_name)):
                if self.joint_name[i] == 'default':
                    continue
                id = self.INDEX_JOINT_[self.joint_name[i]]
                if id == 5:
                    angle = meters_to_degrees(self.current_joint_state[i])
                else:
                    angle = radians_to_degrees(self.current_joint_state[i])
                goal_msg.servo_id.append(id)

                if id == 2 or id == 5:
                    goal_msg.target_angle.append(-angle)
                else:
                    goal_msg.target_angle.append(angle)
            self.send_command_with_cancel(goal_msg)
        else:
            if self.time_delay <= 0:
                goal_msg = MoveArm.Goal()
                goal_msg.servo_id = [0,1,2,3,4,5]
                goal_msg.target_angle = [0.0,0.0,0.0,0.0,0.0,0.0]
                goal_msg.time = [1145.51,1145.51,1145.51,1145.51,1145.51,1145.51]
                goal_msg.test_time = self.test_time

                for id in range(len(goal_msg.servo_id)):
                    
                    if id == 5:
                        angle = meters_to_degrees(self.current_joint_state[id])
                    else:
                        angle = radians_to_degrees(self.current_joint_state[id])

                    if id == 2 or id == 5:
                        goal_msg.target_angle[id] = -angle
                        
                    else:
                        goal_msg.target_angle[id] = angle
                        # time = 200*abs(goal_msg.target_angle[id] - self.current_angle[id])/3.0
                    time = 100*abs(goal_msg.target_angle[id] - self.current_angle[id])/3.0
                    #计算单颗舵机的时间
                    #tree
                    if id <4     :
                        goal_msg.time[id] = time
                        if self.time_delay<time:
                            self.time_delay = time


                print(f'delay_time:{self.time_delay},test_time:{self.test_time}')
                self.send_command_with_cancel(goal_msg)
            else:
                self.time_delay -= 10

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
