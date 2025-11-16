#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class ObjectDetector(Node):
    def __init__(self):
        super().__init__("object_detector")
        self.bridge = CvBridge()
        self.sub = self.create_subscription(
            Image, "tello/image_raw", self.cb, 10
        )

    def cb(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        red1 = cv2.inRange(hsv, (0,100,100), (10,255,255))
        red2 = cv2.inRange(hsv, (160,100,100), (179,255,255))
        red  = red1 | red2

        black = cv2.inRange(hsv, (0,0,0), (180,255,40))

        contours_r, _ = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_b, _ = cv2.findContours(black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours_r:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        for c in contours_b:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)

        cv2.imshow("Detección", frame)
        cv2.waitKey(1)

def main():
    rclpy.init()
    rclpy.spin(ObjectDetector())
    rclpy.shutdown()
