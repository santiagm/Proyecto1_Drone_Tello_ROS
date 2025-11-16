#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class VideoViewer(Node):
    def __init__(self):
        super().__init__("video_viewer")
        self.bridge = CvBridge()
        self.sub = self.create_subscription(
            Image, "tello/image_raw", self.cb, 10
        )

    def cb(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2.imshow("Tello Video", frame)
        cv2.waitKey(1)

def main():
    rclpy.init()
    rclpy.spin(VideoViewer())
    rclpy.shutdown()
