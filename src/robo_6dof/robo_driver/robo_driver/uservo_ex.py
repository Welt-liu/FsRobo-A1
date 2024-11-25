'''
舵机转手臂控制通用类
'''
import math

class uservo_ex:
	JOITN_ = ['robot_joint1','robot_joint2','robot_joint3','robot_joint4','hand_joint','grippers_joint','right_joint']
	INDEX_JOINT_ = {value: index for index, value in enumerate(JOITN_)}
	SERVO_PORT_NAME =  u'/dev/ttyUSB0'      # 舵机串口号 <<< 修改为实际串口号
	SERVO_BAUDRATE = 115200                 # 舵机的波特率
	ID = 1									# 多手臂时区分话题ID
	servo_ids = list()

	def __init__(self):
		pass
	#返回虚拟关节的名称
	@classmethod
	def fake_joint_name(cls):
		return 'right_joint'

	#将弧度转为角度
	@classmethod
	def radians_to_degrees(cls,radians):
		degrees = radians * (180 / math.pi)
		return degrees
	
	#将米转为角度
	@classmethod
	def meters_to_degrees(cls,meters):
		degrees = (meters/0.027) * 50
		return degrees
	
	#将角度转为弧度
	@classmethod
	def degrees_to_radians(degrees):
		radians = degrees * (math.pi / 180)
		return radians

	#将角度转为米
	@classmethod
	def degrees_to_meters(degrees):
		meters = (degrees/50) * 0.027
		return meters
	
	@classmethod
	def jointstate2servoangle(cls,servo_id,joint_state):
		if servo_id == 0:
			return cls.radians_to_degrees(joint_state)
		elif servo_id == 1:
			return cls.radians_to_degrees(joint_state)
		elif servo_id == 2:
			return cls.radians_to_degrees(-joint_state)
		elif servo_id == 3:
			return cls.radians_to_degrees(-joint_state)
		elif servo_id == 4:
			return cls.radians_to_degrees(-joint_state)
		elif servo_id == 5:
			return cls.meters_to_degrees(joint_state)
		else:
			return 0
	@classmethod
	#将舵机角度转换为关节位置
	def servoangle2jointstate(cls,servo_id,servo_angle):
		if servo_id == 0:
			return cls.degrees_to_radians(servo_angle)
		elif servo_id == 1:
			return cls.degrees_to_radians(servo_angle)
		elif servo_id == 2:
			return -cls.degrees_to_radians(servo_angle)
		elif servo_id == 3:
			return -cls.degrees_to_radians(servo_angle)
		elif servo_id == 4:
			return -cls.degrees_to_radians(servo_angle)
		elif servo_id == 5:
			return -cls.degrees_to_meters(servo_angle)


	def __init__(self):
		print("UartServo init")
         # 初始化串口
        success = False
        while not success:
            try:
                self.uart = serial.Serial(port=uservo_ex.SERVO_PORT_NAME, baudrate=uservo_ex.SERVO_BAUDRATE,
                                            parity=serial.PARITY_NONE, stopbits=1,
                                            bytesize=8, timeout=0)
                success = True  # 如果成功初始化，则设置成功标志
            except serial.SerialException as e:
                print(f"串口初始化失败: {e}")
                time.sleep(0.1)  # 暂停 1 秒后重试
        try:
            self.uservo = UartServoManager(self.uart,srv_num=6)
        except Exception as e:
            print(f"UartServoManager初始化失败: {e}")
        self.servo_ids = list(self.uservo.servos.keys())
        # self.get_logger().info("手臂在线舵机ID: {}".format(servo_ids))
    #归零 
    def  move_to_zero(self):
        #归零
        command_data_list = [
            struct.pack('<BhHH',i,int(START_ANGLE[i]*10), 6000, 0)for i in range(6)
        ]
        command_data_list += [struct.pack('<BhHH', 9, 0, 6000, 0)]
        self.uservo.send_sync_angle(8, 7, command_data_list)

    def set_angle(self,msg):
        command_data_list = [struct.pack('<BhHH', msg.servo_id[i], int(msg.target_angle[i]*10), int(msg.time[i]), 0)for i in range(len(msg.target_angle))]
        self.uservo.send_sync_angle(8, len(msg.target_angle), command_data_list)

    def query_servo_current_angle(self,servo_id):
        angle = self.uservo.query_servo_angle(servo_id)
        return angle

    def disable_all_torque(self):
        for i in self.uservo.servos:
            self.disable_torque(i)

    
	def disable_torque(self,servo_id):
    	self.uservo.disable_torque(servo_id)