#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class TelemetryMonitor(Node):
    def __init__(self):
        super().__init__("telemetry_monitor")

        self.create_subscription(Int32, "tello/battery", self.battery_cb, 10)
        self.create_subscription(Int32, "tello/height", self.height_cb, 10)

    def battery_cb(self, msg):
        self.get_logger().info(f"Batería: {msg.data}%")

    def height_cb(self, msg):
        self.get_logger().info(f"Altura: {msg.data} cm")

def main():
    rclpy.init()
    rclpy.spin(TelemetryMonitor())
    rclpy.shutdown()
