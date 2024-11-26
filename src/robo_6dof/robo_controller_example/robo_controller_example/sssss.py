import rclpy
from rclpy.node import Node
from robo_interfaces.srv import RoboStates
import time

class ExampleNode(Node):
    def __init__(self):
        super().__init__('example_node')

        self.servo_servicer = self.create_client(RoboStates, 'robo_states')
        while not self.servo_servicer.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.get_logger().info('service available')
        
        self.loop_()

    
    def send_servo_to_zero(self):
        req = RoboStates.Request()
        req.command = 'zero'
        self.get_logger().info('等待..')
        future = self.servo_servicer.call_async(req)
        self.servo_servicer.wait_for_service()
        return future.result()
    
    def loop_(self):
        while True:
            self.send_servo_to_zero()
            time.sleep(1)
        

def main(args=None):
    rclpy.init(args=args)
    example = ExampleNode()
    rclpy.spin(example)

    example.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()