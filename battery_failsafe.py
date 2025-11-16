#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String

class BatteryFailsafe(Node):
    def __init__(self):
        super().__init__("battery_failsafe")
        self.sub = self.create_subscription(
            Int32, "tello/battery", self.check_battery, 10
        )
        self.pub = self.create_publisher(String, "tello/cmd", 10)

    def check_battery(self, msg):
        if msg.data < 20:
            self.get_logger().warn("Batería baja — Aterrizando.")
            self.pub.publish(String(data="land"))

def main():
    rclpy.init()
    rclpy.spin(BatteryFailsafe())
    rclpy.shutdown()
