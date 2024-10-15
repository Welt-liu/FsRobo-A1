import rclpy
from rclpy.node import Node

from fsrobo_a1_msg_srv_4py.msg import ArmAngle                            # CHANGE


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(ArmAngle, 'topic', 10)  # CHANGE
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = ArmAngle()                                                # CHANGE
        msg.angle = [self.i+0.0, self.i+1.0, self.i+2.0, self.i+3.0]                                           # CHANGE
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.angle)       # CHANGE
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()