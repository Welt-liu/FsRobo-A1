# robo和其他模块的通信中转节点
import rclpy                            
from sensor_msgs.msg import JointState  
from rclpy.action import ActionServer, CancelResponse
from rclpy.node import Node
import time
# from robo_interfaces.action import MoveArm
import math
from std_msgs.msg import Float32MultiArray
from robo_driver.uservo import robo_Arm_Info
from robo_interfaces.msg import SetAngle
from control_msgs.action import FollowJointTrajectory
from control_msgs.action import GripperCommand
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

ROBO_ACTION_NODE = 'robo_action_client_node'+str(robo_Arm_Info.ID)
ROBO_CURRENT_ANGLE_SUBSCRIPTION = 'current_angle_topic'+str(robo_Arm_Info.ID)
ROBO_SET_ANGLE_PUBLISHER ='set_angle_topic'+str(robo_Arm_Info.ID)
ROBO_ARM_ACTION_SERVER = '/arm_controller/follow_joint_trajectory'
ROBO_GIRRPER_ACTION_SERVER = '/grippers_controller/gripper_cmd'

#将米转为角度
def meters_to_degrees(meters):
    degrees = (meters/0.027) * 50
    return degrees
#将角度转为米
def degrees_to_meters(degrees):
    meters = (degrees/50) * 0.027
    return meters
#将弧度转为角度
def radians_to_degrees(radians):
    degrees = radians * (180 / math.pi)
    return degrees
#将角度转为弧度
def degrees_to_radians(degrees):
    radians = degrees * (math.pi / 180)
    return radians

#将舵机角度转换为关节位置
def servoangle2jointstate(servo_id,servo_angle):
    if servo_id == 0:
        return degrees_to_radians(servo_angle)
    elif servo_id == 1:
        return degrees_to_radians(servo_angle)
    elif servo_id == 2:
        return -degrees_to_radians(servo_angle)
    elif servo_id == 3:
        return -degrees_to_radians(servo_angle)
    elif servo_id == 4:
        return -degrees_to_radians(servo_angle)
    elif servo_id == 5:
        return -degrees_to_meters(servo_angle)

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





class RoboActionClient(Node):
    JOITN_ = ['robot_joint1','robot_joint2','robot_joint3','robot_joint4','hand_joint','grippers_joint','right_joint']
    INDEX_JOINT_ = {value: index for index, value in enumerate(JOITN_)}
    test_time = 0
    current_angle = [0.0,0.0,0.0,0.0,0.0,0.0]
    current_joint_state = [0.0,0.0,0.0,0.0,0.0,0.0]
    last_time = 0

    def __init__(self):
        super().__init__(ROBO_ACTION_NODE)

        self.callback_group = ReentrantCallbackGroup()
        # 创建手臂动作服务器
        self.Arm_FollowJointTrajectoryNode = ActionServer(
            self,
            FollowJointTrajectory,
            ROBO_ARM_ACTION_SERVER,
            execute_callback = self.arm_execute_callback,
            cancel_callback = self.arm_cancel_callback,
            callback_group=self.callback_group
        )
        #创建夹爪动作服务器
        self.Arm_FollowJointTrajectoryNode = ActionServer(
            self,
            GripperCommand,
            ROBO_GIRRPER_ACTION_SERVER,
            execute_callback = self.gripper_execute_callback,
            cancel_callback = self.gripper_cancel_callback,
            callback_group=self.callback_group
        )
        # 创建话题 :接收current_angle_topic消息
        self.currentangle_subscription = self.create_subscription(
            Float32MultiArray,                                               
            ROBO_CURRENT_ANGLE_SUBSCRIPTION,
            self.current_angle_callback,
            1,
            callback_group=self.callback_group)
        # 发布joint_states话题
        self.joint_states_publisher = self.create_publisher(
            JointState,                                               
            'joint_states',
            1)
        #发布角度控制话题
        self.set_angle_publishers = self.create_publisher(
            SetAngle,ROBO_SET_ANGLE_PUBLISHER,
            1)

        self.get_logger().info('robo_controller_node is ready.')

    def arm_cancel_callback(self,cancel_request):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    #发布joint_states消息
    def joint_states_publisher_callback(self):
        JointState_msg = JointState()
        JointState_msg.header.stamp = self.get_clock().now().to_msg()
        JointState_msg.velocity = []  # 如果无速度值可留空
        JointState_msg.effort = []  # 同上
        for i in range(len(self.current_angle)):
            JointState_msg.name.append(self.JOITN_[i])
            JointState_msg.position.append(servoangle2jointstate(servo_id=i,servo_angle=self.current_angle[i]))
            
        self.joint_states_publisher.publish(JointState_msg)

        
    # 接收机械臂当前角度话题回调
    def current_angle_callback(self, msg):
        _data = msg.data
        for i in range(len(_data)):
            self.current_angle[i] = _data[i]
        self.joint_states_publisher_callback()

    # 处理动作服务器回调
    def arm_execute_callback(self, goal_handle):
        trajectory = goal_handle.request.trajectory
        self.get_logger().info(f'Receiving trajectory with {len(trajectory.points)} points.')
        self.last_time = 0

        for index,point in enumerate(trajectory.points):
            position = point.positions
            time_from_start = point.time_from_start.sec + point.time_from_start.nanosec/1e9
            # 处理每个关节的目标位置
            if time_from_start - self.last_time <0.2 and index != len(trajectory.points)-1:
                print(f'point {index} is too close to last point, skip it.')
                continue
            run_time = time_from_start - self.last_time
            self.test_time+=1
            goal_msg = SetAngle()

            for i in range(len(trajectory.joint_names)):
                goal_msg.servo_id.append(self.INDEX_JOINT_[trajectory.joint_names[i]])
                goal_msg.test_time = self.test_time
            #逐舵机计算
            for i in range(len(goal_msg.servo_id)):
                goal_msg.target_angle.append(jointstate2servoangle(servo_id = goal_msg.servo_id[i], joint_state = position[i]))
                goal_msg.time.append((run_time)*1000.0)

            self.last_time = time_from_start

            self.set_angle_publishers.publish(goal_msg)
            sleep_time = goal_msg.time[0]/1000.0
            time.sleep(sleep_time)
        
        # 成功完成所有点，返回成功状态
        goal_handle.succeed()
        result = FollowJointTrajectory.Result()
        return result

    def gripper_cancel_callback(self,cancel_request):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def gripper_execute_callback(self, goal_handle):
        pass
        position = goal_handle.request.command.position 
        max_effort = goal_handle.request.command.max_effort

        goal_msg = SetAngle()
        goal_msg.servo_id.append(5)
        goal_msg.target_angle.append(jointstate2servoangle(servo_id = 5, joint_state = position))
        goal_msg.time.append(1000.0)
        print(f"max_effort:{max_effort}")
        self.set_angle_publishers.publish(goal_msg)
            # 成功完成所有点，返回成功状态
        goal_handle.succeed()

        result = GripperCommand.Result()
        return result



def main(args=None):
    rclpy.init(args=args)
    action_client = RoboActionClient()
    executor = MultiThreadedExecutor()
    #executor = PriorityExecutor()
    executor.add_node(action_client)
    executor.spin()
    # rclpy.spin(action_client)
    # action_client.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
