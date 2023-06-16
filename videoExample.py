from core.robot import RobotClient
import time

robot = RobotClient("rainbowdash.local")

frame = robot.get_frame()
print(frame)
time.sleep(3)
robot.closeWebRTC()