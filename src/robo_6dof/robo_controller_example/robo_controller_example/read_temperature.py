import rclpy
from rclpy.node import Node
from robo_interfaces.srv import RoboStates
import time

class ExampleNode(Node):
    start_temp = [0.0,0.0,0.0,0.0,0.0,0.0]
    def __init__(self):
        super().__init__('example_node')
        self.start_time = time.time()
        self.first = True
        self.servo_servicer = self.create_client(RoboStates, 'robo_states')
        while not self.servo_servicer.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.get_logger().info('service available')
        
        self.loop_()

    
    def query_servo_temp(self):
        req = RoboStates.Request()
        req.command = 'temperature'
        self.get_logger().info('等待..')
        future = self.servo_servicer.call_async(req)
        self.servo_servicer.wait_for_service()
        rclpy.spin_until_future_complete(self, future)
        return future.result()
    
    def loop_(self):
        while True:
            result = self.query_servo_temp()
            if self.first:
                for i in range(len(result.servo_data)):
                    self.start_temp[i] = result.servo_data[i]
                self.first = False
            else:
                print(f'current time {time.time() - self.start_time:.2f}')
            for i in range(len(result.servo_data)):
                print(f'舵机{i+1}温度:{result.servo_data[i]}，温升={result.servo_data[i] - self.start_temp[i]}')
            time.sleep(2)
        

def main(args=None):
    rclpy.init(args=args)
    example = ExampleNode()
    rclpy.spin(example)

    example.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()