# robo和其他模块的通信中转节点
import rclpy                            
from sensor_msgs.msg import JointState  
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node           
import time
from robo_interfaces.action import MoveArm
import math
from std_msgs.msg import Float32MultiArray
from .uservo import robo_Arm_Info
from robo_interfaces.msg import SetAngle
from control_msgs.action import FollowJointTrajectory


ROBO_ACTION_NODE = 'robo_action_client_node'+str(robo_Arm_Info.ID)
ROBO_CURRENT_ANGLE_SUBSCRIPTION = 'current_angle_topic'+str(robo_Arm_Info.ID)
ROBO_ACTION_CLIENT = 'move'+str(robo_Arm_Info.ID)
ROBO_SET_ANGLE_PUBLISHER ='set_angle_topic'+str(robo_Arm_Info.ID)

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
        return degrees_to_radians(servo_angle)
    elif servo_id == 4:
        return degrees_to_radians(servo_angle)
    elif servo_id == 5:
        return -degrees_to_meters(servo_angle)


class FollowJointTrajectoryNode(Node):
    def __init__(self):
        super().__init__('follow_joint_trajectory_node')
        




class RoboActionClient(Node):
    JOITN_ = ['robot_joint1','robot_joint2','robot_joint3','robot_joint4','hand_joint','grippers_joint','right_joint']
    INDEX_JOINT_ = {value: index for index, value in enumerate(JOITN_)}
    test_time = 0
    # goal_msg = None
    current_angle = [0.0,0.0,0.0,0.0,0.0,0.0]
    current_joint_state = [0.0,0.0,0.0,0.0,0.0,0.0]
    time_delay = 0
    last_time = 0

    def __init__(self):
        super().__init__(ROBO_ACTION_NODE)

        self.FollowJointTrajectoryNode = ActionServer(
            self,
            FollowJointTrajectory,
            '/arm_controller/follow_joint_trajectory',
            execute_callback = self.execute_callback,
        )

        self.get_logger().info('Follow Joint Trajectory server is ready.')


        self.joint_states_publisher = self.create_publisher(
            JointState,                                               
            'joint_states',1)

        # 创建话题 :接收current_angle_topic消息
        self.currentangle_subscription = self.create_subscription(
            Float32MultiArray,                                               
            ROBO_CURRENT_ANGLE_SUBSCRIPTION,
            self.current_angle_callback,1)

        self.set_angle_publishers = self.create_publisher(SetAngle,ROBO_SET_ANGLE_PUBLISHER,1)  
        self._goal_handle = None  # 存储当前目标句柄


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

        
    # 处理当前角度信息
    def current_angle_callback(self, msg):
        _data = msg.data
        for i in range(len(_data)):
            self.current_angle[i] = _data[i]
        self.joint_states_publisher_callback()


    def execute_callback(self, goal_handle):
        # 从目标消息中提取轨迹
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
            testdata = time_from_start - self.last_time
            self.test_time+=1

            goal_msg = SetAngle()

            for i in range(len(trajectory.joint_names)):
                goal_msg.servo_id.append(self.INDEX_JOINT_[trajectory.joint_names[i]])
                goal_msg.test_time = self.test_time
            #逐舵机计算
            for i in range(len(goal_msg.servo_id)):
                id = goal_msg.servo_id[i]

                if id == 5:
                    angle = meters_to_degrees(position[i])
                else:
                    angle = radians_to_degrees(position[i])
                if id == 2 or id == 5:
                    goal_msg.target_angle.append(-angle)
                else:
                    goal_msg.target_angle.append(angle)

                goal_msg.time.append((time_from_start - self.last_time)*1000.0)
            self.last_time = time_from_start

            self.set_angle_publishers.publish(goal_msg)
            sleep_time = goal_msg.time[0]/1000.0
            time.sleep(sleep_time)
        
        # 成功完成所有点，返回成功状态
        goal_handle.succeed()
        result = FollowJointTrajectory.Result()
        return result



def main(args=None):
    rclpy.init(args=args)
    action_client = RoboActionClient()
    rclpy.spin(action_client)
    action_client.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
