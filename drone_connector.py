#!/usr/bin/env python3
from djitellopy import Tello
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String, Int32
import cv2
from cv_bridge import CvBridge

class DroneConnector(Node):
    def __init__(self):
        super().__init__("drone_connector")

        self.tello = Tello()
        self.tello.connect()
        self.tello.streamon()

        self.bridge = CvBridge()

        self.pub_battery = self.create_publisher(Int32, "tello/battery", 10)
        self.pub_height = self.create_publisher(Int32, "tello/height", 10)
        self.pub_image  = self.create_publisher(Image, "tello/image_raw", 10)

        self.sub_cmd = self.create_subscription(
            String, "tello/cmd", self.cmd_callback, 10
        )

        self.timer = self.create_timer(0.1, self.update)

    def cmd_callback(self, msg):
        self.tello.send_command_with_return(msg.data)

    def update(self):
        battery = self.tello.get_battery()
        height  = self.tello.get_height()
        frame   = self.tello.get_frame_read().frame

        self.pub_battery.publish(Int32(data=battery))
        self.pub_height.publish(Int32(data=height))

        img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        self.pub_image.publish(img_msg)

def main():
    rclpy.init()
    node = DroneConnector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
