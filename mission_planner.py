#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class MissionPlanner(Node):
    def __init__(self):
        super().__init__("mission_planner")
        self.pub = self.create_publisher(String, "tello/cmd", 10)
        self.timer = self.create_timer(1.0, self.run)
        self.executed = False

    def run(self):
        if self.executed:
            return
        cmds = ["takeoff", "forward 50", "cw 90", "forward 80", "land"]
        for cmd in cmds:
            self.pub.publish(String(data=cmd))
            self.get_logger().info(f"Sent: {cmd}")
            time.sleep(3)
        self.executed = True

def main():
    rclpy.init()
    rclpy.spin(MissionPlanner())
    rclpy.shutdown()

if __name__ == "__main__":
    main()
