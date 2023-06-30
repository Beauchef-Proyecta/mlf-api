from core.robot import RobotClient
import time
import cv2

robot = RobotClient("rainbowdash.local")

robot.showVideo()

time.sleep(10)

robot.closeWebRTC()