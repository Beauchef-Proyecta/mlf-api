from core.robot import RobotClient
import time

robot = RobotClient("rainbowdash.local")

robot.get_frame()
robot.showVideo()

time.sleep(10)
robot.closeWebRTC()