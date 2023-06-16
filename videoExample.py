from core.robot import RobotClient
import time
import cv2

robot = RobotClient("rainbowdash.local")

frame = robot.get_frame()
cv2.imshow("frame", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
robot.closeWebRTC()