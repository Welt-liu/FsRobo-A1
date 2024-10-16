import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

# from fsrobo_a1_msg_srv_4py.msg import ArmAngle                            # CHANGE


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'follower_arm_topic', 10)  # CHANGE
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Float32MultiArray()                                                # CHANGE
        msg.data = [self.i+0.0, self.i+1.0, self.i+2.0, self.i+3.0]                                           # CHANGE
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)       # CHANGE
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()